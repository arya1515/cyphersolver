"""pick.py TOKEN...: for each token, score every candidate value (others fixed from key.json) and print the top 5."""
import json, sys, numpy as np
from parse import load
from solve import model
from lang import lm
m = model(); enc = {c: i for i, c in enumerate(lm.alphabet('early', False))}
k = json.load(open('key.json', encoding='utf-8'))
from solve2 import value
h = {int(a[1:]): b for a, b in k.items() if a.startswith('H')}; s = {a: b for a, b in k.items() if not a.startswith('H')}
runs, _ = load()
C = 'bcdfghklmnprstwz'
cands = [c + v for c in C for v in 'aeiou'] + list('abcdefghiklmnoprstuwz') + ['ch', 'sch', 'st', 'ab', 'ob', 'ub', 'is', 'es', 'as', 'us', 'qu', 'tz', 'ss', 'en', 'er', 'un', 'ck', '']
for tok in sys.argv[1:]:
    rs = [r for _, r in runs if tok in r]
    res = []
    for c in cands:
        s2 = dict(s); s2[tok] = c
        tot = 0
        for r in rs:
            t = ''.join((c if x == tok else value(x, h, s)) for x in r if '?' not in x)
            x = np.array([enc[q] for q in t if q in enc], dtype=np.int64); tot += m.score_idx(x) + 2.6 * len(x)
        res.append((tot, c))
    res.sort(reverse=True)
    print(tok, sum(r.count(tok) for r in rs), ' '.join(f'{c or "0"}:{v:.0f}' for v, c in res[:5]))
