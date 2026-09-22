"""Homophonic annealer with a plain add-k quadgram table (the shared dense LM over-rewards unseen repeats).
Env: TOK token file, CORPUS lang/corpora file, NUL=1 lets tokens map to null. Usage: anneal3.py restarts iters seed"""
import os, sys, math, random, re
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lang import lm
here = os.path.dirname(os.path.abspath(__file__))
LET = 'abcdefghilmnopqrstuxyz'
A = len(LET); IX = {c: i for i, c in enumerate(LET)}
corp = os.environ.get('CORPUS', 'fr-1520s-diplomatic')
cache = os.path.join(here, f'quad_{corp}.npy')
if os.path.exists(cache):
    Q = np.load(cache)
else:
    t = open(os.path.join(here, '..', 'lang', 'corpora', corp + '.txt'), encoding='utf8', errors='ignore').read()
    t = lm.norm(t, 'early').replace(' ', '').replace('k', 'c').replace('w', 'u').replace('j', 'i').replace('v', 'u')
    x = np.array([IX[c] for c in t if c in IX])
    q = ((x[:-3] * A + x[1:-2]) * A + x[2:-1]) * A + x[3:]
    c = np.bincount(q, minlength=A ** 4).reshape(-1, A).astype(float)
    Q = np.log((c + 0.01) / c.sum()).ravel().astype(np.float32)
    np.save(cache, Q)

rows = [l.split() for l in open(os.path.join(here, os.environ.get('TOK', 'qm_tokens.txt')), encoding='utf8') if l.strip() and not l.startswith('#')]
toks = [t for r in rows for t in r if not t.startswith('<') and not re.fullmatch(r'\d\d', t)]
types = sorted(set(toks)); tid = {t: i for i, t in enumerate(types)}
seq = np.array([tid[t] for t in toks]); L = len(seq)

NUL = os.environ.get('NUL') == '1'
KA = A + 1 if NUL else A
def score(key):
    x = key[seq]
    if NUL:
        x = x[x < A]
        pen = -float(os.environ.get('NP','10.5')) * (L - len(x))
    else:
        pen = 0.0
    q = ((x[:-3] * A + x[1:-2]) * A + x[2:-1]) * A + x[3:]
    return float(Q[q].sum()) + pen

def run(iters, rng):
    key = np.array([rng.randrange(KA) for _ in types])
    s = score(key); best = (s, key.copy())
    T0 = float(os.environ.get('T0', '15'))
    for k in range(iters):
        T = T0 * (0.01 ** (k / iters))
        i = rng.randrange(len(types)); old = key[i]
        if rng.random() < 0.5:
            key[i] = rng.randrange(KA); j = None
        else:
            j = rng.randrange(len(types)); key[i], key[j] = key[j], key[i]
        ns = score(key)
        if ns >= s or rng.random() < math.exp((ns - s) / T):
            s = ns
            if s > best[0]: best = (s, key.copy())
        else:
            if j is None: key[i] = old
            else: key[i], key[j] = key[j], key[i]
    return best

def show(key): return ''.join((LET+'_')[k] for k in key[seq])

if __name__ == '__main__':
    R, N, seed = (int(a) for a in (sys.argv[1:4] + ['4', '200000', '1'][len(sys.argv) - 1:]))
    rng = random.Random(seed); res = []
    for r in range(R):
        s, key = run(N, rng); res.append((s, r, key))
        print(f'restart {r}: {s / L:.3f}  {show(key)[:150]}', flush=True)
    s, _, key = max(res, key=lambda z: z[0])
    print('BEST', s / L); print(' '.join(f'{t}={(LET+"_")[key[tid[t]]]}' for t in types)); print(show(key))
