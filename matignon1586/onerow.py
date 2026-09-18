"""Cut exactly one text row per image - no neighbours in frame, so nothing can be read twice.
   python onerow.py <flat.png> <lines.txt> <out> <first> <last> [cols=3]"""
import sys
from PIL import Image, ImageOps, ImageDraw
src, ysf, out = sys.argv[1], sys.argv[2], sys.argv[3]
lo, hi = int(sys.argv[4]), int(sys.argv[5])
K = int(sys.argv[6]) if len(sys.argv) > 6 else 3
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
ys = [int(v) for v in open(ysf).read().split(',')]
pitch = (ys[-1]-ys[0])/max(1, len(ys)-1)
W = im.width; ov = 90
import os
SLOPE = 0.0
if os.path.exists(sys.argv[2].replace('_lines.txt', '_slope.txt')):
    SLOPE = float(open(sys.argv[2].replace('_lines.txt', '_slope.txt')).read())
step = (W + ov*(K-1))//K
for i in range(lo, min(hi, len(ys))):
    y = ys[i]
    y0, y1 = int(y-0.62*pitch), int(y+0.42*pitch)
    for c in range(K):
        x0 = max(0, c*(step-ov)); x1 = min(W, x0+step)
        dy = int(SLOPE*((x0+x1)/2 - W/2))          # rows slope: each column needs its own y
        t = im.crop((x0, y0+dy, x1, y1+dy)).convert('RGB')
        d = ImageDraw.Draw(t); d.rectangle([0, 0, 52, t.height], fill=(255, 255, 255))
        d.text((4, t.height//2-6), str(i+1), fill=(200, 0, 0))
        s = 1950/t.width
        t.resize((1950, int(t.height*s)), Image.LANCZOS).save(f'{out}_{i+1:02d}_{c}.png')
print(f'rows {lo+1}..{min(hi,len(ys))} x {K} cols')
