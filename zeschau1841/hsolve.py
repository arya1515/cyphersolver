"""Homophonic annealer over a tokenised digit string, scored by a 4-gram letter model.

python hsolve.py <ciphertext file> <seg> [restarts] [iters]
seg:  fix2:0 / fix2:1         pairs from offset 0 or 1
      null:<digits>:<off>     drop those single digits, then pairs
      pref:<10 lengths>       first digit decides the group length, e.g. pref:2131131313
      synth                   control: encrypt French with a random homophonic 2-digit key
"""
import sys, random, math, numpy as np
from collections import Counter

LP = np.load(__file__.replace('hsolve.py', 'fr4.npy'))
A = 26


FR = np.array([7.6,.9,3.3,3.7,14.7,1.1,1.,.7,7.5,.5,.1,5.5,3.,7.1,5.4,2.5,1.4,6.7,7.9,7.3,6.3,1.8,.1,.4,.3,.1]); FR /= FR.sum()
W = 3.0


def score(x):
    c = ((x[:-3] * A + x[1:-2]) * A + x[2:-1]) * A + x[3:]
    n = np.bincount(x, minlength=A) + 1e-9; p = n / n.sum()
    return float(LP[c].sum()) - W * len(x) * float((p * np.log(p / FR)).sum())


def tokens(s, seg):
    kind, *a = seg.split(':')
    if kind == 'fix2':
        o = int(a[0]); return [s[i:i + 2] for i in range(o, len(s) - 1, 2)]
    if kind == 'null':
        t = ''.join(c for c in s if c not in a[0]); o = int(a[1])
        return [t[i:i + 2] for i in range(o, len(t) - 1, 2)]
    if kind == 'pref':
        L = [int(c) for c in a[0]]; out = []; i = 0
        while i < len(s):
            n = L[int(s[i])]; out.append(s[i:i + n]); i += n
        return out
    raise SystemExit(seg)


def solve(tok, restarts=6, iters=60000, seed=0):
    types = sorted(set(tok)); ti = {t: k for k, t in enumerate(types)}
    seq = np.array([ti[t] for t in tok]); T = len(types)
    freq = Counter(tok)
    rng = random.Random(seed); best = (-1e18, None)
    for r in range(restarts):
        key = np.array([rng.randrange(A) for _ in range(T)])
        cur = score(key[seq]); temp = 12.0
        for it in range(iters):
            t = rng.randrange(T); old = key[t]; key[t] = rng.randrange(A)
            sc = score(key[seq]); d = sc - cur
            if d >= 0 or rng.random() < math.exp(d / temp): cur = sc
            else: key[t] = old
            temp = max(0.5, 12.0 * (1 - it / iters))
        if cur > best[0]: best = (cur, key.copy())
        print(f'  restart {r}: {cur / len(tok):.3f}/char', flush=True)
    cur, key = best
    pt = ''.join(chr(97 + key[i]) for i in seq)
    return cur / len(tok), pt, {types[k]: chr(97 + key[k]) for k in range(T)}


if __name__ == '__main__':
    f, seg = sys.argv[1], sys.argv[2]
    R = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    I = int(sys.argv[4]) if len(sys.argv) > 4 else 60000
    if seg == 'synth':
        txt = ''.join(c for c in open(f, encoding='utf8').read().lower() if 'a' <= c <= 'z')[:1800]
        codes = random.Random(1).sample([f'{i:02d}' for i in range(100)], 100)
        f2 = Counter(txt); homs = {}; k = 0
        for ch, n in f2.most_common():
            m = max(1, round(n / len(txt) * 100)); homs[ch] = codes[k:k + m]; k += m
        tok = [random.choice(homs[c] or ['99']) for c in txt]
    else:
        s = ''.join(l.split()[1] for l in open(f) if l.strip())
        tok = tokens(s, seg)
    print(seg, len(tok), 'tokens', len(set(tok)), 'types')
    sc, pt, key = solve(tok, R, I)
    print(f'{sc:.3f}/char'); print(pt[:600])
