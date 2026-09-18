"""Damaged span after 前電云三日後商妥: letters 'xaqaqe'+'eianakerele'+'be' (19) must be 20 = 5 codes.
Try: one inserted letter anywhere, plus up to one substitution from common confusions (e/c, g/q, n/h, m/x ...),
score by LM over the 5 codes in context."""
import sys, itertools; sys.path.insert(0,'.'); sys.path.insert(0,'..')
from show17 import T
from family import code2ch, lp
S = 'xaqaqeeianakerelebe'
L = 'klmnpqrstvxyzbcdfghjaeiou'
def score(s):
    if len(s) != 20: return None
    sy = [s[i:i+2] for i in range(0, 20, 2)]
    if not all(x in T for x in sy): return None
    codes = ['%02d%02d' % (T[sy[i]], T[sy[i+1]]) for i in range(0, 10, 2)]
    chs = [code2ch.get(c) for c in codes]
    if None in chs: return None
    return sum(lp(c) for c in chs), ''.join(chs), s
res = {}
for i in range(20):
    for a in L:
        s1 = S[:i] + a + S[i:]
        cands = [s1]
        for j in range(20):
            for b in L:
                if b != s1[j]: cands.append(s1[:j] + b + s1[j+1:])
        for s in cands:
            r = score(s)
            if r: res[r[2]] = r
out = sorted(res.values(), key=lambda x: -x[0])
for r in out[:40]: print('%.1f %s %s' % r)
