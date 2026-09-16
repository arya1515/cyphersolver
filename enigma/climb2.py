"""Configurable plugboard hill climb: phase schedule over measures (0 IC, 1 monogram, 2 bigram, 3 trigram),
first-improvement or steepest ascent, plug removal allowed from `back_from` plugs."""
import numpy as np
from numba import njit
from solver import score_ic, score_tri, decrypt, nplugs_of, make_S, build_table


@njit(cache=True)
def score_m(S, ct, pb, N, meas, mono, bi, tri):
    if meas == 0:
        return score_ic(S, ct, pb, N)
    if meas == 3:
        return score_tri(S, ct, pb, N, tri)
    if meas == 1:
        s = 0.0
        for i in range(N):
            s += mono[pb[S[i, pb[ct[i]]]]]
        return s
    p0 = pb[S[0, pb[ct[0]]]]
    s = 0.0
    for i in range(1, N):
        p1 = pb[S[i, pb[ct[i]]]]
        s += bi[p0 * 26 + p1]
        p0 = p1
    return s


@njit(cache=True)
def phase_meas(npl, sched_from, sched_meas):
    m = sched_meas[0]
    for k in range(sched_from.shape[0]):
        if npl >= sched_from[k]:
            m = sched_meas[k]
    return m


@njit(cache=True)
def phase_idx(npl, sched_from):
    k = 0
    for j in range(sched_from.shape[0]):
        if npl >= sched_from[j]:
            k = j
    return k


@njit(cache=True)
def climb2(S, ct, N, pb, sched_from, sched_meas, back_from, steepest, mono, bi, tri):
    npl = nplugs_of(pb)
    ph = phase_idx(npl, sched_from)
    meas = sched_meas[ph]
    best = score_m(S, ct, pb, N, meas, mono, bi, tri)
    improved = True
    cand = np.empty(26, dtype=np.int64)
    bestpb = np.empty(26, dtype=np.int64)
    while improved:
        improved = False
        p2 = phase_idx(npl, sched_from)
        if p2 > ph:  # phases only advance (bomm behaviour), otherwise measure flips can cycle forever
            ph = p2; meas = sched_meas[ph]
            best = score_m(S, ct, pb, N, meas, mono, bi, tri)
        sweep_best = best
        for a in range(26):
            for b in range(a + 1, 26):
                pa = pb[a]; pbb = pb[b]
                # enumerate candidate plugboards for this pair into cand, evaluate each
                nopt = 0
                for opt in range(4):
                    for q in range(26):
                        cand[q] = pb[q]
                    dn = 0
                    if pa == a and pbb == b:
                        if opt > 0: break
                        cand[a] = b; cand[b] = a; dn = 1
                    elif npl < back_from:
                        break
                    elif pa == b:
                        if opt > 0: break
                        cand[a] = a; cand[b] = b; dn = -1
                    elif pa == a or pbb == b:
                        if opt > 1: break
                        if pa == a:
                            u = a; v = b; c = pbb
                        else:
                            u = b; v = a; c = pa
                        if opt == 0:
                            cand[c] = c; cand[u] = v; cand[v] = u
                        else:
                            cand[v] = v; cand[u] = c; cand[c] = u
                    else:
                        c = pa; d = pbb
                        if opt == 0:
                            cand[a] = b; cand[b] = a; cand[c] = c; cand[d] = d; dn = -1
                        elif opt == 1:
                            cand[a] = b; cand[b] = a; cand[c] = d; cand[d] = c
                        elif opt == 2:
                            cand[a] = d; cand[d] = a; cand[b] = b; cand[c] = c; dn = -1
                        else:
                            cand[a] = d; cand[d] = a; cand[b] = c; cand[c] = b
                    nopt += 1
                    s = score_m(S, ct, cand, N, meas, mono, bi, tri)
                    if steepest:
                        if s > sweep_best:
                            sweep_best = s
                            for q in range(26):
                                bestpb[q] = cand[q]
                    else:
                        if s > best:
                            best = s; improved = True
                            for q in range(26):
                                pb[q] = cand[q]
                            npl += dn
                            pa = pb[a]; pbb = pb[b]
                            break
        if steepest and sweep_best > best:
            best = sweep_best; improved = True
            for q in range(26):
                pb[q] = bestpb[q]
            npl = nplugs_of(pb)
    return score_tri(S, ct, pb, N, tri)
