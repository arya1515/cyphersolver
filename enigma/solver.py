"""Ciphertext-only Enigma I attack (Gillogly / Sullivan-Weierud / Ostwald-Weierud style) in numba.

Key space per wheel order: 26^3 core start positions x i0 (letter index at which the middle wheel first steps,
1..26, equivalent to the right ring setting) x optional left-wheel double step at the k-th middle step.
For each location: plugboard hill climb from a set of start plugboards (E-Stecker: E self-steckered or E-x),
IC until `tri_from` plugs then Sinkov trigram score; removing plugs allowed from `back_from` plugs.
"""
import numpy as np
from numba import njit, prange
import numba as nb
from enigma_core import WHEELS, UKW, perm, inv, A

ORDERS = [(a, b, c) for a in WHEELS for b in WHEELS for c in WHEELS if len({a, b, c}) == 3]
WNAMES = list(WHEELS)


def build_table(order, ukw='B'):
    """T[l,m,r,x]: scrambler permutation with ring settings A (core positions l,m,r)."""
    rot = [perm(WHEELS[w][0]) for w in order]
    rinv = [inv(r) for r in rot]
    u = perm(UKW[ukw])
    l = np.arange(26)[:, None, None, None]
    m = np.arange(26)[None, :, None, None]
    r = np.arange(26)[None, None, :, None]
    x = np.arange(26)[None, None, None, :]
    offs = [l, m, r]
    y = np.broadcast_to(x, (26, 26, 26, 26))
    for i in (2, 1, 0):
        y = (rot[i][(y + offs[i]) % 26] - offs[i]) % 26
    y = u[y]
    for i in (0, 1, 2):
        y = (rinv[i][(y + offs[i]) % 26] - offs[i]) % 26
    return np.ascontiguousarray(y.astype(np.int64))


@njit(cache=True)
def make_S(T, l, m, r, i0, kleft, N, S):
    t = i0 + 26 * kleft + 1
    for i in range(N):
        ms = 0 if i < i0 else (i - i0) // 26 + 1
        ex = 0; ls = 0
        if kleft >= 0 and i >= t:
            ex = 1; ls = 1
        li = (l + ls) % 26; mi = (m + ms + ex) % 26; ri = (r + i) % 26
        for x in range(26):
            S[i, x] = T[li, mi, ri, x]


@njit(cache=True)
def score_ic(S, ct, pb, N):
    f = np.zeros(26, dtype=np.int64)
    for i in range(N):
        f[pb[S[i, pb[ct[i]]]]] += 1
    s = 0
    for a in range(26):
        s += f[a] * (f[a] - 1)
    return float(s)


@njit(cache=True)
def score_tri(S, ct, pb, N, logp):
    p0 = pb[S[0, pb[ct[0]]]]
    p1 = pb[S[1, pb[ct[1]]]]
    s = 0.0
    for i in range(2, N):
        p2 = pb[S[i, pb[ct[i]]]]
        s += logp[(p0 * 26 + p1) * 26 + p2]
        p0 = p1; p1 = p2
    return s


@njit(cache=True)
def decrypt(S, ct, pb, N, out):
    for i in range(N):
        out[i] = pb[S[i, pb[ct[i]]]]


@njit(cache=True)
def sc(S, ct, pb, N, logp, use_tri):
    if use_tri:
        return score_tri(S, ct, pb, N, logp)
    return score_ic(S, ct, pb, N)


@njit(cache=True)
def nplugs_of(pb):
    n = 0
    for a in range(26):
        if pb[a] != a: n += 1
    return n // 2


@njit(cache=True)
def climb(S, ct, N, pb, logp, tri_from, back_from):
    """First-improvement hill climb over plugboard moves. pb modified in place. Returns trigram score."""
    npl = nplugs_of(pb)
    use_tri = npl >= tri_from
    best = sc(S, ct, pb, N, logp, use_tri)
    improved = True
    while improved:
        improved = False
        if (not use_tri) and npl >= tri_from:
            use_tri = True
            best = sc(S, ct, pb, N, logp, True)
        for a in range(26):
            for b in range(a + 1, 26):
                pa = pb[a]; pbb = pb[b]
                if pa == a and pbb == b:
                    pb[a] = b; pb[b] = a
                    s = sc(S, ct, pb, N, logp, use_tri)
                    if s > best:
                        best = s; improved = True; npl += 1
                    else:
                        pb[a] = a; pb[b] = b
                elif npl < back_from:
                    continue
                elif pa == b:
                    pb[a] = a; pb[b] = b
                    s = sc(S, ct, pb, N, logp, use_tri)
                    if s > best:
                        best = s; improved = True; npl -= 1
                    else:
                        pb[a] = b; pb[b] = a
                elif pa == a or pbb == b:
                    # one self-steckered (u), other (v) plugged with c
                    if pa == a:
                        u = a; v = b; c = pbb
                    else:
                        u = b; v = a; c = pa
                    # option 1: unplug v-c, plug u-v
                    pb[c] = c; pb[u] = v; pb[v] = u
                    s1 = sc(S, ct, pb, N, logp, use_tri)
                    # option 2: plug u-c, v self
                    pb[v] = v; pb[u] = c; pb[c] = u
                    s2 = sc(S, ct, pb, N, logp, use_tri)
                    if s1 > best and s1 >= s2:
                        pb[v] = v; pb[u] = u; pb[c] = c
                        pb[u] = v; pb[v] = u
                        best = s1; improved = True
                    elif s2 > best:
                        best = s2; improved = True
                    else:
                        pb[u] = u; pb[c] = v; pb[v] = c
                else:
                    # a-c and b-d plugged separately
                    c = pa; d = pbb
                    # opt1: a-b, c,d self
                    pb[a] = b; pb[b] = a; pb[c] = c; pb[d] = d
                    s1 = sc(S, ct, pb, N, logp, use_tri)
                    # opt2: a-b, c-d
                    pb[c] = d; pb[d] = c
                    s2 = sc(S, ct, pb, N, logp, use_tri)
                    # opt3: a-d, b,c self
                    pb[a] = d; pb[d] = a; pb[b] = b; pb[c] = c
                    s3 = sc(S, ct, pb, N, logp, use_tri)
                    # opt4: a-d, b-c
                    pb[b] = c; pb[c] = b
                    s4 = sc(S, ct, pb, N, logp, use_tri)
                    m = max(max(s1, s2), max(s3, s4))
                    if m > best:
                        best = m; improved = True
                        if m == s1:
                            pb[a] = b; pb[b] = a; pb[c] = c; pb[d] = d; npl -= 1
                        elif m == s2:
                            pb[a] = b; pb[b] = a; pb[c] = d; pb[d] = c
                        elif m == s3:
                            pb[a] = d; pb[d] = a; pb[b] = b; pb[c] = c; npl -= 1
                        else:
                            pass  # already opt4
                    else:
                        pb[a] = c; pb[c] = a; pb[b] = d; pb[d] = b
    if use_tri:
        return best
    return score_tri(S, ct, pb, N, logp)


@njit(cache=True)
def best_climb(S, ct, N, starts, logp, tri_from, back_from, pbout):
    best = -1e18
    pb = np.empty(26, dtype=np.int64)
    for k in range(starts.shape[0]):
        for a in range(26):
            pb[a] = starts[k, a]
        s = climb(S, ct, N, pb, logp, tri_from, back_from)
        if s > best:
            best = s
            for a in range(26):
                pbout[a] = pb[a]
    return best


@njit(parallel=True, cache=True)
def search_order(T, ct, N, i0s, kleft, starts, logp, tri_from, back_from, K, out_scores, out_keys):
    """out_scores: (676, K) float64 (init -inf); out_keys: (676, K, 31) int64:
    l m r i0 kleft + 26 plugboard entries."""
    for lm in prange(676):
        l = lm // 26; m = lm % 26
        S = np.empty((N, 26), dtype=np.int64)
        pbout = np.empty(26, dtype=np.int64)
        for r in range(26):
            for j in range(i0s.shape[0]):
                i0 = i0s[j]
                make_S(T, l, m, r, i0, kleft, N, S)
                s = best_climb(S, ct, N, starts, logp, tri_from, back_from, pbout)
                if s > out_scores[lm, K - 1]:
                    # insert
                    pos = K - 1
                    while pos > 0 and out_scores[lm, pos - 1] < s:
                        out_scores[lm, pos] = out_scores[lm, pos - 1]
                        for q in range(31):
                            out_keys[lm, pos, q] = out_keys[lm, pos - 1, q]
                        pos -= 1
                    out_scores[lm, pos] = s
                    out_keys[lm, pos, 0] = l; out_keys[lm, pos, 1] = m; out_keys[lm, pos, 2] = r
                    out_keys[lm, pos, 3] = i0; out_keys[lm, pos, 4] = kleft
                    for q in range(26):
                        out_keys[lm, pos, 5 + q] = pbout[q]


def e_stecker_starts():
    st = np.tile(np.arange(26), (26, 1))
    e = A.index('E')
    for k in range(26):
        if k != e:
            st[k, e] = k; st[k, k] = e
    return st.astype(np.int64)


def run_order(order, ct, i0s, kleft=-1, starts=None, K=50, tri_from=7, back_from=5, ukw='B', logp=None):
    T = build_table(order, ukw)
    N = len(ct)
    if starts is None: starts = e_stecker_starts()
    out_scores = np.full((676, K), -np.inf)
    out_keys = np.zeros((676, K, 31), dtype=np.int64)
    search_order(T, np.asarray(ct, dtype=np.int64), N, np.asarray(i0s, dtype=np.int64), kleft, starts, logp,
                 tri_from, back_from, K, out_scores, out_keys)
    sc_ = out_scores.reshape(-1); ke = out_keys.reshape(-1, 31)
    idx = np.argsort(-sc_)[:K]
    return sc_[idx], ke[idx]


def fmt_key(order, key):
    l, m, r, i0, kl = key[:5]
    pb = key[5:]
    plugs = ' '.join(A[a] + A[pb[a]] for a in range(26) if pb[a] > a)
    return '%s core %s%s%s i0=%2d kl=%2d [%s]' % ('-'.join(order), A[l], A[m], A[r], i0, kl, plugs)


def decrypt_key(order, ct, key, ukw='B'):
    T = build_table(order, ukw)
    N = len(ct); S = np.empty((N, 26), dtype=np.int64)
    l, m, r, i0, kl = key[:5]
    make_S(T, l, m, r, i0, kl, N, S)
    out = np.empty(N, dtype=np.int64)
    decrypt(S, np.asarray(ct, dtype=np.int64), np.asarray(key[5:], dtype=np.int64), N, out)
    return ''.join(A[i] for i in out)


def letters(s):
    return np.array([A.index(c) for c in s.upper() if c in A], dtype=np.int64)
