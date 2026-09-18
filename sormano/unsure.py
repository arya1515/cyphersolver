# -*- coding: utf-8 -*-
"""Cluster the glyphs still unsure after k-NN and montage them for labelling."""
import sys, json, os
import numpy as np
from PIL import Image, ImageDraw
from collections import defaultdict
from cluster import kmeans

sp = sys.argv[1]; k = int(sys.argv[2]); field = sys.argv[3] if len(sys.argv) > 3 else 'let2'
D = json.load(open(sp+'/knn.json')); recs = D['recs']
X = np.load(sp+'/Xknn.npy')
idx = np.array([i for i, r in enumerate(recs) if r[field] == '?'])
print('unsure', len(idx))
lab, C = kmeans(X[idx], k, iters=40, seed=3)
d = np.linalg.norm(X[idx] - C[lab], axis=1)
pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
byc = defaultdict(list)
for i, l, dd in zip(idx, lab, d): byc[int(l)].append((float(dd), int(i)))
keys = sorted(byc, key=lambda c: -len(byc[c]))
per, cell, chunk = 11, 150, 13; cols = per+1
for ci in range(0, len(keys), chunk):
    part = keys[ci:ci+chunk]
    canvas = Image.new('L', (cols*cell, len(part)*cell), 245); dr = ImageDraw.Draw(canvas)
    for ri, c in enumerate(part):
        sel = [i for _, i in sorted(byc[c])[:per]]
        dr.text((4, ri*cell+cell//2-6), 'u%d(%d)' % (c, len(byc[c])), fill=0)
        for j, i in enumerate(sel):
            r = recs[i]
            g = ims[r['page']].crop((r['x0'], r['y0'], r['x1'], r['y1'])); w, h = g.size
            s = min((cell-14)/float(w), (cell-14)/float(h))
            g = g.resize((max(1, int(w*s)), max(1, int(h*s))), Image.LANCZOS)
            canvas.paste(g, ((j+1)*cell+(cell-g.size[0])//2, ri*cell+(cell-g.size[1])//2))
        dr.line([0, ri*cell, cols*cell, ri*cell], fill=170)
    canvas.save(sp+'/UN_%02d.png' % (ci//chunk))
json.dump({str(int(i)): int(l) for i, l in zip(idx, lab)}, open(sp+'/unsure_lab.json', 'w'))
print('chunks', (len(keys)+chunk-1)//chunk)
