# -*- coding: utf-8 -*-
"""Feature extraction + k-means over the whole glyph inventory (per-line threshold)."""
import sys, json, os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from pipeline import otsu

FW, FH = 16, 22

def build_features(recs, pagemap):
    ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
    # threshold per (page, line)
    thr = {}
    from collections import defaultdict
    byline = defaultdict(list)
    for r in recs: byline[(r['page'], r['line'])].append(r)
    for k, rs in byline.items():
        im = ims[k[0]]
        xs = min(r['x0'] for r in rs); xe = max(r['x1'] for r in rs)
        y0 = rs[0]['y0']; y1 = rs[0]['y1']
        a = np.asarray(im.crop((xs, y0, xe, y1)), dtype=np.uint8)
        thr[k] = otsu(a)
    X = np.zeros((len(recs), FW*FH+2), dtype=np.float32)
    keep = []
    for i, r in enumerate(recs):
        g = np.asarray(ims[r['page']].crop((r['x0'], r['y0'], r['x1'], r['y1'])),
                       dtype=np.uint8)
        m = (g < thr[(r['page'], r['line'])]).astype(np.float32)
        r['ink'] = int(m.sum())
        m = gaussian_filter(m, 1.6)
        im2 = Image.fromarray((np.clip(m, 0, 1)*255).astype(np.uint8)).resize((FW, FH), Image.BILINEAR)
        v = np.asarray(im2, dtype=np.float32).ravel()/255.0
        X[i, :FW*FH] = v
        X[i, -2] = min(2.2, (r['x1']-r['x0'])/44.0)
        X[i, -1] = min(2.0, r['ink']/900.0)
        if r['ink'] >= 45 and (r['x1']-r['x0']) >= 11: keep.append(i)
    return X, thr, np.array(keep)

def kmeans(X, k, iters=60, seed=0):
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    idx = rng.choice(n, k, replace=False)
    C = X[idx].copy(); lab = np.zeros(n, dtype=np.int32)
    for it in range(iters):
        for s in range(0, n, 4096):
            e = min(n, s+4096)
            d = ((X[s:e, None, :] - C[None, :, :])**2).sum(axis=2)
            lab[s:e] = d.argmin(axis=1)
        newC = np.zeros_like(C); cnt = np.bincount(lab, minlength=k)
        np.add.at(newC, lab, X)
        for j in range(k):
            if cnt[j] > 0: newC[j] /= cnt[j]
            else: newC[j] = X[rng.integers(n)]
        shift = np.abs(newC-C).max(); C = newC
        if shift < 1e-4: break
    print('kmeans done it=%d shift=%.5f' % (it, shift), flush=True)
    return lab, C

def thr_ser(thr):
    return {'%s|%d' % k: int(v) for k, v in thr.items()}

if __name__ == '__main__':
    inv = sys.argv[1]; outdir = sys.argv[2]; k = int(sys.argv[3])
    D = json.load(open(inv)); recs = D['recs']
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    X, thr, keep = build_features(recs, pagemap)
    print('features', X.shape, 'keep', len(keep), flush=True)
    ks = set(keep.tolist())
    for i, r in enumerate(recs):
        if i not in ks: r['c'] = -1; r['d'] = 0.0
    recs_k = [recs[i] for i in keep]; Xk = X[keep]
    Xm = Xk - Xk.mean(axis=0)
    samp = np.random.default_rng(1).choice(len(Xk), 6000, replace=False)
    U, S, Vt = np.linalg.svd(Xm[samp], full_matrices=False)
    P = Vt[:70].T
    Z = (Xm @ P).astype(np.float32)
    lab, C = kmeans(Z, k)
    for r, l in zip(recs_k, lab): r['c'] = int(l)
    d = np.linalg.norm(Z - C[lab], axis=1)
    for r, dd in zip(recs_k, d): r['d'] = float(dd)
    json.dump(dict(recs=recs, bands=D['bands']), open(os.path.join(outdir,'clustered.json'), 'w'))
    np.save(os.path.join(outdir,'Z.npy'), Z); np.save(os.path.join(outdir,'C.npy'), C)
    np.save(os.path.join(outdir,'keep.npy'), keep)
    np.save(os.path.join(outdir,'P.npy'), P)
    np.save(os.path.join(outdir,'mean.npy'), Xk.mean(axis=0))
    json.dump(thr_ser(thr), open(os.path.join(outdir,'thr.json'),'w'))
    json.dump([int(i) for i in keep], open(os.path.join(outdir,'keep.json'),'w'))
    print('done', flush=True)
