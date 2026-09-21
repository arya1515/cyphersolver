"""Fast feasibility search: can digit run D encipher letters L under a code of
the given group lengths, as a function code->letter (and optionally letter->code)?

Backtracking with undo rather than dict copying, which makes it ~100x faster.
"""
import sys

sys.setrecursionlimit(50000)


def fit(D, L, lens=(1, 2), twoway=True, want=1, node_cap=3_000_000):
    n, m = len(D), len(L)
    fwd = {}
    rev = {}
    sols = []
    nodes = [0]

    def rec(i, j):
        if len(sols) >= want or nodes[0] > node_cap:
            return
        nodes[0] += 1
        if j == m:
            if i == n:
                sols.append((dict(fwd), dict(rev)))
            return
        l = L[j]
        for k in lens:
            if i + k > n:
                continue
            c = D[i:i + k]
            fc = fwd.get(c)
            if fc is not None and fc != l:
                continue
            rl = rev.get(l) if twoway else None
            if twoway and rl is not None and rl != c:
                continue
            addf = fc is None
            addr = twoway and rl is None
            if addf:
                fwd[c] = l
            if addr:
                rev[l] = c
            rec(i + k, j + 1)
            if addf:
                del fwd[c]
            if addr:
                del rev[l]
            if len(sols) >= want:
                return
    rec(0, 0)
    return sols, nodes[0]
