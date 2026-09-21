"""Solve a variable-length (1- or 2-digit) deterministic code from exact cribs.

The repeat spectrum says the code is deterministic: no homophones. So the map is
a function BOTH ways - each letter always written the same way, each code always
meaning the same letter. That is a very strong constraint, and with an exact
crib (a digit run whose plaintext is known from a decipherment written on the
page) it can simply be searched.

Segmentations of D into len(L) codes of length 1 or 2 are enumerated by DP with
the two-way consistency carried along.
"""
import re
from solve import norm_plain


def solve_crib(D, L, code_lens=(1, 2), fwd=None, rev=None, limit=200000):
    """Return list of (fwd, rev) maps consistent with D enciphering L."""
    fwd = dict(fwd or {})          # code -> letter
    rev = dict(rev or {})          # letter -> code
    out = []
    n, m = len(D), len(L)
    seen = 0

    def rec(i, j, f, r):
        nonlocal seen
        seen += 1
        if seen > limit:
            return
        if j == m:
            if i == n:
                out.append((dict(f), dict(r)))
            return
        for k in code_lens:
            if i + k > n:
                continue
            c = D[i:i + k]
            l = L[j]
            fc, rl = f.get(c), r.get(l)
            if fc is not None and fc != l:
                continue
            if rl is not None and rl != c:
                continue
            f2, r2 = f, r
            if fc is None or rl is None:
                f2 = dict(f); r2 = dict(r)
                f2[c] = l; r2[l] = c
            rec(i + k, j + 1, f2, r2)
    rec(0, 0, fwd, rev)
    return out


def merge(sols):
    """Values every solution agrees on."""
    if not sols:
        return {}, {}
    f0, r0 = sols[0]
    f = {c: l for c, l in f0.items() if all(s[0].get(c) == l for s in sols)}
    r = {l: c for l, c in r0.items() if all(s[1].get(l) == c for s in sols)}
    return f, r


def clean(s):
    return norm_plain(re.sub(r'[?*]', '', s))
