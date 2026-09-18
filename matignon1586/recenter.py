"""Re-centre fitted line positions on the median centre of the glyph boxes they catch.

An ink-mass centre is pulled around by ascenders and descenders; the x-height band is what the
tiles need to be centred on, and the segmented boxes give it directly.
"""
import sys, numpy as np, json
from PIL import Image, ImageOps
from seg2 import binarize
from shapes import line_boxes
src, ysfile, half, gap = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
bw = binarize(np.array(im))
ys = [int(v) for v in open(ysfile).read().split(',')]
for it in range(3):
    out = []
    for y in ys:
        bs = line_boxes(bw, y, half, gap)
        if not bs: out.append(y); continue
        cs = sorted((b[2]+b[3])//2 for b in bs)
        med = cs[len(cs)//2]
        out.append(int(round(0.5*y + 0.5*med)))
    ys = out
print(','.join(map(str, ys)))
print('diffs', [ys[i+1]-ys[i] for i in range(len(ys)-1)])
open(ysfile, 'w').write(','.join(map(str, ys)))
