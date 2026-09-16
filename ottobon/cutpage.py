"""Clean a page region of a BNE opening and cut it into single lines at 3x, two overlapping halves per line.
python cutpage.py hi08.jpg f38r 1240 200 2140 830 [nlines]
Line positions: a regular grid (period from the autocorrelation of the row-ink profile, phase from the profile),
which is robust to the bleed-through and the irregular ink density. Writes img/<tag>_clean.png,
img/<tag>_grid.png (grid overlay for checking) and img/lines/<tag>_lNN_a.png / _b.png."""
import sys, os
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
src, tag = sys.argv[1], sys.argv[2]; x0, y0, x1, y1 = map(int, sys.argv[3:7])
nl = int(sys.argv[7]) if len(sys.argv) > 7 else None
im = Image.open(os.path.join('img', src)).convert('L').crop((x0, y0, x1, y1))
a = np.array(im).astype(float); bg = np.array(im.filter(ImageFilter.GaussianBlur(30))).astype(float)
n = np.clip(255 * (a / (bg + 1)), 0, 255); out = np.clip((n / 255.0) ** 2.0 * 255 * 1.1, 0, 255).astype(np.uint8)
im2 = Image.fromarray(out); im2.save(os.path.join('img', tag + '_clean.png'))
rows = (out < 100).sum(1).astype(float); rows -= rows.mean()
ac = np.correlate(rows, rows, 'full')[len(rows) - 1:]
lo = int(sys.argv[8]) if len(sys.argv) > 8 else 50
per = lo + int(np.argmax(ac[lo:90]))
# phase: maximise summed profile at grid points
best = None
for ph in range(per):
    ys = np.arange(ph, len(rows), per); s = (rows[ys] > 0).sum() * 1000 + rows[ys].sum()
    if best is None or s > best[0]: best = (s, ph)
ph = best[1]; ys = [y for y in range(ph, len(rows), per)]
# drop grid lines with no ink (blank top/bottom)
rowsum = (out < 100).sum(1)
ys = [y for y in ys if rowsum[max(y - per // 2, 0):y + per // 2].sum() > 0.15 * np.percentile([rowsum[max(v - per // 2, 0):v + per // 2].sum() for v in ys], 60)]
if nl: ys = ys[:nl]
# refine each centre to the local maximum of the smoothed profile within a third of a period
smr = np.convolve((out < 100).sum(1).astype(float), np.ones(15) / 15, mode='same')
ys = [int(max(y - per // 3, 0) + np.argmax(smr[max(y - per // 3, 0):y + per // 3])) for y in ys]
print(tag, 'period', per, 'lines', len(ys), ys)
g = im2.convert('RGB'); d = ImageDraw.Draw(g)
for y in ys: d.line([(0, y), (g.width, y)], fill=(255, 0, 0), width=1)
g.save(os.path.join('img', tag + '_grid.png'))
os.makedirs('img/lines', exist_ok=True); w = im2.width; h2 = per // 2 + 12
for i, y in enumerate(ys):
    c = im2.crop((0, max(y - h2, 0), w, min(y + h2, im2.height)))
    sc = 2000.0 / w
    cc = c.resize((int(w * sc), int(c.height * sc)), Image.LANCZOS).convert('RGB')
    dd = ImageDraw.Draw(cc); dd.rectangle([0, 0, 120, 22], fill=(255, 255, 255)); dd.text((4, 4), '%s l%02d' % (tag, i + 1), fill=(200, 0, 0))
    cc.save('img/lines/%s_l%02d.png' % (tag, i + 1))
