"""Cut a flattened cipher block into per-row tiles with alternate rows tinted, so the left and right
half of one row always carry the same wash and joins never depend on trusting a line number.
   python rowcut.py <flat.png> <lines.txt> <out> [rows_per_image=3]"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageChops
src, ysf, out = sys.argv[1], sys.argv[2], sys.argv[3]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 3
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
ys = [int(v) for v in open(ysf).read().split(',')]
W = im.width; half = W//2 + 90
def cut(rng, name, xa, xb):
    rows = []
    for i in rng:
        y = ys[i]; t = im.crop((xa, y-88, xb, y+30)).convert('RGB')
        if i % 2:
            t = ImageChops.multiply(t, Image.new('RGB', t.size, (255, 228, 228)))
        d = ImageDraw.Draw(t)
        d.rectangle([0, 0, 90, 118], fill=(255, 255, 255))
        d.text((12, 50), 'L%d' % (i+1), fill=(200, 0, 0))
        rows.append(t)
    H = sum(r.height for r in rows)
    o = Image.new('RGB', (xb-xa, H), (255, 255, 255)); yy = 0
    for r in rows: o.paste(r, (0, yy)); yy += r.height
    s = min(1.0, 1950/o.width)
    o.resize((int(o.width*s), int(o.height*s)), Image.LANCZOS).save(name)
for s in range(0, len(ys), n):
    rng = range(s, min(s+n, len(ys)))
    cut(rng, f'{out}_{s//n+1:02d}_0.png', 0, half)
    cut(rng, f'{out}_{s//n+1:02d}_1.png', W-half, W)
print((len(ys)+n-1)//n, 'images x 2 halves')
