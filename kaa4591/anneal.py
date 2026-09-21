"""Substitution annealer for the KAA 4591 ciphertexts.

Input: a text file of cipher words, tokens separated by '.', words by spaces (or one token per char with --chars).
Tokens in `fixed` are pinned; the rest are annealed over letters (homophones allowed) against a lang/ model.
  python kaa4591/anneal.py FILE --model de-modern [--chars] [--fix a=e,b=n] [--iters 200000] [--restarts 8]
"""
import argparse, math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lang import lm

ap = argparse.ArgumentParser()
ap.add_argument('file'); ap.add_argument('--model', default='de-modern')
ap.add_argument('--chars', action='store_true'); ap.add_argument('--fix', default='')
ap.add_argument('--iters', type=int, default=200000); ap.add_argument('--restarts', type=int, default=6)
ap.add_argument('--nospace', action='store_true'); ap.add_argument('--cap', default='e3,n3,i2,r2,s2,t2,a2,d2,h2,u2'); ap.add_argument('--seed', type=int, default=1)
a = ap.parse_args()
random.seed(a.seed)
M = lm.load(a.model, spaces=not a.nospace) if a.nospace else lm.load(a.model)
raw = open(a.file, encoding='utf8').read().split()
words = [list(w) if a.chars else w.split('.') for w in raw]
toks = sorted({t for w in words for t in w})
fixed = dict(kv.split('=') for kv in a.fix.split(',') if kv)
LET = 'abcdefghiklmnopqrstuwz'
free = [t for t in toks if t not in fixed]
CAP = {c: 1 for c in LET}; CAP.update({kv[0]: int(kv[1:]) for kv in a.cap.split(',') if kv})
from collections import Counter
def ok(key):
    c = Counter(key[t] for t in free)
    return all(c[l] <= CAP[l] for l in c)
def rand_key():
    pool = [l for l in LET for _ in range(CAP[l])]; random.shuffle(pool)
    k = dict(fixed)
    for t in free: k[t] = pool.pop() if pool else random.choice(LET)
    return k

def text(key):
    j = '' if a.nospace else ' '
    return j.join(''.join(key.get(t, '?') if len(key.get(t, '?')) else '' for t in w) for w in words)

def score(key):
    return M.score_idx(M.encode(text(key)))

best_all = None
for r in range(a.restarts):
    key = rand_key()
    cur = score(key); best = (cur, dict(key))
    T0 = 0.02 * sum(len(w) for w in words) ** 0.5
    for i in range(a.iters):
        T = T0 * (1 - i / a.iters) + 1e-3
        t = random.choice(free); old = key[t]
        if random.random() < 0.5:
            u = random.choice(free); key[t], key[u] = key[u], key[t]
            undo = lambda: key.__setitem__(u, key[t]) or key.__setitem__(t, old)
        else:
            key[t] = random.choice(LET)
            if not ok(key): key[t] = old; continue
            undo = lambda: key.__setitem__(t, old)
        s = score(key)
        if s >= cur or random.random() < math.exp((s - cur) / T):
            cur = s
            if s > best[0]: best = (s, dict(key))
        else:
            undo()
    print(f'restart {r}: {best[0]:.1f}', text(best[1])[:200], flush=True)
    if best_all is None or best[0] > best_all[0]: best_all = best
print('BEST', best_all[0]); print(' '.join(f'{t}={best_all[1][t]}' for t in toks)); print(text(best_all[1]))
