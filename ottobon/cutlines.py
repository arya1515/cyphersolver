"""Cut a cleaned page into single text lines (peak detection on the row-ink profile) and save each line
as two overlapping halves at 3x: img/lines/<page>_lNN_a.png / _b.png. Usage: python cutlines.py p030_R 170 1070"""
import sys, os
from PIL import Image
import numpy as np
pg, x0, x1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
os.makedirs('img/lines', exist_ok=True)
im = Image.open('img/%s_clean.png' % pg); a = np.array(im)
rows = (a < 100)[:, x0:x1].sum(1).astype(float)
sm = np.convolve(rows, np.ones(9) / 9, mode='same')
peaks = []
for y in range(30, len(sm) - 30):
    if sm[y] == sm[y - 22:y + 23].max() and sm[y] > 60:
        if not peaks or y - peaks[-1] > 40: peaks.append(y)
print(pg, len(peaks), peaks)
for i, y in enumerate(peaks):
    c = im.crop((x0, max(y - 38, 0), x1, min(y + 38, a.shape[0]))); w = c.width
    for h, (xa, xb) in enumerate([(0, w // 2 + 60), (w // 2 - 60, w)]):
        cc = c.crop((xa, 0, xb, c.height)).resize(((xb - xa) * 3, c.height * 3), Image.LANCZOS)
        cc.save('img/lines/%s_l%02d_%s.png' % (pg, i + 1, 'ab'[h]))
