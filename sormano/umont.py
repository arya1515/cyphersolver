# -*- coding: utf-8 -*-
"""Montages of clusters lacking a confident label, in dendrogram order."""
import sys, os, json
from collections import defaultdict
import numpy as np
from PIL import Image, ImageDraw
from scipy.cluster.hierarchy import linkage, leaves_list
import labels

SP = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else 'todo'
D = json.load(open(os.path.join(SP, 'clustered.json')))
C = np.load(os.path.join(SP, 'C.npy'))
pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
byc = defaultdict(list)
for r in D['recs']:
    if r['c'] >= 0: byc[r['c']].append(r)
if mode == 'todo':
    sel = [c for c in byc if labels.L.get(c, '~') in ('~', '?')]
else:
    sel = list(byc)
Z = linkage(C[sel], method='average')
order = [sel[i] for i in leaves_list(Z)]
per, cell, chunk = 12, 150, 13
cols = per + 1
for ci in range(0, len(order), chunk):
    part = order[ci:ci+chunk]
    canvas = Image.new('L', (cols*cell, len(part)*cell), 245)
    d = ImageDraw.Draw(canvas)
    for ri, k in enumerate(part):
        s = sorted(byc[k], key=lambda r: r['d'])[:per]
        d.text((4, ri*cell+cell//2-10), '%d\n(%d)%s' % (k, len(byc[k]), labels.L.get(k, '')), fill=0)
        for j, r in enumerate(s):
            g = ims[r['page']].crop((r['x0']-6, r['cy']-82, r['x1']+6, r['cy']+82))
            w, h = g.size
            sc = min((cell-14)/float(w), (cell-14)/float(h))
            g = g.resize((max(1,int(w*sc)), max(1,int(h*sc))), Image.LANCZOS)
            canvas.paste(g, ((j+1)*cell+(cell-g.size[0])//2, ri*cell+(cell-g.size[1])//2))
        d.line([0, ri*cell, cols*cell, ri*cell], fill=170)
    canvas.save(os.path.join(SP, 'U_%02d.png' % (ci//chunk)))
json.dump([int(x) for x in order], open(os.path.join(SP, 'u_order.json'), 'w'))
print('chunks', (len(order)+chunk-1)//chunk, 'clusters', len(order))
