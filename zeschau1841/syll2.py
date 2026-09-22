"""Syllabic annealer: each 2-digit code -> a letter or a French syllable; score the expanded text.

python syll.py [restarts] [iters] [seed codes as 11=la,70=pre ...]
Lines tokenised by offsets.json (a stray edge digit is dropped).
"""
import sys, json, random, math, numpy as np
from hsolve import score, A

UNITS = list('abcdefghijlmnopqrstuvxyz') + '''la le li lo lu ra re ri ro ru ma me mi mo mu na ne ni no nu ta te ti to tu
da de di do du sa se si so su ca ce ci co cu pa pe pi po pu va ve vi vo vu fa fe fi fo ga ge gi go ba be bi bo bu
qu que qui cha che chi cho pre pro pri tra tre tri tro dre gra gre bre bra cre cra fra fre
an en in on un am em im om ai au ou oi eu ei ar er ir or ur al el il ol as es is os us at et it ot ut
ent ant ment tion ion ons ais ait oit eur our par pour con com des les ses ces mes tes nous vous que qui
ien ier iere eme ere elle esse ette eux ance ence'''.split()


def load():
    off = json.load(open('offsets.json'))
    toks = []
    for l in open('ct_R5005.txt'):
        k, s = l.split(); o = off[k]
        toks += [s[i:i + 2] for i in range(o, len(s) - 1, 2)]
    return toks


def sc_(x, key):
    from collections import Counter
    c = Counter(k for k in key if k >= 24)          # a syllable cell may appear once in the table
    dup = sum(v - 1 for v in c.values())
    cl = Counter(k for k in key if k < 24); dupl = sum(max(0, v - 4) for v in cl.values())
    return score(x) + 2.3 * len(x) - 60 * dup - 60 * dupl


def run(toks, seeds, restarts, iters, rng):
    types = sorted(set(toks)); T = len(types); ti = {t: i for i, t in enumerate(types)}
    seq = [ti[t] for t in toks]
    U = [np.array([ord(c) - 97 for c in u]) for u in UNITS]
    uid = {u: i for i, u in enumerate(UNITS)}
    fixed = {ti[c]: uid[u] for c, u in seeds.items() if c in ti}
    best = (-1e18, None)
    for r in range(restarts):
        key = [fixed.get(t, rng.randrange(26)) for t in range(T)]  # start letters-only
        def expand():
            return np.concatenate([U[key[t]] for t in seq])
        x = expand(); cur = sc_(x, key)
        free = [t for t in range(T) if t not in fixed]
        for it in range(iters):
            temp = max(0.3, 8 * (1 - it / iters))
            t = rng.choice(free); old = key[t]
            key[t] = rng.randrange(len(UNITS)) if rng.random() < 0.5 else rng.randrange(24)
            x = expand(); sc = sc_(x, key)
            if sc >= cur or rng.random() < math.exp((sc - cur) / temp): cur = sc
            else: key[t] = old
        pt = '|'.join(UNITS[key[t]] for t in seq)
        print(f'restart {r}: {cur / len(seq):.3f}', flush=True)
        if cur > best[0]: best = (cur, {types[t]: UNITS[key[t]] for t in range(T)}, pt)
    return best


if __name__ == '__main__':
    R = int(sys.argv[1]); I = int(sys.argv[2])
    seeds = dict(a.split('=') for a in sys.argv[3:])
    sc, key, pt = run(load(), seeds, R, I, random.Random(len(sys.argv)))
    print(sc); print(' '.join(f'{k}={v}' for k, v in sorted(key.items())))
    print(pt[:1500].replace('|', ''))
