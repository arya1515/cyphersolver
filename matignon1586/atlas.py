"""Cluster the segmented glyphs of a page by shape and render an atlas montage.

Features: each glyph is cropped to its ink, pasted into a square keeping aspect, blurred (so that
stroke jitter does not dominate), unit-normalised, and given a small aspect-ratio tail. Distance is
correlation, linkage average; we deliberately over-cluster, since several clusters mapping to the
same glyph costs nothing while a mixed cluster costs a lot.
"""
import numpy as np, json, sys
from PIL import Image, ImageOps, ImageDraw, ImageFilter
from scipy.cluster.hierarchy import linkage, fcluster
from seg import binarize

src, boxfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
K = int(sys.argv[4]) if len(sys.argv) > 4 else 110
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
a = np.array(im); bw = binarize(a)
boxes = json.load(open(boxfile))

S = 24
feats, crops, index = [], [], []
for li, line in enumerate(boxes):
    for gi, (x0, x1, y0, y1) in enumerate(line):
        sub = bw[y0:y1, x0:x1]
        if sub.size == 0 or sub.sum() < 4: continue
        h, w = sub.shape
        sc = (S - 4) / max(h, w)
        g = Image.fromarray((sub * 255).astype(np.uint8)).resize(
            (max(1, int(w * sc)), max(1, int(h * sc))), Image.BILINEAR)
        canv = Image.new('L', (S, S), 0)
        canv.paste(g, ((S - g.width) // 2, (S - g.height) // 2))
        canv = canv.filter(ImageFilter.GaussianBlur(1.2))
        v = np.asarray(canv, dtype=np.float32).ravel()
        v = v - v.mean()
        n = np.linalg.norm(v) or 1.0
        v = v / n
        feats.append(np.concatenate([v, [1.5 * np.log(max(w, 1) / max(h, 1))]]))
        index.append((li, gi))
        crops.append(a[max(0, y0-4):y1+4, max(0, x0-3):x1+3])
F = np.array(feats)
print('glyphs', len(F))
Z = linkage(F, method='average', metric='correlation')
lab = fcluster(Z, t=K, criterion='maxclust')
print('clusters', lab.max())
json.dump({'index': index, 'labels': lab.tolist()}, open(out + '.json', 'w'))

from collections import Counter
cnt = Counter(lab.tolist())
order = [c for c, _ in cnt.most_common()]
CH, CW, PER = 54, 42, 13
sheet = Image.new('L', (CW * PER + 96, CH * len(order)), 255)
d = ImageDraw.Draw(sheet)
for r, c in enumerate(order):
    d.text((6, CH * r + 18), f'{c}:{cnt[c]}', fill=0)
    ids = [i for i in range(len(lab)) if lab[i] == c][:PER]
    for k, i in enumerate(ids):
        g = Image.fromarray(crops[i]).convert('L')
        s = min(CW / max(g.width, 1), (CH - 6) / max(g.height, 1), 1.5)
        g = g.resize((max(1, int(g.width * s)), max(1, int(g.height * s))), Image.LANCZOS)
        sheet.paste(g, (96 + CW * k, CH * r + (CH - g.height) // 2))
sheet.save(out + '.png')
print('atlas', sheet.size)
