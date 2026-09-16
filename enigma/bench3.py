"""Check climb3 == climb2 results and speed; pipeline success with E+N starts and ILS."""
import sys, time, numpy as np
from solver import *
from climb2 import climb2
from climb3 import climb3, ils3
from controls import make_controls

mono = np.load('mono_logp.npy'); bi = np.load('bi_logp.npy'); tri = np.load('tri_logp.npy')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
controls = make_controls(N, nsyn=40, seed=7)
tables = {}
E = e_stecker_starts()
def x_starts(letter):
    st = np.tile(np.arange(26), (25, 1)); e = A.index(letter); j = 0
    for k in range(26):
        if k != e:
            st[j, e] = k; st[j, k] = e; j += 1
    return st.astype(np.int64)
NST = x_starts('N'); XST = x_starts('X')
sf = np.array([0, 4, 8]); sm = np.array([0, 2, 3])
sf3 = np.array([0]); sm3 = np.array([3])
W = np.zeros(8 * N + 200, dtype=np.int64)
np.random.seed(5)
agree = 0; tot = 0; t2 = 0.0; t3 = 0.0
res = {'E': 0, 'E+ILS10': 0, 'E+N': 0, 'E+N+ILS10': 0, 'E+N+X+ILS20': 0}; tm = {k: 0.0 for k in res}
for name, order, ct, l, m, r, i0, pb in controls:
    if order not in tables: tables[order] = build_table(order)
    S = np.empty((N, 26), dtype=np.int64); make_S(tables[order], l, m, r, i0, -1, N, S)
    ts = score_tri(S, ct, pb, N, tri)
    # agreement check on 26 E starts
    for k in range(26):
        p2 = E[k].copy(); t = time.time(); s2 = climb2(S, ct, N, p2, sf, sm, 5, False, mono, bi, tri); t2 += time.time() - t
        p3 = E[k].copy(); t = time.time(); s3 = climb3(S, ct, N, p3, sf, sm, 5, bi, tri, W); t3 += time.time() - t
        tot += 1; agree += abs(s2 - s3) < 1e-6
    def run(starts):
        best = -1e9; bp = None
        for k in range(starts.shape[0]):
            pk = starts[k].copy(); s = climb3(S, ct, N, pk, sf, sm, 5, bi, tri, W)
            if s > best: best = s; bp = pk.copy()
        return best, bp
    t = time.time(); sE, pE = run(E); tE = time.time() - t
    t = time.time(); pI = pE.copy(); sI = ils3(S, ct, N, pI, 10, bi, tri, W, sf3, sm3); tI = time.time() - t
    t = time.time(); sN, pN = run(NST); tN = time.time() - t
    bestEN = max(sE, sN); pEN = pE if sE >= sN else pN
    t = time.time(); pI2 = pEN.copy(); sI2 = ils3(S, ct, N, pI2, 10, bi, tri, W, sf3, sm3); tI2 = time.time() - t
    t = time.time(); sX, pX = run(XST); tX = time.time() - t
    cands = [(sE, pE), (sN, pN), (sX, pX)]; sB, pB = max(cands, key=lambda x: x[0])
    t = time.time(); pI3 = pB.copy(); sI3 = ils3(S, ct, N, pI3, 20, bi, tri, W, sf3, sm3); tI3 = time.time() - t
    ok = {'E': sE, 'E+ILS10': max(sE, sI), 'E+N': bestEN, 'E+N+ILS10': max(bestEN, sI2), 'E+N+X+ILS20': max(sB, sI3)}
    tms = {'E': tE, 'E+ILS10': tE + tI, 'E+N': tE + tN, 'E+N+ILS10': tE + tN + tI2, 'E+N+X+ILS20': tE + tN + tX + tI3}
    for k in res:
        res[k] += ok[k] >= ts - 1e-6; tm[k] += tms[k]
    print('%-5s true %5.0f ' % (name, ts) + ' '.join('%s:%s' % (k, '+' if ok[k] >= ts - 1e-6 else '-') for k in res), flush=True)
print('climb2 vs climb3 agreement: %d/%d; time climb2 %.2f ms, climb3 %.2f ms per start' % (agree, tot, 1000 * t2 / tot, 1000 * t3 / tot))
n = len(controls)
for k in res:
    print('%-14s %2d/%d  %.1f ms/location' % (k, res[k], n, 1000 * tm[k] / n))
