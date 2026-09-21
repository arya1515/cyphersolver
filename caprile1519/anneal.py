"""Homophonic substitution anneal: each cipher token -> one plaintext letter, 4-gram Italian LM."""
import re, sys, random, math
sys.path.insert(0, r'C:\Users\dbour\cypher\.worktrees\bonzagni1512')
from lang import lm
import numpy as np
import os
KLW = float(os.environ.get('KLW','3'))
ORDER = int(os.environ.get('ORDER','4'))

def runs(path, drop=()):
    out = []
    for line in open(path, encoding='utf8'):
        m = re.match(r'\S+ L\d+:\s*(.*)', line)
        if not m: continue
        s = re.sub(r'\[[^\]]*\]', ' | ', m.group(1))
        cur = []
        for t in s.split():
            if t == '|':
                if cur: out.append(cur); cur = []
                continue
            t = t.rstrip('?')
            if t in ('#', '') or t.startswith('#') or t in drop: continue
            cur.append(t)
        if cur: out.append(cur)
    return out

def solve(seqs, model='it-cinquecento', iters=40000, restarts=20, seed=0):
    M = lm.load(model, order=ORDER, spaces=False)
    alpha = [c for c in M.alpha if c != ' ' and c not in 'kwxyj']
    toks = sorted({t for s in seqs for t in s})
    ti = {t: i for i, t in enumerate(toks)}
    idx = [np.array([ti[t] for t in s]) for s in seqs]
    rnd = random.Random(seed)
    it = 'eaoinlrtscdpumvghfbqz'
    freq = dict(zip(it, [11.8,11.7,9.8,10.1,6.9,6.5,6.4,5.6,5.0,4.5,3.7,3.0,3.0,2.5,2.1,1.6,1.1,1.0,0.9,0.5,0.9]))
    Z = sum(freq.values()); freq = {k: v / Z for k, v in freq.items()}
    N = sum(len(x) for x in idx)
    cnt = np.zeros(len(toks))
    for x in idx:
        for i in x: cnt[i] += 1
    def score(key):
        obs = {}
        for i, c in enumerate(key): obs[c] = obs.get(c, 0) + cnt[i]
        kl = sum((o / N) * math.log((o / N) / freq.get(c, 0.002)) for c, o in obs.items() if o)
        tot = -KLW * N * kl
        for x in idx:
            txt = ''.join(key[i] for i in x)
            if len(txt) >= 4: tot += M.score_idx(M.encode(txt))
        return tot
    best = None
    for r in range(restarts):
        key = [rnd.choice('eaoinrtlsc') for _ in toks]
        cur = score(key); T = 20.0
        for it in range(iters):
            i = rnd.randrange(len(toks)); old = key[i]
            key[i] = rnd.choice(alpha)
            s = score(key)
            if s >= cur or rnd.random() < math.exp((s - cur) / T): cur = s
            else: key[i] = old
            T = max(0.5, T * 0.9997)
        if best is None or cur > best[0]: best = (cur, key[:])
        print(r, round(cur, 1), ''.join(key[ti[t]] for t in seqs[0])[:60], flush=True)
    return best, toks

if __name__ == '__main__':
    seqs = runs(sys.argv[1])
    print(len(seqs), sum(map(len, seqs)))
    (sc, key), toks = solve(seqs, iters=int(sys.argv[2]) if len(sys.argv) > 2 else 20000, restarts=int(sys.argv[3]) if len(sys.argv) > 3 else 8)
    print('best', sc)
    print({t: k for t, k in zip(toks, key)})
    ti = {t: i for i, t in enumerate(toks)}
    for s in seqs: print(' '.join(s)); print('  ', ''.join(key[ti[t]] for t in s))
