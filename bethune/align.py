"""align.py - forced alignment of a known token sequence to the ink of a cipher block.

The hard part of reading this hand is not the key but the cut between glyphs: a connected-component
segmenter over-cuts by about 40 %. This module never cuts. It concatenates the cipher spans of a block
into one strip, normalises it to a fixed height, and runs a dynamic program that assigns each token of
the known sequence a variable-width slice of the strip, scoring a slice against a per-class template.
Templates start from a uniform split and are re-estimated from the alignment (hard EM), so after a few
rounds every token type has a picture of itself averaged over all its occurrences.

Those templates are the point: they give a labelled exemplar sheet for the hand, and a classifier that
can be run over the leaves that have no decipherment.

  python bethune/align.py blocks.json --iters 6 --out templates.npz [--montage DIR]
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageOps

H = 80          # normalised strip height
NB = 14         # horizontal bins in a slice descriptor
WMIN, WMAX, WSTEP = 14, 140, 2


def strip_of(spans, pages):
    """concatenate the ink of the given (canvas, y0, y1, x0, x1) fractional spans into one array"""
    parts = []
    for canvas, y0, y1, x0, x1 in spans:
        im = pages.get(canvas)
        if im is None:
            im = Image.open('bethune/full/c%03d.jpg' % canvas).convert('L')
            pages[canvas] = im
        W, Hh = im.size
        band = im.crop((int(W*x0), int(Hh*y0), int(W*x1), int(Hh*y1)))
        band = ImageOps.autocontrast(band, cutoff=1)
        a = 255.0 - np.asarray(band, dtype=np.float32)      # ink positive
        a = np.clip(a - 60.0, 0, None)
        rows = a.sum(axis=1)
        nz = np.nonzero(rows > rows.max()*0.02)[0]
        if len(nz):
            a = a[max(0, nz[0]-4):min(a.shape[0], nz[-1]+5)]
        cols = a.sum(axis=0)                                  # trim leading/trailing blank
        nzc = np.nonzero(cols > max(1.0, cols.max()*0.01))[0]
        if len(nzc):
            a = a[:, max(0, nzc[0]-3):min(a.shape[1], nzc[-1]+4)]
        img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        img = img.resize((max(1, int(img.width*H/img.height)), H), Image.LANCZOS)
        parts.append(np.asarray(img, dtype=np.float32))
    strip = np.concatenate(parts, axis=1)
    strip /= max(1.0, strip.max())
    return strip


def descriptors(strip, w):
    """descriptor of every slice of width w: (nx, H*NB), L2-normalised"""
    Hh, W = strip.shape
    if W < w:
        return np.zeros((0, Hh*NB), np.float32)
    cs = np.zeros((Hh, W+1), np.float32)
    np.cumsum(strip, axis=1, out=cs[:, 1:])
    edges = np.round(np.linspace(0, w, NB+1)).astype(int)
    for b in range(NB):                                  # keep every bin non-empty and inside [0, w]
        if edges[b+1] <= edges[b]:
            edges[b+1] = min(edges[b]+1, w)
    edges[NB] = w
    nx = W - w + 1
    out = np.empty((nx, Hh, NB), np.float32)
    xs = np.arange(nx)
    for b in range(NB):
        b0, b1 = edges[b], edges[b+1]
        if b1 == b0:
            b1 = b0 + 1
        seg = (cs[:, xs+b1] - cs[:, xs+b0]) / (b1-b0)       # (H, nx)
        out[:, :, b] = seg.T
    out = out.reshape(nx, Hh*NB)
    n = np.linalg.norm(out, axis=1, keepdims=True)
    out /= np.maximum(n, 1e-6)
    return out


def align_block(strip, tokens, templates, classes, widths):
    """DP: assign each token a slice. returns list of (x0, x1) per token, and the score"""
    W = strip.shape[1]
    T = len(tokens)
    ws = list(range(WMIN, WMAX+1, WSTEP))
    # cost[w][x][k] -> use only the classes we need
    idx = [classes.get(t, -1) for t in tokens]
    cost = {}
    for w in ws:
        d = descriptors(strip, w)
        if d.shape[0] == 0:
            cost[w] = None; continue
        cost[w] = d @ templates.T                            # (nx, K) cosine
    NEG = -1e18
    dp = np.full((T+1, W+1), NEG, np.float64)
    bp = np.zeros((T+1, W+1, 2), np.int32)
    dp[0, 0] = 0.0
    for t in range(T):
        k = idx[t]
        row = dp[t]
        valid = np.nonzero(row > NEG/2)[0]
        if len(valid) == 0:
            break
        for w in ws:
            c = cost[w]
            if c is None:
                continue
            xs = valid[valid + w <= W]
            if len(xs) == 0:
                continue
            sc = row[xs] + (c[xs, k] if k >= 0 else 0.0) * 10.0 + widths.get(tokens[t], {}).get(w, 0.0)
            tgt = xs + w
            better = sc > dp[t+1][tgt]
            if better.any():
                dp[t+1][tgt[better]] = sc[better]
                bp[t+1][tgt[better], 0] = xs[better]
                bp[t+1][tgt[better], 1] = w
    if dp[T, W] <= NEG/2:
        # allow the last token to stop short of the end
        end = int(np.argmax(dp[T]))
        if dp[T, end] <= NEG/2:
            return None, NEG
    else:
        end = W
    segs = []
    x = end
    for t in range(T, 0, -1):
        x0 = int(bp[t, x, 0])
        segs.append((x0, x))
        x = x0
    return segs[::-1], float(dp[T, end])


def slice_desc(strip, x0, x1):
    d = descriptors(strip[:, x0:x1], x1-x0)
    return d[0] if d.shape[0] else np.zeros(H*NB, np.float32)


def main():
    cfg = json.load(open(sys.argv[1], encoding='utf-8'))
    iters = int(sys.argv[sys.argv.index('--iters')+1]) if '--iters' in sys.argv else 6
    out = sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else 'bethune/templates.npz'
    montage = sys.argv[sys.argv.index('--montage')+1] if '--montage' in sys.argv else None
    pages = {}
    blocks = []
    for b in cfg['blocks']:
        strip = strip_of(b['spans'], pages)
        toks = b['tokens'].split()
        toks = [toks[i-1] if (t == 'PH' and i > 0) else t for i, t in enumerate(toks)]
        blocks.append({'id': b['id'], 'strip': strip, 'tokens': toks})
        print('%-4s strip %d px, %d tokens, %.1f px/token' %
              (b['id'], strip.shape[1], len(toks), strip.shape[1]/len(toks)))
    vocab = sorted({t for b in blocks for t in b['tokens']})
    classes = {t: i for i, t in enumerate(vocab)}
    K = len(vocab)
    print('classes', K)
    # --- initialise templates from a uniform split
    templates = np.zeros((K, H*NB), np.float32)
    counts = np.zeros(K)
    for b in blocks:
        n = len(b['tokens']); W = b['strip'].shape[1]
        for t, tok in enumerate(b['tokens']):
            x0, x1 = int(W*t/n), int(W*(t+1)/n)
            if x1-x0 < 4:
                continue
            templates[classes[tok]] += slice_desc(b['strip'], x0, x1)
            counts[classes[tok]] += 1
    templates /= np.maximum(np.linalg.norm(templates, axis=1, keepdims=True), 1e-6)
    widths = {}
    for it in range(iters):
        newt = np.zeros_like(templates); cnt = np.zeros(K)
        allsegs = []
        tot = 0.0
        for b in blocks:
            segs, sc = align_block(b['strip'], b['tokens'], templates, classes, widths)
            if segs is None:
                print('  align failed', b['id']); allsegs.append(None); continue
            allsegs.append(segs); tot += sc
            for (x0, x1), tok in zip(segs, b['tokens']):
                if x1-x0 < 4:
                    continue
                newt[classes[tok]] += slice_desc(b['strip'], x0, x1)
                cnt[classes[tok]] += 1
        keep = cnt > 0
        newt[keep] /= np.maximum(np.linalg.norm(newt[keep], axis=1, keepdims=True), 1e-6)
        templates[keep] = newt[keep]
        print('iter %d  score %.1f  classes seen %d/%d' % (it+1, tot, int(keep.sum()), K))
    np.savez(out, templates=templates, vocab=np.array(vocab), counts=cnt)
    print('wrote', out)
    if montage:
        os.makedirs(montage, exist_ok=True)
        for b, segs in zip(blocks, allsegs):
            if segs is None:
                continue
            strip = (255*(1.0-b['strip'])).astype(np.uint8)
            im = Image.fromarray(strip).convert('RGB')
            from PIL import ImageDraw
            d = ImageDraw.Draw(im)
            for (x0, x1), tok in zip(segs, b['tokens']):
                d.line([(x0, 0), (x0, H)], fill=(255, 0, 0))
                d.text((x0+1, 0), tok, fill=(0, 0, 255))
            im = im.resize((im.width*2, im.height*2), Image.LANCZOS)
            per = 2400
            for i in range(0, im.width, per):
                im.crop((i, 0, min(im.width, i+per), im.height)).save(
                    '%s/%s_%02d.jpg' % (montage, b['id'], i//per), quality=93)
        print('montages in', montage)


if __name__ == '__main__':
    main()
