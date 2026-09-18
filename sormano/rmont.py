# -*- coding: utf-8 -*-
"""Montages of the clusters still needing a label, in dendrogram order."""
import sys, os, json
from collections import defaultdict
import numpy as np
from PIL import Image, ImageDraw
from scipy.cluster.hierarchy import linkage, leaves_list

SP = sys.argv[1]
D = json.load(open(SP+'/clustered.json'))
C = np.load(SP+'/C.npy')
auto = {int(k): v for k, v in json.load(open(SP+'/auto700.json')).items()}
review = [t[0] for t in json.load(open(SP+'/review700.json'))]
pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
byc = defaultdict(list)
for r in D['recs']:
    if r['c'] >= 0: byc[r['c']].append(r)
sel = [c for c in review if c in byc]
Z = linkage(C[sel], method='average')
order = [sel[i] for i in leaves_list(Z)]
per, cell, chunk = 11, 150, 13
cols = per+1
for ci in range(0, len(order), chunk):
    part = order[ci:ci+chunk]
    canvas = Image.new('L', (cols*cell, len(part)*cell), 245)
    d = ImageDraw.Draw(canvas)
    for ri, k in enumerate(part):
        s = sorted(byc[k], key=lambda r: r['d'])[:per]
        d.text((4, ri*cell+cell//2-6), '%d(%d)' % (k, len(byc[k])), fill=0)
        for j, r in enumerate(s):
            g = ims[r['page']].crop((r['x0'], r['y0'], r['x1'], r['y1']))
            w, h = g.size
            sc = min((cell-14)/float(w), (cell-14)/float(h))
            g = g.resize((max(1,int(w*sc)), max(1,int(h*sc))), Image.LANCZOS)
            canvas.paste(g, ((j+1)*cell+(cell-g.size[0])//2, ri*cell+(cell-g.size[1])//2))
        d.line([0, ri*cell, cols*cell, ri*cell], fill=170)
    canvas.save(SP+'/RV_%02d.png' % (ci//chunk))
json.dump([int(x) for x in order], open(SP+'/rv_order.json','w'))
print('chunks', (len(order)+chunk-1)//chunk, 'clusters', len(order))
