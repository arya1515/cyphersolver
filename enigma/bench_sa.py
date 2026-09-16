"""SA vs hill climb: per-run success at the true location on the 12 controls."""
import sys, time, numpy as np
from solver import *
from controls import make_controls, nplugs_correct
from sa import anneal

tri = np.load('tri_logp.npy')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
controls = make_controls(N)
tables = {}
np.random.seed(3)
settings = [(20000, 12.0, 0.5), (40000, 12.0, 0.5), (20000, 25.0, 1.0), (60000, 15.0, 0.3)]
print('control  ' + '  '.join('steps=%d T=%g-%g' % s for s in settings), flush=True)
tot = {s: [0, 0.0] for s in settings}
for name, order, ct, l, m, r, i0, pb in controls:
    if order not in tables: tables[order] = build_table(order)
    S = np.empty((N, 26), dtype=np.int64); make_S(tables[order], l, m, r, i0, -1, N, S)
    ts = score_tri(S, ct, pb, N, tri)
    row = []
    for s in settings:
        ok = 0; R = 8; t = time.time()
        for rep in range(R):
            pbk = np.arange(26)
            sc_ = anneal(S, ct, N, pbk, tri, s[0], s[1], s[2], 13)
            if sc_ >= ts - 1e-6: ok += 1
        dt = (time.time() - t) / R
        tot[s][0] += ok; tot[s][1] += dt
        row.append('%d/%d (%.1fms)' % (ok, R, 1000 * dt))
    print('%-6s ' % name + '  '.join('%18s' % x for x in row), flush=True)
print('TOTAL  ' + '  '.join('%18s' % ('%d/96 (%.1fms)' % (tot[s][0], 1000 * tot[s][1] / len(controls))) for s in settings))
