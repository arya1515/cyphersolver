# cut a page region into text lines (projection profile), enhance, save 2 halves per line at 2x
import sys, numpy as np
from PIL import Image, ImageFilter
img, x0, x1, y0, y1, out = sys.argv[1], *map(float, sys.argv[2:6]), sys.argv[6]
im = Image.open(img).convert('L'); W, H = im.size
X0, X1, Y0, Y1 = int(W*x0), int(W*x1), int(H*y0), int(H*y1)
r = im.crop((X0, Y0, X1, Y1))
a = np.asarray(r).astype(float); bg = np.asarray(r.filter(ImageFilter.GaussianBlur(20))).astype(float)
d = np.clip((a-bg)*3+255, 0, 255)
ink = (d < 150).sum(1); sm = np.convolve(ink, np.ones(15)/15, 'same')
thr = np.percentile(sm,20)+ (sm.max()-np.percentile(sm,20))*0.25; rows = []; inrow = False
for i, v in enumerate(sm):
    if v > thr and not inrow: s = i; inrow = True
    elif v <= thr and inrow:
        if i - s > 8: rows.append((s, i))
        inrow = False
D = Image.fromarray(d.astype('uint8'))
for k, (s, e) in enumerate(rows):
    c = (s+e)//2; h = max(e-s, 40)
    L = D.crop((0, max(0, c-int(h*1.1)), D.size[0], c+int(h*1.1)))
    w = L.size[0]
    for j, (u, v) in enumerate([(0, w//2+40), (w//2-40, w)]):
        p = L.crop((u, 0, v, L.size[1])); p = p.resize((p.size[0]*2, p.size[1]*2)); p.save(f'{out}_{k:02d}{"ab"[j]}.jpg')
print(len(rows), rows)
