"""Cut a flattened cipher block into strips of N lines, split into left/right halves, for reading
several lines per image.   python strips.py <flat.png> <lines.txt> <out> [lines_per_strip=3]"""
import sys
from PIL import Image, ImageOps, ImageDraw
src, ysf, out = sys.argv[1], sys.argv[2], sys.argv[3]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 3
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
ys = [int(v) for v in open(ysf).read().split(',')]
pitch = (ys[-1]-ys[0])/max(1, len(ys)-1)
W = im.width; k = 0
for s in range(0, len(ys), n):
    grp = ys[s:s+n]
    y0 = max(0, int(grp[0]-0.62*pitch)); y1 = min(im.height, int(grp[-1]+0.62*pitch))
    for h in range(2):
        x0 = 0 if h == 0 else W//2 - 60; x1 = W//2 + 60 if h == 0 else W
        t = im.crop((x0, y0, x1, y1)).convert('RGB'); d = ImageDraw.Draw(t)
        for i, y in enumerate(grp):
            d.text((4 if h == 0 else 4, y - y0 - 14), str(s+i+1), fill=(220, 0, 0))
        sc = 1900/t.width
        t.resize((1900, int(t.height*sc)), Image.LANCZOS).save(f'{out}_{s//n+1:02d}_{h}.png')
    k += 1
print(k, 'strips x 2 halves')
