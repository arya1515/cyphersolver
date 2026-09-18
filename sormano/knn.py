# -*- coding: utf-8 -*-
"""k-NN glyph classifier trained on the cluster-labelled glyphs.

Features: blurred 16x22 raster + 4x4 grid of 8-bin gradient-orientation
histograms.  Labels: cipher letter from full700.json, or '~' for clear/noise.
"""
import sys, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, sobel
from pipeline import otsu
from collections import defaultdict, Counter

FW, FH = 16, 22

def glyph_feature(g, thr):
    m = (g < thr).astype(np.float32)
    m = gaussian_filter(m, 1.4)
    im2 = Image.fromarray((np.clip(m, 0, 1)*255).astype(np.uint8)).resize((FW, FH), Image.BILINEAR)
    ras = np.asarray(im2, dtype=np.float32).ravel()/255.0
    # gradient orientation histograms on a 32x44 version
    im3 = Image.fromarray((np.clip(m, 0, 1)*255).astype(np.uint8)).resize((32, 44), Image.BILINEAR)
    a = np.asarray(im3, dtype=np.float32)/255.0
    gx = sobel(a, axis=1); gy = sobel(a, axis=0)
    mag = np.hypot(gx, gy); ang = (np.arctan2(gy, gx) + np.pi) / (2*np.pi) * 8
    b = np.floor(ang).astype(int) % 8
    hog = np.zeros((4, 4, 8), dtype=np.float32)
    for yi in range(4):
        for xi in range(4):
            sub_m = mag[yi*11:(yi+1)*11, xi*8:(xi+1)*8]
            sub_b = b[yi*11:(yi+1)*11, xi*8:(xi+1)*8]
            hog[yi, xi] = np.bincount(sub_b.ravel(), weights=sub_m.ravel(), minlength=8)
    hog = hog.ravel(); hog /= (np.linalg.norm(hog) + 1e-6)
    w = min(2.2, g.shape[1]/44.0)
    return np.concatenate([ras, 1.5*hog, [w, w]])

def features(recs, pagemap):
    ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
    byline = defaultdict(list)
    for r in recs: byline[(r['page'], r['line'])].append(r)
    thr = {}
    for k, rs in byline.items():
        im = ims[k[0]]
        a = np.asarray(im.crop((min(r['x0'] for r in rs), rs[0]['y0'],
                                max(r['x1'] for r in rs), rs[0]['y1'])), dtype=np.uint8)
        thr[k] = otsu(a)
    X = np.zeros((len(recs), FW*FH+128+2), dtype=np.float32)
    for i, r in enumerate(recs):
        g = np.asarray(ims[r['page']].crop((r['x0'], r['y0'], r['x1'], r['y1'])), dtype=np.uint8)
        X[i] = glyph_feature(g, thr[(r['page'], r['line'])])
    return X

def knn_predict(Xtr, ytr, Xte, k=5, chunk=1024):
    out = []; conf = []
    n2 = (Xtr**2).sum(axis=1)
    for s in range(0, len(Xte), chunk):
        q = Xte[s:s+chunk]
        d = n2[None, :] - 2*q @ Xtr.T + (q**2).sum(axis=1)[:, None]
        idx = np.argpartition(d, k, axis=1)[:, :k]
        for row, ii in zip(d, idx):
            ii = ii[np.argsort(row[ii])]
            votes = Counter(ytr[j] for j in ii)
            lab, n = votes.most_common(1)[0]
            out.append(lab); conf.append(n/float(k))
    return np.array(out), np.array(conf)

if __name__ == '__main__':
    sp = sys.argv[1]
    L = {int(k): v for k, v in json.load(open(sp+'/full700.json')).items()}
    D = json.load(open(sp+'/clustered.json')); recs = D['recs']
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    X = features(recs, pagemap)
    np.save(sp+'/Xknn.npy', X)
    y = np.array([L.get(r['c'], '~') if r['c'] >= 0 else '~' for r in recs])
    lab = np.where(y != '?')[0]
    print('labelled', len(lab), 'letters', Counter(y[lab]).most_common(30))
    # 5-fold CV on labelled set
    rng = np.random.default_rng(0); perm = rng.permutation(lab); folds = np.array_split(perm, 5)
    correct = 0; tot = 0; confm = Counter()
    for f in range(5):
        te = folds[f]; tr = np.concatenate([folds[g] for g in range(5) if g != f])
        pred, conf = knn_predict(X[tr], y[tr], X[te])
        for t, p in zip(y[te], pred):
            tot += 1; correct += (t == p)
            if t != p: confm[(t, p)] += 1
    print('CV accuracy %.4f' % (correct/float(tot)))
    print('top confusions', confm.most_common(25))
