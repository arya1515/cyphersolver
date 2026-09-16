"""Incremental-scoring plugboard hill climb (same neighbourhood and first-improvement order as climb2).
State: pb, q[i] = S_i[pb[c_i]], p[i] = pb[q[i]], letter counts f. A move changes <= 4 plugboard entries; only
positions with c_i or q_i in the changed set are re-decrypted, and only the n-grams touching them re-scored.
Measures: 0 IC, 2 bigram, 3 trigram (monogram dropped)."""
import numpy as np
from numba import njit
from solver import score_tri, nplugs_of


@njit(cache=True)
def init_state(S, ct, N, pb, q, p, f):
    for a in range(26):
        f[a] = 0
    for i in range(N):
        q[i] = S[i, pb[ct[i]]]
        p[i] = pb[q[i]]
        f[p[i]] += 1


@njit(cache=True)
def full_score(p, f, N, meas, bi, tri):
    if meas == 0:
        s = 0
        for a in range(26):
            s += f[a] * (f[a] - 1)
        return float(s)
    s = 0.0
    if meas == 2:
        for i in range(N - 1):
            s += bi[p[i] * 26 + p[i + 1]]
        return s
    for i in range(N - 2):
        s += tri[(p[i] * 26 + p[i + 1]) * 26 + p[i + 2]]
    return s


@njit(cache=True)
def eval_move(S, ct, N, pb, q, p, f, meas, bi, tri, D, newv, nd, mask, wst, sid,
              aff, oldp, oldq, oldpb, wlist):
    """Tentatively apply the move (letters D[:nd] -> newv[:nd]); returns (delta, naff, nw).
    Caller reverts with revert() if rejected. sid: unique stamp id for this evaluation."""
    for j in range(nd):
        mask[D[j]] = sid
        oldpb[j] = pb[D[j]]
    for j in range(nd):
        pb[D[j]] = newv[j]
    n = 0
    for i in range(N):
        if mask[ct[i]] == sid or mask[q[i]] == sid:
            aff[n] = i; oldq[n] = q[i]; oldp[n] = p[i]
            n += 1
    delta = 0.0
    if meas == 0:
        for j in range(n):
            i = aff[j]
            nq = S[i, pb[ct[i]]]; np_ = pb[nq]
            o = p[i]
            if np_ != o:
                f[o] -= 1; delta -= 2.0 * f[o]
                delta += 2.0 * f[np_]; f[np_] += 1
            q[i] = nq; p[i] = np_
        return delta, n, 0
    # n-gram measures: mark windows
    nw = 0
    if meas == 2:
        for j in range(n):
            i = aff[j]
            for k in range(i - 1, i + 1):
                if k >= 0 and k <= N - 2 and wst[k] != sid:
                    wst[k] = sid; wlist[nw] = k; nw += 1
        old = 0.0
        for j in range(nw):
            k = wlist[j]; old += bi[p[k] * 26 + p[k + 1]]
        for j in range(n):
            i = aff[j]
            nq = S[i, pb[ct[i]]]; np_ = pb[nq]
            f[p[i]] -= 1; f[np_] += 1
            q[i] = nq; p[i] = np_
        new = 0.0
        for j in range(nw):
            k = wlist[j]; new += bi[p[k] * 26 + p[k + 1]]
        return new - old, n, nw
    for j in range(n):
        i = aff[j]
        for k in range(i - 2, i + 1):
            if k >= 0 and k <= N - 3 and wst[k] != sid:
                wst[k] = sid; wlist[nw] = k; nw += 1
    old = 0.0
    for j in range(nw):
        k = wlist[j]; old += tri[(p[k] * 26 + p[k + 1]) * 26 + p[k + 2]]
    for j in range(n):
        i = aff[j]
        nq = S[i, pb[ct[i]]]; np_ = pb[nq]
        f[p[i]] -= 1; f[np_] += 1
        q[i] = nq; p[i] = np_
    new = 0.0
    for j in range(nw):
        k = wlist[j]; new += tri[(p[k] * 26 + p[k + 1]) * 26 + p[k + 2]]
    return new - old, n, nw


@njit(cache=True)
def revert(pb, q, p, f, D, nd, oldpb, aff, oldp, oldq, n):
    for j in range(nd):
        pb[D[j]] = oldpb[j]
    for j in range(n):
        i = aff[j]
        f[p[i]] -= 1; f[oldp[j]] += 1
        p[i] = oldp[j]; q[i] = oldq[j]


@njit(cache=True)
def phase_idx(npl, sched_from):
    k = 0
    for j in range(sched_from.shape[0]):
        if npl >= sched_from[j]:
            k = j
    return k


@njit(cache=True)
def climb3(S, ct, N, pb, sched_from, sched_meas, back_from, bi, tri, W):
    """W: workspace int64 array of size >= 8*N + 200. Returns trigram score; pb modified in place."""
    q = W[0:N]; p = W[N:2 * N]; aff = W[2 * N:3 * N]; oldp = W[3 * N:4 * N]; oldq = W[4 * N:5 * N]
    wlist = W[5 * N:6 * N]; wst = W[6 * N:7 * N]; mask = W[7 * N:7 * N + 26]; f = W[7 * N + 26:7 * N + 52]
    D = W[7 * N + 52:7 * N + 56]; newv = W[7 * N + 56:7 * N + 60]; oldpb = W[7 * N + 60:7 * N + 64]
    for i in range(N):
        wst[i] = -1
    for a in range(26):
        mask[a] = -1
    sid = 0
    init_state(S, ct, N, pb, q, p, f)
    npl = nplugs_of(pb)
    ph = phase_idx(npl, sched_from)
    meas = sched_meas[ph]
    improved = True
    eps = 1e-9
    while improved:
        improved = False
        p2 = phase_idx(npl, sched_from)
        if p2 > ph:
            ph = p2; meas = sched_meas[ph]
        for a in range(26):
            for b in range(a + 1, 26):
                pa = pb[a]; pbb = pb[b]
                if pa == a and pbb == b:
                    nopt = 1
                elif npl < back_from:
                    continue
                elif pa == b:
                    nopt = 1
                elif pa == a or pbb == b:
                    nopt = 2
                else:
                    nopt = 4
                for opt in range(nopt):
                    pa = pb[a]; pbb = pb[b]
                    dn = 0
                    if pa == a and pbb == b:
                        nd = 2; D[0] = a; D[1] = b; newv[0] = b; newv[1] = a; dn = 1
                    elif pa == b:
                        nd = 2; D[0] = a; D[1] = b; newv[0] = a; newv[1] = b; dn = -1
                    elif pa == a or pbb == b:
                        if pa == a:
                            u = a; v = b; c = pbb
                        else:
                            u = b; v = a; c = pa
                        nd = 3; D[0] = u; D[1] = v; D[2] = c
                        if opt == 0:
                            newv[0] = v; newv[1] = u; newv[2] = c
                        else:
                            newv[0] = c; newv[1] = v; newv[2] = u
                    else:
                        c = pa; d = pbb
                        nd = 4; D[0] = a; D[1] = b; D[2] = c; D[3] = d
                        if opt == 0:
                            newv[0] = b; newv[1] = a; newv[2] = c; newv[3] = d; dn = -1
                        elif opt == 1:
                            newv[0] = b; newv[1] = a; newv[2] = d; newv[3] = c
                        elif opt == 2:
                            newv[0] = d; newv[1] = b; newv[2] = c; newv[3] = a; dn = -1
                        else:
                            newv[0] = d; newv[1] = c; newv[2] = b; newv[3] = a
                    sid += 1
                    delta, n, nw = eval_move(S, ct, N, pb, q, p, f, meas, bi, tri, D, newv, nd, mask, wst, sid,
                                             aff, oldp, oldq, oldpb, wlist)
                    if delta > eps:
                        improved = True; npl += dn
                        break
                    else:
                        revert(pb, q, p, f, D, nd, oldpb, aff, oldp, oldq, n)
    return score_tri(S, ct, pb, N, tri)


@njit(cache=True)
def ils3(S, ct, N, pb, rounds, bi, tri, W, sched_from3, sched_meas3):
    """Iterated local search from pb: remove 2 random plugs, add 1 random, trigram-only re-climb; keep if better."""
    best = score_tri(S, ct, pb, N, tri)
    cur = np.empty(26, dtype=np.int64); trial = np.empty(26, dtype=np.int64)
    for a in range(26):
        cur[a] = pb[a]
    plugged = np.empty(26, dtype=np.int64); free = np.empty(26, dtype=np.int64)
    for r in range(rounds):
        for a in range(26):
            trial[a] = cur[a]
        for rep in range(2):
            npg = 0
            for a in range(26):
                if trial[a] > a:
                    plugged[npg] = a; npg += 1
            if npg == 0: break
            a = plugged[np.random.randint(0, npg)]; b = trial[a]
            trial[a] = a; trial[b] = b
        nf = 0
        for a in range(26):
            if trial[a] == a:
                free[nf] = a; nf += 1
        if nf >= 2:
            i = np.random.randint(0, nf); j = np.random.randint(0, nf - 1)
            if j >= i: j += 1
            a = free[i]; b = free[j]; trial[a] = b; trial[b] = a
        s = climb3(S, ct, N, trial, sched_from3, sched_meas3, 0, bi, tri, W)
        if s > best:
            best = s
            for a in range(26):
                cur[a] = trial[a]
    for a in range(26):
        pb[a] = cur[a]
    return best
