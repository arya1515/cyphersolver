# -*- coding: utf-8 -*-
"""Leave-one-out k-NN prediction for every glyph + line-wise cipher/clear smoothing."""
import sys, json
import numpy as np
from collections import Counter, defaultdict

def loo_predict(X, y, lab, k=6, chunk=768):
    """Predict all rows of X from the labelled rows `lab`, excluding self."""
    Xtr = X[lab]; ytr = y[lab]; n2 = (Xtr**2).sum(axis=1)
    pos = {int(i): j for j, i in enumerate(lab)}
    pred = np.empty(len(X), dtype=object); conf = np.zeros(len(X))
    for s in range(0, len(X), chunk):
        q = X[s:s+chunk]
        d = n2[None, :] - 2*q @ Xtr.T + (q**2).sum(axis=1)[:, None]
        idx = np.argpartition(d, k+1, axis=1)[:, :k+1]
        for t, (row, ii) in enumerate(zip(d, idx)):
            i = s+t
            ii = ii[np.argsort(row[ii])]
            if i in pos: ii = [j for j in ii if j != pos[i]]
            ii = ii[:k]
            votes = Counter(ytr[j] for j in ii)
            l, n = votes.most_common(1)[0]
            pred[i] = l; conf[i] = n/float(k)
    return pred, conf

def smooth(recs):
    """Mark each glyph cipher/clear by majority in a 5-glyph window, then
    demote isolated letters inside clear runs and promote isolated '~' inside
    cipher runs (using the k-NN's second choice is not stored; we fall back
    to marking them '?')."""
    byline = defaultdict(list)
    for i, r in enumerate(recs): byline[(r['page'], r['line'])].append(i)
    for key, idxs in byline.items():
        idxs.sort(key=lambda i: recs[i]['x0'])
        n = len(idxs)
        isc = [recs[i]['let'] != '~' for i in idxs]
        sm = []
        for p in range(n):
            w = isc[max(0, p-2):p+3]
            sm.append(sum(w) >= (len(w)+1)//2)
        for p, i in enumerate(idxs):
            r = recs[i]
            if isc[p] and not sm[p] and r['conf'] < 0.85:
                r['let2'] = '~'
            elif (not isc[p]) and sm[p]:
                r['let2'] = '?'
            else:
                r['let2'] = r['let']

if __name__ == '__main__':
    sp = sys.argv[1]
    L = {int(k): v for k, v in json.load(open(sp+'/full700.json')).items()}
    D = json.load(open(sp+'/clustered.json')); recs = D['recs']
    X = np.load(sp+'/Xknn.npy')
    y = np.array([L.get(r['c'], '~') if r['c'] >= 0 else '~' for r in recs], dtype=object)
    import os
    if os.path.exists(sp+'/overrides.json'):
        for i, v in json.load(open(sp+'/overrides.json')).items(): y[int(i)] = v
    lab = np.where(y != '?')[0]
    pred, conf = loo_predict(X, y, lab)
    for r, p, c in zip(recs, pred, conf):
        r['let'] = str(p); r['conf'] = float(c)
    smooth(recs)
    json.dump(D, open(sp+'/knn.json', 'w'))
    print('decoded', sum(1 for r in recs if r['let2'] not in '~?'),
          'unsure', sum(1 for r in recs if r['let2'] == '?'))
