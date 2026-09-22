"""Homophonic annealer for the Queen Mother -> de Foix letter (qm_tokens.txt).
Each cipher token maps to one plaintext letter (a-z, early norm: no j/v) or to null ('_').
Two-digit numbers are treated as nomenclator codes and removed (they are rare).
Usage: python anneal.py [restarts] [iters] [seed]"""
import os, sys, math, random, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lang import lm
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
M = lm.load(os.environ.get('LM','fr-1530-despatches'), order=5, spaces=False)
rows = [l.split() for l in open(os.path.join(here, 'qm_tokens.txt'), encoding='utf8') if l.strip() and not l.startswith('#')]
toks = [t for r in rows for t in r if not t.startswith('<') and not re.fullmatch(r'\d\d', t)]
types = sorted(set(toks))
tid = {t: i for i, t in enumerate(types)}
seq = np.array([tid[t] for t in toks])
LET = 'abcdefghilmnopqrstuxyz'
FQ = {'fr': [8,1,3,4,17,1,1,1,7,6,3,7,5,3,1,7,8,7,6,1,1,1], 'en': [8,2,3,4,12,2,2,6,7,4,2,7,7,2,1,6,6,9,3,1,2,1]}
freq = dict(zip(LET, FQ[os.environ.get('FQ','fr')]))

def text(key):
    return ''.join(key[i] for i in seq)

FR = np.array([freq[c] for c in LET], float); FR /= FR.sum()
LAM = float(os.environ.get('LAM', '3'))
def score(key):
    t = text(key)
    cnt = np.array([t.count(c) for c in LET], float) + 0.5; p = cnt / cnt.sum()
    kl = float((p * np.log(p / FR)).sum())
    return M.score_idx(M.encode(t)) - LAM * len(t) * kl

def run(iters, rng):
    pool = ''.join(c * freq[c] for c in LET)
    key = [rng.choice(pool) for _ in types]
    s = score(key); best = (s, key[:])
    T0 = 3.0
    for k in range(iters):
        T = T0 * (1 - k / iters) + 0.05
        i = rng.randrange(len(types)); old = key[i]
        key[i] = rng.choice(LET)
        ns = score(key)
        if ns >= s or rng.random() < math.exp((ns - s) / T):
            s = ns
            if s > best[0]: best = (s, key[:])
        else:
            key[i] = old
    return best

if __name__ == '__main__':
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 40000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    res = []
    for r in range(R):
        s, key = run(N, rng)
        res.append((s, key))
        print(f'restart {r}: {s / len(seq):.3f}/char  {text(key)[:160]}', flush=True)
    s, key = max(res)
    print('BEST', s / len(seq))
    print(' '.join(f'{t}={key[tid[t]]}' for t in types))
    print(text(key))
