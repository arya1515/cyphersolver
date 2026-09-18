"""Bigram-scored search of the damaged span between 妥 and 後 (see NOTES)."""
import sys, json, math, itertools, os
sys.path.insert(0,'.'); sys.path.insert(0,'..')
from show17 import T
from family import code2ch
lm = json.load(open('../lm_zh.json', encoding='utf-8')); uni, bi = lm['uni'], lm['bi']
tot = sum(uni.values())
def lpu(c): return math.log((uni.get(c,0)+0.5)/tot)
def lpb(a, b):
    pb = bi.get(a+b, 0) / (uni.get(a, 0) + 1)
    return math.log(0.7*pb + 0.3*math.exp(lpu(b)))
S = 'xaqaqeeianakerelebe'
CONF = {'e':'cia', 'c':'e', 'g':'q', 'q':'g', 'n':'hrmu', 'h':'nk', 'k':'h', 'a':'ou', 'o':'a', 'i':'e', 'u':'n', 'r':'n', 'm':'n', 'x':'m', 'l':'b', 'b':'l'}
L = 'klmnpqrstvxyzbcdfghjaeiou'
def score(s):
    sy = [s[i:i+2] for i in range(0, 20, 2)]
    if not all(x in T for x in sy): return None
    chs = [code2ch.get('%02d%02d' % (T[sy[i]], T[sy[i+1]])) for i in range(0, 10, 2)]
    if None in chs: return None
    seq = ['妥'] + chs + ['後']
    return sum(lpb(a, b) for a, b in zip(seq, seq[1:])), ''.join(chs), s
seen = {}
for i in range(20):
    for a in L:
        s1 = S[:i] + a + S[i:]
        pos = range(20)
        opts = [[s1[j]] + list(CONF.get(s1[j], '')) for j in pos]
        idx = [j for j in pos if len(opts[j]) > 1]
        for k in range(3):
            for js in itertools.combinations(idx, k):
                for rep in itertools.product(*[CONF[s1[j]] for j in js]):
                    s = list(s1)
                    for j, r in zip(js, rep): s[j] = r
                    s = ''.join(s)
                    if s in seen: continue
                    r = score(s)
                    seen[s] = r
res = sorted((r for r in seen.values() if r), key=lambda x: -x[0])
for r in res[:40]: print('%.1f %s %s' % r)
