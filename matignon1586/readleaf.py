"""Read a leaf from its figures alone: segment, match each box against the labelled exemplars,
and decode the resulting letter-sets by beam search against the French model.

No figure is ever named. Each box gets a distribution over letters from how closely it resembles
the crib-labelled exemplars, and the language model chooses among them - which is the right model
for this cipher, since the exemplars show i/n/s and e/u are not separable by shape.
"""
import sys, json, math
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from scipy import ndimage
from rlsa import otsu
from shapes import line_boxes
from solve import segment as wordsplit
import pickle

D = pickle.load(open('lm.pkl','rb')); CNT = D['cnt']; N = D['N']
AL = 'abcdefghilmnopqrstuxyz'; LAM = 0.4
CHAR_BONUS = 1.6   # ~ the model's mean per-character cost
def clogp(ctx, ch):
    tot = 0.0; w = 1.0
    for n in range(N, 1, -1):
        c = ctx[-(n-1):]
        if len(c) < n-1: continue
        den = CNT[n-1][c]
        if den < 2: continue
        tot += w*LAM*(CNT[n][c+ch]/den); w *= (1-LAM)
        if w < 1e-6: break
    tot += w*(CNT[1][ch]+1)/(sum(CNT[1].values())+22)
    return math.log(max(tot, 1e-12))

S = 26
def vec_from(arr):
    a = 255 - arr.astype(np.float32)
    if a.max() > 0: a = a/a.max()
    h, w = a.shape
    sc = (S-4)/max(h, w)
    g = Image.fromarray((a*255).astype(np.uint8)).resize(
        (max(1,int(w*sc)), max(1,int(h*sc))), Image.BILINEAR)
    canv = Image.new('L', (S,S), 0); canv.paste(g, ((S-g.width)//2, (S-g.height)//2))
    canv = canv.filter(ImageFilter.GaussianBlur(1.1))
    v = np.asarray(canv, dtype=np.float32).ravel(); v -= v.mean()
    return v/(np.linalg.norm(v) or 1.0)

man = json.load(open('exemplars/manifest.json'))
EX = [(m['letter'], vec_from(np.asarray(Image.open(m['file']).convert('L')))) for m in man]

def cands_for(box_img, topk=4, temp=12.0):
    v = vec_from(box_img)
    sims = sorted(((float(v@e), l) for l, e in EX), reverse=True)[:topk]
    best = sims[0][0]
    out = {}
    for s, l in sims:
        out[l] = max(out.get(l, -9e9), (s-best)*temp)
    return sorted(out.items(), key=lambda kv: -kv[1])

def read(src, ysfile, gap, lines):
    im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
    a = np.array(im); bw = ndimage.median_filter(a < otsu(a), size=3)
    ys = [int(v) for v in open(ysfile).read().split(',')]
    ink = np.convolve((a<(a.mean()-0.45*a.std())).sum(axis=1).astype(float), np.ones(11)/11, 'same')
    pitch = int(np.median(np.diff(ys))); w = max(10, int(0.38*pitch))
    ys = [int(max(0,y-w)+np.argmax(ink[max(0,y-w):min(len(ink),y+w)])) for y in ys]
    for li in lines:
        bs = line_boxes(bw, ys[li-1], 40, gap)
        cands = [cands_for(a[y0:y1, x0:x1]) for (x0,x1,y0,y1) in bs]
        beams = [('', 0.0)]
        for cl in cands:
            nb = []
            for txt, sc in beams:
                for l, pen in cl[:3]:
                    # Beam search over variable-length emissions is biased towards short ones:
                    # a code group emitting eight characters pays eight characters of log-prob
                    # while a letter pays one, although both consume exactly one figure. Offset it
                    # with a per-character bonus at the model's average cost, so hypotheses that
                    # consume the same number of figures are compared on equal terms.
                    sc2 = sc + pen; c = txt
                    for ch in l:
                        sc2 += clogp(c[-(N-1):], ch) + CHAR_BONUS; c += ch
                    nb.append((c, sc2))
            nb.sort(key=lambda x: -x[1])
            seen = set(); out = []
            for txt, sc in nb:
                k = txt[-(N-1):]
                if k in seen: continue
                seen.add(k); out.append((txt, sc))
                if len(out) >= 300: break
            beams = out
        print(f'line {li:2d} ({len(bs)} figures):', wordsplit(beams[0][0]))

if __name__ == '__main__':
    read(sys.argv[1], sys.argv[2], int(sys.argv[3]), [int(x) for x in sys.argv[4].split(',')])
