# Cut a manuscript page into text-line strips by horizontal ink projection, and stack them into labelled sheets
# (5 strips per sheet, each downscaled to 2000 px wide) for transcription by eye.
# usage: python strips.py full_c019.jpg [x0frac x1frac y0frac y1frac] [outprefix]
import sys, os
import numpy as np
from PIL import Image, ImageOps, ImageDraw
Image.MAX_IMAGE_PIXELS = None
src = sys.argv[1]
x0f, x1f, y0f, y1f = (float(v) for v in sys.argv[2:6]) if len(sys.argv) >= 6 else (0.18, 0.99, 0.02, 0.98)
pref = sys.argv[6] if len(sys.argv) > 6 else os.path.splitext(os.path.basename(src))[0]
im = Image.open(src).convert('L'); im = ImageOps.autocontrast(im, cutoff=1)
W, H = im.size
box = im.crop((int(W * x0f), int(H * y0f), int(W * x1f), int(H * y1f)))
a = np.asarray(box, dtype=float)
ink = (a < 110).mean(axis=1)                      # fraction of dark pixels per row
# smooth
k = 9; sm = np.convolve(ink, np.ones(k) / k, mode='same')
thr = max(0.008, sm.max() * float(os.environ.get('THR','0.12')))
rows = sm > thr
# find runs
lines = []; i = 0; n = len(rows)
while i < n:
    if rows[i]:
        j = i
        while j < n and rows[j]:
            j += 1
        if j - i > 25:
            lines.append((i, j))
        i = j
    else:
        i += 1
# merge lines closer than 12 px (ascender/descender splits)
merged = []
for s, e in lines:
    if merged and s - merged[-1][1] < 14:
        merged[-1] = (merged[-1][0], e)
    else:
        merged.append((s, e))
print('lines found', len(merged))
os.makedirs('strips', exist_ok=True)
per = 5; sheetno = 0; buf = []
pad = 18
for li, (s, e) in enumerate(merged, 1):
    halves = int(os.environ.get('HALVES', '1'))
    for h in range(halves):
        x0 = int(box.width * (h / halves - (0.03 if h else 0))); x1 = int(box.width * ((h + 1) / halves + (0.03 if h < halves - 1 else 0)))
        crop = box.crop((x0, max(0, s - pad), x1, min(box.height, e + pad)))
        scale = 2000 / crop.width
        crop = crop.resize((2000, max(1, int(crop.height * scale))), Image.LANCZOS)
        lab = Image.new('L', (2000, crop.height + 22), 255); lab.paste(crop, (0, 22))
        ImageDraw.Draw(lab).text((6, 4), '%s line %02d%s  (y %d-%d)' % (pref, li, ('abcd'[h] if halves > 1 else ''), s, e), fill=0)
        buf.append(lab)
    if len(buf) >= per or li == len(merged):
        Hh = sum(x.height for x in buf); S = Image.new('L', (2000, Hh), 255); y = 0
        for x in buf:
            S.paste(x, (0, y)); y += x.height
        S.save('strips/%s_s%02d.png' % (pref, sheetno)); sheetno += 1; buf = []
print('sheets', sheetno)
