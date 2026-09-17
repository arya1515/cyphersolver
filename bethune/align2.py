"""align2.py - forced alignment over component boundaries.

align.py let the cut fall anywhere, and with a uniform start every template collapsed to the average
glyph. Here the cuts are restricted to the boundaries a connected-component pass already proposes. That
pass over-cuts (about 1.4 components per glyph) but almost never merges two glyphs, so the true glyph
boundaries are a subset of its boundaries, and the job becomes choosing which of them to keep: token t
takes 1..MAXC consecutive components. A per-class width model (log-normal, re-estimated each round)
supplies the signal that breaks the symmetry, since ',' marks, single letters and two-figure groups
differ sharply in width.

  python bethune/align2.py bethune/blocks.json --iters 8 --out bethune/tpl.npz --montage DIR
"""
import sys, os, json, math
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy import ndimage

H = 80
NB = 14
MAXC = 4
WT_IMG = 12.0       # weight on the template cosine
WT_W = 1.0          # weight on the width model


def band_array(canvas, y0, y1, x0, x1, pages):
    im = pages.get(canvas)
    if im is None:
        im = Image.open('bethune/full/c%03d.jpg' % canvas).convert('L')
        pages[canvas] = im
    W, Hh = im.size
    band = ImageOps.autocontrast(im.crop((int(W*x0), int(Hh*y0), int(W*x1), int(Hh*y1))), cutoff=1)
    a = 255.0 - np.asarray(band, dtype=np.float32)
    a = np.clip(a - 60.0, 0, None)
    rows = a.sum(axis=1)
    nz = np.nonzero(rows > rows.max()*0.02)[0]
    if len(nz):
        a = a[max(0, nz[0]-4):min(a.shape[0], nz[-1]+5)]
    cols = a.sum(axis=0)
    nzc = np.nonzero(cols > max(1.0, cols.max()*0.01))[0]
    if len(nzc):
        a = a[:, max(0, nzc[0]-3):min(a.shape[1], nzc[-1]+4)]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    img = img.resize((max(1, int(img.width*H/img.height)), H), Image.LANCZOS)
    return np.asarray(img, dtype=np.float32)/255.0


def components(band):
    """x-intervals of ink components, small parts merged into the one they overlap"""
    bw = band > 0.18
    bw = ndimage.binary_closing(bw, structure=np.ones((2, 2)))
    lab, n = ndimage.label(bw, structure=np.ones((3, 3)))
    if n == 0:
        return []
    objs = ndimage.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs):
        ys, xs = sl
        comps.append([xs.start, xs.stop, int(bw[sl].sum())])
    med = np.median([c[2] for c in comps])
    comps = [c for c in comps if c[2] >= max(4, 0.03*med)]
    comps.sort(key=lambda c: c[0])
    changed = True
    while changed:
        changed = False
        for i in range(len(comps)-1):
            a, b = comps[i], comps[i+1]
            ov = min(a[1], b[1]) - max(a[0], b[0])
            wmin = min(a[1]-a[0], b[1]-b[0])
            if wmin > 0 and ov > 0.92*wmin:
                comps[i] = [min(a[0], b[0]), max(a[1], b[1]), a[2]+b[2]]
                del comps[i+1]; changed = True; break
    return [(c[0], c[1]) for c in comps]


def strip_and_cuts(spans, pages):
    parts, cuts, off = [], [], 0
    for sp in spans:
        b = band_array(*sp, pages)
        cs = components(b)
        for (x0, x1) in cs:
            cuts.append((x0+off, x1+off))
        parts.append(b); off += b.shape[1]
    return np.concatenate(parts, axis=1), cuts


def desc(strip, x0, x1):
    x1 = max(x1, x0+1)
    seg = strip[:, x0:x1]
    w = seg.shape[1]
    e = np.linspace(0, w, NB+1)
    out = np.empty((H, NB), np.float32)
    for b in range(NB):
        a0 = min(int(e[b]), w-1)
        a1 = max(int(e[b+1]), a0+1)
        out[:, b] = seg[:, a0:min(a1, w)].mean(axis=1)
    v = out.reshape(-1)
    return v/max(np.linalg.norm(v), 1e-6)


def align(strip, cuts, tokens, templates, classes, wmu, wsd):
    C, T = len(cuts), len(tokens)
    NEG = -1e18
    dp = np.full((T+1, C+1), NEG)
    bp = np.zeros((T+1, C+1), np.int32)
    dp[0, 0] = 0.0
    cache = {}
    for t in range(T):
        k = classes.get(tokens[t], -1)
        for i in range(C):
            if dp[t, i] <= NEG/2:
                continue
            for m in range(1, MAXC+1):
                j = i+m
                if j > C:
                    break
                key = (i, j)
                if key not in cache:
                    cache[key] = desc(strip, cuts[i][0], cuts[j-1][1])
                d = cache[key]
                w = cuts[j-1][1]-cuts[i][0]
                sc = dp[t, i] + WT_IMG*float(d @ templates[k]) if k >= 0 else dp[t, i]
                if k >= 0 and wsd[k] > 0:
                    z = (math.log(max(w, 2))-wmu[k])/wsd[k]
                    sc -= WT_W*0.5*z*z
                if sc > dp[t+1, j]:
                    dp[t+1, j] = sc; bp[t+1, j] = i
    if dp[T, C] <= NEG/2:
        return None, NEG
    segs = []; j = C
    for t in range(T, 0, -1):
        i = int(bp[t, j]); segs.append((cuts[i][0], cuts[j-1][1])); j = i
    return segs[::-1], float(dp[T, C])


def main():
    cfg = json.load(open(sys.argv[1], encoding='utf-8'))
    iters = int(sys.argv[sys.argv.index('--iters')+1]) if '--iters' in sys.argv else 8
    out = sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else 'bethune/tpl.npz'
    montage = sys.argv[sys.argv.index('--montage')+1] if '--montage' in sys.argv else None
    pages, blocks = {}, []
    for b in cfg['blocks']:
        strip, cuts = strip_and_cuts(b['spans'], pages)
        toks = b['tokens'].split()
        toks = [toks[i-1] if (t == 'PH' and i > 0) else t for i, t in enumerate(toks)]
        blocks.append({'id': b['id'], 'strip': strip, 'cuts': cuts, 'tokens': toks})
        print('%-4s %5d px  %3d comps  %3d tokens  %.2f comp/token' %
              (b['id'], strip.shape[1], len(cuts), len(toks), len(cuts)/len(toks)))
    vocab = sorted({t for b in blocks for t in b['tokens']})
    classes = {t: i for i, t in enumerate(vocab)}
    K = len(vocab)
    templates = np.zeros((K, H*NB), np.float32)
    wmu = np.full(K, math.log(24.0)); wsd = np.full(K, 0.55)
    cnt = np.zeros(K)
    for b in blocks:                                   # proportional start over components
        C, T = len(b['cuts']), len(b['tokens'])
        for t, tok in enumerate(b['tokens']):
            i, j = int(round(t*C/T)), max(int(round((t+1)*C/T)), int(round(t*C/T))+1)
            j = min(j, C)
            templates[classes[tok]] += desc(b['strip'], b['cuts'][i][0], b['cuts'][j-1][1])
            cnt[classes[tok]] += 1
    templates /= np.maximum(np.linalg.norm(templates, axis=1, keepdims=True), 1e-6)
    allsegs = None
    for it in range(iters):
        newt = np.zeros_like(templates); cnt = np.zeros(K)
        ws = [[] for _ in range(K)]
        allsegs = []; tot = 0.0
        for b in blocks:
            segs, sc = align(b['strip'], b['cuts'], b['tokens'], templates, classes, wmu, wsd)
            allsegs.append(segs)
            if segs is None:
                print('   align failed', b['id']); continue
            tot += sc
            for (x0, x1), tok in zip(segs, b['tokens']):
                k = classes[tok]
                newt[k] += desc(b['strip'], x0, x1); cnt[k] += 1
                ws[k].append(math.log(max(x1-x0, 2)))
        keep = cnt > 0
        newt[keep] /= np.maximum(np.linalg.norm(newt[keep], axis=1, keepdims=True), 1e-6)
        templates[keep] = newt[keep]
        for k in range(K):
            if len(ws[k]) >= 2:
                wmu[k] = float(np.mean(ws[k])); wsd[k] = max(0.15, float(np.std(ws[k])))
            elif len(ws[k]) == 1:
                wmu[k] = ws[k][0]; wsd[k] = 0.35
        print('iter %d  score %.1f' % (it+1, tot))
    np.savez(out, templates=templates, vocab=np.array(vocab), wmu=wmu, wsd=wsd, counts=cnt)
    print('wrote', out, ' classes', K)
    if montage:
        os.makedirs(montage, exist_ok=True)
        for b, segs in zip(blocks, allsegs):
            if segs is None:
                continue
            im = Image.fromarray((255*(1.0-b['strip'])).astype(np.uint8)).convert('RGB')
            d = ImageDraw.Draw(im)
            for (x0, x1), tok in zip(segs, b['tokens']):
                d.line([(x0, 0), (x0, H)], fill=(255, 0, 0))
                d.text((x0+1, 0), tok, fill=(0, 0, 255))
            im = im.resize((im.width*2, im.height*2), Image.LANCZOS)
            for i in range(0, im.width, 2400):
                im.crop((i, 0, min(im.width, i+2400), im.height)).save(
                    '%s/%s_%02d.jpg' % (montage, b['id'], i//2400), quality=93)
        print('montages in', montage)


if __name__ == '__main__':
    main()
