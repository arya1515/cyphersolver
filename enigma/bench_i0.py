"""Tolerance to a wrong middle-step index i0: at the true (l,m,r) with i0 offset by d, run 26 E-starts
(ic4-bi-tri8) and report the max number of correct plugs recovered and the best score."""
import sys, time, numpy as np
from solver import *
from climb2 import climb2
from controls import make_controls, nplugs_correct

mono = np.load('mono_logp.npy'); bi = np.load('bi_logp.npy'); tri = np.load('tri_logp.npy')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
controls = make_controls(N)
tables = {}
starts = e_stecker_starts()
sf = np.array([0, 4, 8]); sm = np.array([0, 2, 3])
offs = [0, 1, -1, 2, -2, 3, -3, 5]
print('control ' + ' '.join('%8s' % ('d=%+d' % d) for d in offs), flush=True)
for name, order, ct, l, m, r, i0, pb in controls:
    if order not in tables: tables[order] = build_table(order)
    row = []
    for d in offs:
        i0d = i0 + d
        if i0d < 1 or i0d > 26:
            row.append('   -    '); continue
        S = np.empty((N, 26), dtype=np.int64); make_S(tables[order], l, m, r, i0d, -1, N, S)
        bestc = 0; bests = -1e9
        for k in range(26):
            pbk = starts[k].copy()
            s = climb2(S, ct, N, pbk, sf, sm, 5, False, mono, bi, tri)
            c = nplugs_correct(pbk, pb)
            if s > bests: bests = s; bestc_at = c
            bestc = max(bestc, c)
        row.append('%2d/%2d %4.0f' % (bestc, bestc_at, bests))
    print('%-7s ' % name + ' '.join(row), flush=True)
