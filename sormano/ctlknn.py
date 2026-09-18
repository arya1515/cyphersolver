# -*- coding: utf-8 -*-
"""Classify the control page with the k-NN model and print decoded lines."""
import sys, json
import numpy as np
from collections import defaultdict
from knn import features, knn_predict
sp = sys.argv[1]
L = {int(k): v for k, v in json.load(open(sp+'/full700.json')).items()}
D = json.load(open(sp+'/clustered.json')); recs = D['recs']
X = np.load(sp+'/Xknn.npy')
y = np.array([L.get(r['c'], '~') if r['c'] >= 0 else '~' for r in recs], dtype=object)
for i, v in json.load(open(sp+'/overrides.json')).items(): y[int(i)] = v
lab = np.where(y != '?')[0]
C = json.load(open(sp+'/ctl.json')); crecs = C['recs']
Xc = features(crecs, {'ctl_113r': 'raw/full117.jpg'})
pred, conf = knn_predict(X[lab], y[lab], Xc, k=6)
byline = defaultdict(list)
for r, p in zip(crecs, pred): r['let'] = str(p); byline[r['line']].append(r)
for k in sorted(byline):
    rs = sorted(byline[k], key=lambda r: r['x0'])
    print('L%02d %s' % (k, ''.join('.' if r['let'] == '~' else r['let'] for r in rs)))
