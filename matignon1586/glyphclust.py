"""Cluster segmented glyphs into figure classes and emit the page as a sequence of cluster ids.
This replaces reading the figures by eye: the solver then works on what the scribe actually wrote,
not on my names for his shapes.   python glyphclust.py <glyphs.npz> <out.txt> [k] [restarts]"""
import sys
import numpy as np
d = np.load(sys.argv[1])
G, rows = d['G'], d['rows']
out = sys.argv[2]
k = int(sys.argv[3]) if len(sys.argv) > 3 else 45
restarts = int(sys.argv[4]) if len(sys.argv) > 4 else 6
X = G/np.linalg.norm(G, axis=1, keepdims=True)
rng = np.random.default_rng(0)
best = None
for r in range(restarts):
    # k-means++ style seeding on cosine distance
    idx = [rng.integers(len(X))]
    d2 = 1 - X @ X[idx[0]]
    for _ in range(k-1):
        p = np.maximum(d2, 0)**2
        if p.sum() <= 0: p = np.ones(len(X))
        i = rng.choice(len(X), p=p/p.sum())
        idx.append(i)
        d2 = np.minimum(d2, 1 - X @ X[i])
    C = X[idx].copy()
    for it in range(60):
        S = X @ C.T
        lab = S.argmax(axis=1)
        newC = np.zeros_like(C)
        for j in range(k):
            m = lab == j
            if m.sum(): newC[j] = X[m].mean(axis=0)
            else: newC[j] = X[rng.integers(len(X))]
        newC /= np.linalg.norm(newC, axis=1, keepdims=True)+1e-9
        if np.allclose(newC, C, atol=1e-5): C = newC; break
        C = newC
    inertia = (X * C[lab]).sum()
    if best is None or inertia > best[0]: best = (inertia, lab.copy(), C.copy())
inertia, lab, C = best
lines = {}
for g, r in enumerate(rows): lines.setdefault(int(r), []).append(int(lab[g]))
with open(out, 'w') as fh:
    for r in sorted(lines): fh.write(' '.join(f'c{c}' for c in lines[r])+'\n')
sizes = np.bincount(lab, minlength=k)
print(f'k={k}  mean cosine to centroid {inertia/len(X):.3f}')
print('cluster sizes:', ' '.join(str(s) for s in sorted(sizes, reverse=True)))
