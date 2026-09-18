"""Tile a block line by line, framing each tile on the line's own ink extent.

Rather than trust a fitted centre, walk out from it until the row-ink falls away, and crop exactly
that band. This adapts per line, so pitch wander and a drifting offset stop mattering.
"""
import sys, json
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage
from rlsa import otsu

src, ysfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
ntile = int(sys.argv[4]) if len(sys.argv) > 4 else 5
which = sys.argv[5] if len(sys.argv) > 5 else None

im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
a = np.array(im)
bw = ndimage.median_filter(a < otsu(a), size=3)
ink = bw.sum(axis=1).astype(float)
ink = np.convolve(ink, np.ones(5)/5, 'same')
ys = [int(v) for v in open(ysfile).read().split(',')]
sel = [int(v)-1 for v in which.split(',')] if which else range(len(ys))
W = a.shape[1]
report = []
for i in sel:
    y = ys[i]
    lo = max(0, y-90); hi = min(len(ink), y+90)
    peak = ink[lo:hi].max()
    if peak <= 0: continue
    th = 0.22*peak
    top = y
    while top > lo and ink[top] > th: top -= 1
    bot = y
    while bot < hi-1 and ink[bot] > th: bot += 1
    # if the fitted centre sat in a gap, snap to the nearest peak first
    if ink[y] < th:
        j = lo + int(np.argmax(ink[lo:hi])); y = j
        top = bot = y
        while top > lo and ink[top] > th: top -= 1
        while bot < hi-1 and ink[bot] > th: bot += 1
    t0, t1 = max(0, top-10), min(a.shape[0], bot+10)
    report.append((i+1, y, t0, t1, t1-t0))
    for j in range(ntile):
        x0 = W*j//ntile; x1 = min(W, W*(j+1)//ntile + 70)
        t = im.crop((x0, t0, x1, t1))
        sc = 1900/t.width
        t = t.resize((int(t.width*sc), int(t.height*sc)), Image.LANCZOS)
        t.save(f'{out}_{i+1:02d}_{j}.png')
print('tiled', len(report))
for r in report[:12]: print('line', r[0], 'centre', r[1], 'band', r[2], r[3], 'h', r[4])
