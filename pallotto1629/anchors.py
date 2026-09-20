"""Recover a homophonic key from long PROVABLY-CONSISTENT alignment fragments.

A crib aligner can fit anything, because a fresh code may always be assigned a
fresh letter. The constraint that cannot be faked is repetition: inside one
window, a repeated code must carry the same letter and the mapping must stay a
function. A long run that survives that test is almost certainly a true
alignment, because chance runs die at the first repeat conflict.

So: try every (digit offset, crib offset) pair in a band, extend a run while it
stays consistent, keep the long ones, and pool their code->letter votes. Slips
in the transcription simply end a run early; they do not corrupt the votes.
"""
from collections import Counter, defaultdict


def runs(C, P, w=2, band=200, minlen=22, step=2):
    """Yield (i, j, length, mapping) for every maximal consistent run >= minlen."""
    n, m = len(C), len(P)
    out = []
    for i in range(0, n - w * minlen, step):
        lo = max(0, i // w - band)
        hi = min(m - minlen, i // w + band)
        for j in range(lo, hi):
            mp = {}
            k = 0
            while i + w * (k + 1) <= n and j + k < m:
                code = C[i + w * k: i + w * (k + 1)]
                ltr = P[j + k]
                t = mp.get(code)
                if t is None:
                    mp[code] = ltr
                elif t != ltr:
                    break
                k += 1
            if k >= minlen:
                out.append((i, j, k, mp))
    return out


def prune(rs):
    """Keep only maximal runs: drop any run contained in a longer one on the same diagonal."""
    best = {}
    for i, j, k, mp in rs:
        d = i - 2 * j                      # diagonal
        cur = best.get(d)
        if cur is None or k > cur[2]:
            best[d] = (i, j, k, mp)
    return sorted(best.values(), key=lambda r: -r[2])


def vote(rs, weight_by_len=True):
    v = defaultdict(Counter)
    for i, j, k, mp in rs:
        wgt = k if weight_by_len else 1
        for c, l in mp.items():
            v[c][l] += wgt
    return v


def key_from(v, minvotes=1):
    out = {}
    for c, cc in v.items():
        l, n = cc.most_common(1)[0]
        if n >= minvotes:
            out[c] = l
    return out


def agreement(key, truth):
    both = [c for c in key if c in truth]
    if not both:
        return 0.0, 0
    hit = sum(1 for c in both if key[c] == truth[c])
    return hit / len(both), len(both)
