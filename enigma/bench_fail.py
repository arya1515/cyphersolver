"""Which additional climb variants rescue the controls that the 26 E-start pipeline misses?"""
import sys, time, numpy as np
from solver import *
from climb2 import climb2
from sa import anneal, propose
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
NST = x_starts('N'); XST = x_starts('X'); RST = x_starts('R')
sfA = np.array([0, 4, 8]); smA = np.array([0, 2, 3])
sfS = np.array([0, 5]); smS = np.array([0, 3])
rng = np.random.default_rng(5)
np.random.seed(5)

def run_starts(S, ct, starts, sf, sm, bf, steep):
    best = -1e9; bpb = None
    for k in range(starts.shape[0]):
        pbk = starts[k].copy()
        s = climb2(S, ct, N, pbk, sf, sm, bf, steep, mono, bi, tri)
        if s > best: best = s; bpb = pbk.copy()
    return best, bpb

def ils(S, ct, pb0, rounds):
    """perturb best-so-far (remove 2 plugs, add 1 random) and re-climb with trigram-only."""
    best = score_tri(S, ct, pb0, N, tri); cur = pb0.copy()
    for r in range(rounds):
        pbk = cur.copy()
        plugged = [a for a in range(26) if pbk[a] > a]
        for a in rng.choice(plugged, min(2, len(plugged)), replace=False):
            b = pbk[a]; pbk[a] = a; pbk[b] = b
        free = [a for a in range(26) if pbk[a] == a]
        if len(free) >= 2:
            a, b = rng.choice(free, 2, replace=False); pbk[a] = b; pbk[b] = a
        s = climb2(S, ct, N, pbk, np.array([0]), np.array([3]), 0, False, mono, bi, tri)
        if s > best: best = s; cur = pbk.copy()
    return best

variants = ['A:E-first', 'S:E-steep', 'N:N-first', 'X:X-first', 'R:R-first', 'ILS10', 'SA2', 'S2:E-steep-ic4bi']
solved = {v: 0 for v in variants}; tm = {v: 0.0 for v in variants}
rows = []
for name, order, ct, l, m, r, i0, pb in controls:
    if order not in tables: tables[order] = build_table(order)
    S = np.empty((N, 26), dtype=np.int64); make_S(tables[order], l, m, r, i0, -1, N, S)
    ts = score_tri(S, ct, pb, N, tri)
    res = {}
    t = time.time(); sA, pbA = run_starts(S, ct, E, sfA, smA, 5, False); tm['A:E-first'] += time.time() - t; res['A:E-first'] = sA
    t = time.time(); sS, _ = run_starts(S, ct, E, sfS, smS, 3, True); tm['S:E-steep'] += time.time() - t; res['S:E-steep'] = sS
    t = time.time(); sN, _ = run_starts(S, ct, NST, sfA, smA, 5, False); tm['N:N-first'] += time.time() - t; res['N:N-first'] = sN
    t = time.time(); sX, _ = run_starts(S, ct, XST, sfA, smA, 5, False); tm['X:X-first'] += time.time() - t; res['X:X-first'] = sX
    t = time.time(); sR, _ = run_starts(S, ct, RST, sfA, smA, 5, False); tm['R:R-first'] += time.time() - t; res['R:R-first'] = sR
    t = time.time(); sI = ils(S, ct, pbA, 10); tm['ILS10'] += time.time() - t; res['ILS10'] = sI
    t = time.time(); sSA = -1e9
    for rep in range(2):
        pbk = np.arange(26); sSA = max(sSA, anneal(S, ct, N, pbk, tri, 20000, 25.0, 1.0, 13))
    tm['SA2'] += time.time() - t; res['SA2'] = sSA
    t = time.time(); sS2, _ = run_starts(S, ct, E, sfA, smA, 4, True); tm['S2:E-steep-ic4bi'] += time.time() - t; res['S2:E-steep-ic4bi'] = sS2
    ok = {v: res[v] >= ts - 1e-6 for v in variants}
    for v in variants: solved[v] += ok[v]
    rows.append(ok)
    print('%-5s true %5.0f ' % (name, ts) + ' '.join('%s%s' % (v.split(':')[0], '+' if ok[v] else '-') for v in variants), flush=True)
n = len(controls)
print()
for v in variants:
    print('%-18s %2d/%d  %.1f ms' % (v, solved[v], n, 1000 * tm[v] / n))
import itertools
print('union A+S:', sum(r['A:E-first'] or r['S:E-steep'] for r in rows))
print('union A+N:', sum(r['A:E-first'] or r['N:N-first'] for r in rows))
print('union A+S+N:', sum(r['A:E-first'] or r['S:E-steep'] or r['N:N-first'] for r in rows))
print('union A+S+N+X:', sum(r['A:E-first'] or r['S:E-steep'] or r['N:N-first'] or r['X:X-first'] for r in rows))
print('union all:', sum(any(r.values()) for r in rows))
