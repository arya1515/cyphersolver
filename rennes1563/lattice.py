"""Beam decode a line of glyph tokens, each with candidate plaintext values ('-' = null),
under a French n-gram model. Usage: python lattice.py FILE  (lines: tok=a|b|c ...)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lang import lm
M = lm.load('fr-1530-despatches', spaces=False)

def decode(cands, beam=400, prefix=''):
    B = [(0.0, prefix)]
    for opts in cands:
        nb = {}
        for sc, s in B:
            for o in opts:
                o = '' if o == '-' else o
                t = s + o
                ctx = t[-(M.order + len(o) + 2):]
                add = M.score(t[-(M.order - 1 + len(o)):]) - M.score(t[-(M.order - 1 + len(o)):len(t) - len(o)]) if o else -0.3
                v = sc + add
                if t not in nb or nb[t] < v: nb[t] = v
        B = sorted(((v, t) for t, v in nb.items()), reverse=True)[:beam]
    return B

def parse(line):
    out = []
    for tok in line.split():
        from glyphs import cands; out.append(cands(tok))
    return out

if __name__ == '__main__':
    for ln in open(sys.argv[1], encoding='utf-8'):
        ln = ln.strip()
        if not ln or ln.startswith('#'): print(ln); continue
        r = decode(parse(ln))
        for v, t in r[:3]: print(round(v, 1), t)
        print()
