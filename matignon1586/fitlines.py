"""Fit a uniform line grid to a flattened block and snap it to the ink.
   python fitlines.py <flat.png> <out_lines.txt> [lo_pitch] [hi_pitch]"""
import sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw
src, out = sys.argv[1], sys.argv[2]
lo = float(sys.argv[3]) if len(sys.argv) > 3 else 90
hi = float(sys.argv[4]) if len(sys.argv) > 4 else 150
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
a = np.array(im); H, W = a.shape
cov = (a[:, :int(0.8*W)] < 115).sum(axis=1).astype(float)
cov[cov > 0.62*0.8*W] = 0.0          # page edge / dark band: not a text line
p = np.convolve(cov, np.ones(15)/15, 'same')
best = None
for sp in np.arange(lo, hi, 0.25):
    for q in range(int(sp)):
        ys = np.arange(q, H-20, sp).astype(int)
        s = p[ys].mean()
        if best is None or s > best[0]: best = (s, sp, q)
_, sp, q = best
ys = [int(q+sp*i) for i in range(int((H-q)/sp))]
ref = np.percentile([p[y] for y in ys], 75)
ink = [p[y] > 0.35*ref for y in ys]
first = ink.index(True); last = len(ink)-1-ink[::-1].index(True)
ys = ys[first:last+1]
d = max(((p[[min(H-1, y+t) for y in ys]].mean(), t) for t in range(-45, 46)))[1]
ys = [y+d for y in ys]
open(out, 'w').write(','.join(map(str, ys)))
o = im.convert('RGB'); dr = ImageDraw.Draw(o)
for i, y in enumerate(ys):
    dr.line([(0, y), (W, y)], fill=(255, 0, 0), width=2); dr.text((8, y-36), str(i+1), fill=(255, 0, 0))
o.resize((950, int(H*950/W))).save(out.replace('.txt', '_ov.png'))
print('pitch %.1f lines %d' % (sp, len(ys)))
