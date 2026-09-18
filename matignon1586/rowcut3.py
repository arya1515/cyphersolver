"""Like rowcut.py but cuts each row band into K overlapping columns, for small dense hands.
   python rowcut3.py <flat.png> <lines.txt> <out> [rows=2] [cols=3]"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageChops
src, ysf, out = sys.argv[1], sys.argv[2], sys.argv[3]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 2
K = int(sys.argv[5]) if len(sys.argv) > 5 else 3
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
ys = [int(v) for v in open(ysf).read().split(',')]
pitch = (ys[-1]-ys[0])/max(1, len(ys)-1)
W = im.width; ov = 110
step = (W + ov*(K-1))//K
up, dn = int(1.05*pitch), int(0.45*pitch)
for s in range(0, len(ys), n):
    grp = list(range(s, min(s+n, len(ys))))
    for c in range(K):
        x0 = max(0, c*(step-ov)); x1 = min(W, x0+step)
        rows = []
        for i in grp:
            y = ys[i]; t = im.crop((x0, y-up, x1, y+dn)).convert('RGB')
            if i % 2:
                t = ImageChops.multiply(t, Image.new('RGB', t.size, (255, 226, 226)))
            d = ImageDraw.Draw(t); d.rectangle([0, 0, 58, t.height], fill=(255, 255, 255))
            d.text((6, t.height//2-6), 'L%d' % (i+1), fill=(200, 0, 0)); rows.append(t)
        H = sum(r.height for r in rows)
        o = Image.new('RGB', (x1-x0, H), (255, 255, 255)); yy = 0
        for r in rows: o.paste(r, (0, yy)); yy += r.height
        sc = 1950/o.width
        o.resize((1950, int(o.height*sc)), Image.LANCZOS).save(f'{out}_{s//n+1:02d}_{c}.png')
print((len(ys)+n-1)//n, 'bands x', K, 'cols')
