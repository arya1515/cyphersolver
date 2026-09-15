"""Fit digit->letter-set assignment (polyphonic, digit 4 = null) to three marginals: overall letter freq,
word-initial freq, word-final freq (words = segments between 4s). Pure frequency fit; ignores bigrams."""
import collections, math, random, sys
from parse5 import load, digit_stream
runs = digit_stream(load(), keep_marks=False)
NULL = sys.argv[1] if len(sys.argv) > 1 else '4'
# cipher stats
tot = collections.Counter(); ini = collections.Counter(); fin = collections.Counter()
for r in runs:
    segs = ''.join(r).split(NULL)
    for s in segs:
        if not s: continue
        tot.update(s); ini[s[0]] += 1; fin[s[-1]] += 1
D = [d for d in '0123456789' if d != NULL]
def norm(c, keys): n = sum(c[k] for k in keys); return {k: c[k] / n for k in keys}
ct, ci, cf = norm(tot, D), norm(ini, D), norm(fin, D)
# italian stats
text = open('corpus_it.txt', encoding='utf8').read(4000000)
words = text.split()
lt = collections.Counter(); li = collections.Counter(); lf = collections.Counter()
for w in words:
    lt.update(w); li[w[0]] += 1; lf[w[-1]] += 1
ALPHA = 'abcdefghilmnopqrstuz'
pt, pi, pf = norm(lt, ALPHA), norm(li, ALPHA), norm(lf, ALPHA)
print('cipher  tot:', ' '.join(f'{d}:{ct[d]:.3f}' for d in D))
print('cipher  ini:', ' '.join(f'{d}:{ci[d]:.3f}' for d in D))
print('cipher  fin:', ' '.join(f'{d}:{cf[d]:.3f}' for d in D))
print('italian tot:', ' '.join(f'{a}:{pt[a]:.3f}' for a in ALPHA))
print('italian ini:', ' '.join(f'{a}:{pi[a]:.3f}' for a in ALPHA))
print('italian fin:', ' '.join(f'{a}:{pf[a]:.3f}' for a in ALPHA))
def cost(assign):
    c = 0
    for d in D:
        S = [a for a in ALPHA if assign[a] == d]
        for (cc, pp, w) in ((ct, pt, 1.0), (ci, pi, 0.6), (cf, pf, 0.6)):
            q = sum(pp[a] for a in S)
            c += w * (cc[d] - q) ** 2 / (cc[d] + 0.01)
    return c
best = None
for trial in range(6):
    rnd = random.Random(trial)
    assign = {a: rnd.choice(D) for a in ALPHA}
    cur = cost(assign); T = 0.05
    for it in range(25000):
        a = rnd.choice(ALPHA); old = assign[a]; new = rnd.choice(D)
        if new == old: continue
        assign[a] = new; c2 = cost(assign)
        if c2 < cur or rnd.random() < math.exp((cur - c2) / T): cur = c2
        else: assign[a] = old
        T = max(0.0005, T * 0.99993)
    if best is None or cur < best[0]: best = (cur, dict(assign))
    print(f'trial {trial} cost {cur:.4f}: ' + ' '.join(f'{d}={"".join(a for a in ALPHA if assign[a] == d)}' for d in D))
print('\nBEST', best[0]); print(' '.join(f'{d}={"".join(a for a in ALPHA if best[1][a] == d)}' for d in D))
