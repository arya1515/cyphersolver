"""Pipeline success on many controls at the true location: (A) 26 E-starts; (B) A + 2 SA runs; (C) 3 SA runs."""
import sys, time, numpy as np
from solver import *
from climb2 import climb2
from sa import anneal
from controls import make_controls

mono = np.load('mono_logp.npy'); bi = np.load('bi_logp.npy'); tri = np.load('tri_logp.npy')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
controls = make_controls(N, nsyn=int(sys.argv[2]) if len(sys.argv) > 2 else 40, seed=7)
tables = {}
starts = e_stecker_starts()
sf = np.array([0, 4, 8]); sm = np.array([0, 2, 3])
np.random.seed(11)
res = {'A': 0, 'B': 0, 'C': 0}; tm = {'A': 0.0, 'B': 0.0, 'C': 0.0}
fails = {'A': [], 'B': [], 'C': []}
for name, order, ct, l, m, r, i0, pb in controls:
    if order not in tables: tables[order] = build_table(order)
    S = np.empty((N, 26), dtype=np.int64); make_S(tables[order], l, m, r, i0, -1, N, S)
    ts = score_tri(S, ct, pb, N, tri)
    t = time.time(); bestA = -1e9
    for k in range(26):
        pbk = starts[k].copy()
        bestA = max(bestA, climb2(S, ct, N, pbk, sf, sm, 5, False, mono, bi, tri))
    tA = time.time() - t
    t = time.time(); bestS2 = -1e9
    for rep in range(2):
        pbk = np.arange(26); bestS2 = max(bestS2, anneal(S, ct, N, pbk, tri, 20000, 25.0, 1.0, 13))
    tS2 = time.time() - t
    t = time.time(); pbk = np.arange(26); bestS3 = max(bestS2, anneal(S, ct, N, pbk, tri, 20000, 25.0, 1.0, 13)); tS3 = time.time() - t
    okA = bestA >= ts - 1e-6; okB = max(bestA, bestS2) >= ts - 1e-6; okC = bestS3 >= ts - 1e-6
    res['A'] += okA; res['B'] += okB; res['C'] += okC
    tm['A'] += tA; tm['B'] += tA + tS2; tm['C'] += tS2 + tS3
    for kk, ok in (('A', okA), ('B', okB), ('C', okC)):
        if not ok: fails[kk].append(name)
    print('%-5s true %.0f  A %.0f  SA2 %.0f  SA3 %.0f' % (name, ts, bestA, bestS2, bestS3), flush=True)
n = len(controls)
for k in 'ABC':
    print('%s: %d/%d solved, %.1f ms/location, fails %s' % (k, res[k], n, 1000 * tm[k] / n, fails[k]))
