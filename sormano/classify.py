# -*- coding: utf-8 -*-
"""Supervised glyph classifier for the Sormano hand.

Records come from inv.json (x-segmentation) but are re-cropped on a baseline
window computed per line, which the original extraction got wrong. Training
labels come from the hand-labelled clusters in labels.py; the classifier is
k-NN in a PCA space, scored on a held-out split.

python classify.py SPDIR [k] [--pred out.json]
"""
import sys, os, json
from collections import defaultdict, Counter
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from pipeline import otsu
import labels

FW, FH = 18, 26

def line_window(im, rs):
    """x-height band for a line, from the row ink profile of its own glyphs."""
    cy = sorted(r['cy'] for r in rs)[len(rs)//2]
    xs = min(r['x0'] for r in rs); xe = max(r['x1'] for r in rs)
    a = np.asarray(im.crop((xs, cy-70, xe, cy+70)), dtype=np.uint8)
    prof = (a < otsu(a)).sum(axis=1).astype(float)
    k = np.ones(5)/5.0
    prof = np.convolve(prof, k, mode='same')
    m = prof.max()
    on = np.where(prof > m*0.45)[0]
    if len(on) < 4: return cy-58, cy+62
    top, bot = on[0]-70, on[-1]-70          # relative to cy
    xh = max(18, bot-top)
    return int(cy+top-0.85*xh), int(cy+bot+0.85*xh)

def features(SP):
    D = json.load(open(os.path.join(SP, 'inv.json')))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
    recs = D['recs']
    byline = defaultdict(list)
    for r in recs: byline[(r['page'], r['line'])].append(r)
    win, thr = {}, {}
    for kk, rs in byline.items():
        im = ims[kk[0]]
        win[kk] = line_window(im, rs)
        y0, y1 = win[kk]
        xs = min(r['x0'] for r in rs); xe = max(r['x1'] for r in rs)
        thr[kk] = otsu(np.asarray(im.crop((xs, y0, xe, y1)), dtype=np.uint8))
    X = np.zeros((len(recs), FW*FH+3), dtype=np.float32)
    for i, r in enumerate(recs):
        kk = (r['page'], r['line'])
        y0, y1 = win[kk]
        g = np.asarray(ims[r['page']].crop((r['x0'], y0, r['x1'], y1)), dtype=np.uint8)
        m = (g < thr[kk]).astype(np.float32)
        r['ink'] = int(m.sum())
        m = gaussian_filter(m, 1.2)
        im2 = Image.fromarray((np.clip(m, 0, 1)*255).astype(np.uint8)).resize((FW, FH), Image.BILINEAR)
        X[i, :FW*FH] = np.asarray(im2, dtype=np.float32).ravel()/255.0
        X[i, -3] = min(2.2, (r['x1']-r['x0'])/44.0)
        X[i, -2] = min(2.0, r['ink']/900.0)
        X[i, -1] = min(2.0, (y1-y0)/130.0)
    return recs, X, win

def main():
    SP = sys.argv[1]
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    recs, X, win = features(SP)
    C = json.load(open(os.path.join(SP, 'clustered.json')))['recs']
    assert len(C) == len(recs)
    lab = []
    for i, r in enumerate(recs):
        c = C[i]['c']
        ch = labels.L.get(c, None) if c >= 0 else None
        lab.append(ch if ch not in (None, '?', '~') else None)
    idx = np.array([i for i, l in enumerate(lab) if l is not None])
    y = np.array([lab[i] for i in idx])
    print('labelled', len(idx), 'of', len(recs), 'classes', len(set(y)))
    Xm = X - X.mean(axis=0)
    rng = np.random.default_rng(7)
    samp = rng.choice(len(X), min(6000, len(X)), replace=False)
    U, S, Vt = np.linalg.svd(Xm[samp], full_matrices=False)
    P = Vt[:60].T
    Z = (Xm @ P).astype(np.float32)
    perm = rng.permutation(len(idx))
    ntest = len(idx)//5
    te, tr = idx[perm[:ntest]], idx[perm[ntest:]]
    yte = np.array([lab[i] for i in te]); ytr = np.array([lab[i] for i in tr])
    def knn(q, Ztr, ytr, k):
        out = []
        for s in range(0, len(q), 512):
            d = ((Z[q[s:s+512]][:, None, :] - Ztr[None, :, :])**2).sum(axis=2)
            nn = np.argpartition(d, k, axis=1)[:, :k]
            for row, ids in zip(range(len(nn)), nn):
                dd = d[row, ids]
                w = 1.0/(dd+1e-6)
                sc = defaultdict(float)
                for j, wj in zip(ids, w): sc[ytr[j]] += wj
                out.append(max(sc, key=sc.get))
        return np.array(out)
    pred = knn(te, Z[tr], ytr, K)
    acc = (pred == yte).mean()
    print('held-out accuracy %.3f (k=%d)' % (acc, K))
    conf = Counter((a, b) for a, b in zip(yte, pred) if a != b)
    print('top confusions:', conf.most_common(12))
    allpred = knn(np.arange(len(recs)), Z[idx], y, K)
    json.dump([str(p) for p in allpred], open(os.path.join(SP, 'pred.json'), 'w'))
    print('wrote pred.json')

if __name__ == '__main__':
    main()
