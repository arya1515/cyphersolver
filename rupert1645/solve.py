"""Homophonic anneal for R4921: 1-2 digit numbers = letters; letter+digit and 3-digit groups = code words (gaps)."""
import os, sys, re, random, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lang import lm

HERE = os.path.dirname(__file__)
lines = [l for l in open(os.path.join(HERE, 'transcription.txt'), encoding='utf8') if not l.startswith('#')]
toks = [t for l in lines for t in re.sub(r'\[[^\]]*\]', ' | ', l).split()]

def is_letter(t):
    return t.isdigit() and len(t) <= 2 and not t.startswith('0')

# segments of letter tokens between code groups / clear text
segs, cur = [], []
for t in toks:
    if is_letter(t):
        cur.append(t)
    else:
        if cur: segs.append(cur)
        cur = []
if cur: segs.append(cur)
syms = sorted({t for s in segs for t in s}, key=int)
idx = {s: i for i, s in enumerate(syms)}
S = [[idx[t] for t in s] for s in segs]

m = lm.load('en-1640s', spaces=False)
A = 'abcdefghiklmnopqrstuwxyz'  # early norm alphabet (no j, v)
enc = {c: i for i, c in enumerate(A)}

def score(key):
    return sum(m.score_idx(m.encode(''.join(A[key[x]] for x in s))) for s in S if len(s) > 1)

def run(seed, iters=60000):
    rnd = random.Random(seed)
    freq = 'eeeeeeeeettttttaaaaaooooooiiiiinnnnnsssssshhhhhrrrrrdddllluuucccmmwwffggyyppbbk'
    key = [enc[rnd.choice(freq)] for _ in syms]
    cur = score(key); best = (cur, key[:])
    T0 = 8.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.05
        i = rnd.randrange(len(syms)); old = key[i]
        key[i] = rnd.randrange(len(A))
        new = score(key)
        if new >= cur or rnd.random() < math.exp((new - cur) / T):
            cur = new
            if cur > best[0]: best = (cur, key[:])
        else:
            key[i] = old
    return best

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    res = sorted((run(s) for s in range(n)), reverse=True)
    for sc, key in res[:3]:
        print(round(sc, 1))
        out = []
        for t in toks:
            out.append(A[key[idx[t]]] if is_letter(t) else f' <{t}> ')
        print(''.join(out))
        print({s: A[key[idx[s]]] for s in syms})
