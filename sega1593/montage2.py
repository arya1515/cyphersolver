# Montage of box crops from {prefix}_g2.json: montage2.py prefix line zoom out [percol]
import sys, json
from PIL import Image, ImageDraw
pre, k, Z, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
per = int(sys.argv[5]) if len(sys.argv) > 5 else 15
bx = json.load(open(f'{pre}_g2.json'))[str(k)]
im = Image.open(f'{pre}_l{k:02d}.png').convert('L'); w, h = im.size
cw = 60 * Z // 2; ch = h * Z + 16
rows = (len(bx) + per - 1) // per
sheet = Image.new('RGB', (per * cw, rows * ch), (255, 255, 255)); d = ImageDraw.Draw(sheet)
for i, (x0, y0, x1, y1, a) in enumerate(bx):
    pad = 4
    c = im.crop((max(0, x0 - pad), 0, min(w, x1 + pad), h)).resize(((min(w, x1 + pad) - max(0, x0 - pad)) * Z, h * Z), Image.LANCZOS)
    if c.width > cw - 4: c = c.resize((cw - 4, h * Z))
    X = (i % per) * cw; Y = (i // per) * ch
    sheet.paste(c.convert('RGB'), (X + 2, Y + 14))
    d.text((X + 2, Y), str(i), fill=(200, 0, 0))
    d.line((X, Y, X, Y + ch), fill=(180, 180, 180))
sheet.save(out); print(sheet.size, len(bx))
