"""Exact solver for a deterministic (no-homophone) variable-length digit code,
given a digit run D and the letters L it is known to encipher.

Because the code is deterministic, every occurrence of a letter is written the
same way, so a letter's group length is a property of the letter. If lengths are
1 or 2 and letter x occurs n_x times with length e_x, then

    sum n_x * e_x = len(D)   and   sum n_x = len(L)
    =>  sum over the two-digit letters of n_x  =  len(D) - len(L)

So: enumerate the subsets of distinct letters whose counts hit that total, which
fixes the length of every position, read the groups straight off D, and check
that the map is consistent both ways. Tiny search, exact answer.
"""
from collections import Counter
from itertools import combinations


def solve(D, L, maxlen=2):
    """Yield (code->letter, letter->code) for every deterministic code that fits."""
    n, m = len(D), len(L)
    need = n - m                      # extra digits contributed by longer groups
    cnt = Counter(L)
    letters = sorted(cnt)
    out = []
    if maxlen == 2:
        for r in range(0, len(letters) + 1):
            for sub in combinations(letters, r):
                if sum(cnt[x] for x in sub) != need:
                    continue
                elen = {x: (2 if x in sub else 1) for x in letters}
                out.extend(_check(D, L, elen))
    else:
        # lengths 1..maxlen: assign each letter a length, prune by running total
        def rec(idx, acc, elen):
            if acc > need:
                return
            if idx == len(letters):
                if acc == need:
                    out.extend(_check(D, L, elen))
                return
            x = letters[idx]
            for e in range(1, maxlen + 1):
                elen[x] = e
                rec(idx + 1, acc + cnt[x] * (e - 1), elen)
            del elen[x]
        rec(0, 0, {})
    return out


def _check(D, L, elen):
    fwd, rev = {}, {}
    i = 0
    for ch in L:
        k = elen[ch]
        c = D[i:i + k]
        if len(c) < k:
            return []
        if fwd.get(c, ch) != ch or rev.get(ch, c) != c:
            return []
        fwd[c] = ch
        rev[ch] = c
        i += k
    if i != len(D):
        return []
    return [(fwd, rev)]
