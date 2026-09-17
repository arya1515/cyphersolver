# Montage of a line's boxes with labels: montage_lab.py prefix line zoom out labels.json [percol]
# labels.json: {"meta": [...], "labels": {"i": cls}, "align": [...]} from boot2, or {"pred": {"k:j": "an"...}}
import sys, json
from PIL import Image, ImageDraw
PAIRS = ['an', 'bo', 'cp', 'dq', 'er', 'fs', 'gt', 'hu', 'ix', 'ly', 'mz']
NAMES = PAIRS + ['que', 'qui', 'pour', '.', '#']
pre, k, Z, out, labf = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
per = int(sys.argv[6]) if len(sys.argv) > 6 else 15
bx = json.load(open(f'{pre}_g2.json'))[str(k)]
L = json.load(open(labf))
lab = {}
if 'meta' in L:
    for i, (p, kk, j, _, _) in enumerate(L['meta']):
        if p == pre and kk == k:
            a = L['align'][i]
            if a is None: lab[j] = '?'
            elif a[0] == 'm': lab[j] = NAMES[a[1]]
            elif a[0] == 'n': lab[j] = '.'
            else: lab[j] = NAMES[a[1][0]] + '+' + NAMES[a[1][1]]
else:
    for key, v in L['pred'].items():
        kk, j = key.split(':')
        if int(kk) == k: lab[int(j)] = v
im = Image.open(f'{pre}_l{k:02d}.png').convert('L'); w, h = im.size
cw = 60 * Z // 2; ch = h * Z + 30
rows = (len(bx) + per - 1) // per
sheet = Image.new('RGB', (per * cw, rows * ch), (255, 255, 255)); d = ImageDraw.Draw(sheet)
for i, (x0, y0, x1, y1, a) in enumerate(bx):
    pad = 4
    c = im.crop((max(0, x0 - pad), 0, min(w, x1 + pad), h)).resize(((min(w, x1 + pad) - max(0, x0 - pad)) * Z, h * Z), Image.LANCZOS)
    if c.width > cw - 4: c = c.resize((cw - 4, h * Z))
    X = (i % per) * cw; Y = (i // per) * ch
    sheet.paste(c.convert('RGB'), (X + 2, Y + 14))
    d.text((X + 2, Y), str(i), fill=(200, 0, 0))
    d.text((X + 2, Y + 14 + h * Z), lab.get(i, ''), fill=(0, 0, 200))
    d.line((X, Y, X, Y + ch), fill=(180, 180, 180))
sheet.save(out); print(sheet.size, len(bx))
