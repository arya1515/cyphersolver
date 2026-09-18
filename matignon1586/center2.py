"""Set each line's y to the centre of mass of its x-height band.

Within a window around the fitted y, keep only the rows whose ink exceeds a fraction of the
window's peak (that drops ascenders and descenders, which are sparse), and take their centroid.
"""
import sys, numpy as np
from PIL import Image, ImageOps
src, ysfile, win = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
a = np.array(im); ink = (a < 140).sum(axis=1).astype(float)
ys = [int(v) for v in open(ysfile).read().split(',')]
out = []
for y in ys:
    lo, hi = max(0, y-win), min(len(ink), y+win)
    seg = ink[lo:hi]
    if seg.max() <= 0: out.append(y); continue
    keep = seg >= 0.55*seg.max()
    idx = np.where(keep)[0]
    out.append(int(lo + idx.mean()))
print(','.join(map(str, out)))
print('shift', [o-y for o, y in zip(out, ys)][:12])
open(ysfile, 'w').write(','.join(map(str, out)))
