"""Simulated annealing over the plugboard with trigram score (alternative to hill climbing)."""
import numpy as np
from numba import njit
from solver import score_tri, nplugs_of


@njit(cache=True)
def propose(pb, cand, a, b, opt):
    """Fill cand with the plugboard after applying move (a,b,opt). Returns False if the move is invalid."""
    for q in range(26):
        cand[q] = pb[q]
    pa = pb[a]; pbb = pb[b]
    if pa == a and pbb == b:
        cand[a] = b; cand[b] = a
        return True
    if pa == b:
        cand[a] = a; cand[b] = b
        return True
    if pa == a or pbb == b:
        if pa == a:
            u = a; v = b; c = pbb
        else:
            u = b; v = a; c = pa
        if opt % 2 == 0:
            cand[c] = c; cand[u] = v; cand[v] = u
        else:
            cand[v] = v; cand[u] = c; cand[c] = u
        return True
    c = pa; d = pbb
    o = opt % 4
    if o == 0:
        cand[a] = b; cand[b] = a; cand[c] = c; cand[d] = d
    elif o == 1:
        cand[a] = b; cand[b] = a; cand[c] = d; cand[d] = c
    elif o == 2:
        cand[a] = d; cand[d] = a; cand[b] = b; cand[c] = c
    else:
        cand[a] = d; cand[d] = a; cand[b] = c; cand[c] = b
    return True


@njit(cache=True)
def anneal(S, ct, N, pb, tri, nsteps, T0, T1, maxplugs):
    """pb: start plugboard, modified in place to the best found. Returns best trigram score."""
    cand = np.empty(26, dtype=np.int64)
    best = np.empty(26, dtype=np.int64)
    cur = score_tri(S, ct, pb, N, tri)
    bests = cur
    for q in range(26):
        best[q] = pb[q]
    lr = np.log(T1 / T0)
    for step in range(nsteps):
        T = T0 * np.exp(lr * step / nsteps)
        a = np.random.randint(0, 26); b = np.random.randint(0, 26)
        if a == b: continue
        opt = np.random.randint(0, 4)
        propose(pb, cand, a, b, opt)
        if nplugs_of(cand) > maxplugs: continue
        s = score_tri(S, ct, cand, N, tri)
        if s >= cur or np.random.random() < np.exp((s - cur) / T):
            cur = s
            for q in range(26):
                pb[q] = cand[q]
            if s > bests:
                bests = s
                for q in range(26):
                    best[q] = cand[q]
    for q in range(26):
        pb[q] = best[q]
    return bests
