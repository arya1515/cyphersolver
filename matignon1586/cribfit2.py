"""Fit a key against a known plaintext, allowing a figure to stand for a DIGRAPH as well as a
single letter. Cipher-1 does this (its doubled-y is 'ss', its ff-ligature is 'n'), and the crib
words of the second cipher only make sense if that key does it too: bazeille, puissions and
presupose have no figure run with their letter-by-letter repeat pattern, which cannot happen if
every letter has its own figure.
   python cribfit2.py <cipher.txt> <crib.txt> [restarts] [iters]   env: LAM, SEED, FIX, NDIG"""
import sys, os, re, math, random, collections, pickle
from solve import logp, segment
AL = 'abcdefghilmnopqrstuxyz'
DIG = ['ss', 'll', 'nn', 'mm', 'tt', 'ee', 'rr', 'ff', 'on', 'en', 'ou', 'qu', 'es', 'er', 'an', 'ur']
toks = open(sys.argv[1], encoding='utf-8').read().split()
CODE = {t for t in toks if re.fullmatch(r'\d+', t)}
crib = open(sys.argv[2], encoding='utf-8').read().lower()
crib = re.sub(r'[^a-z]', '', crib.replace('v', 'u').replace('j', 'i'))
restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 6
iters = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
LAM = float(os.environ.get('LAM', '6.0'))
FIX = dict(p.split('=') for p in os.environ.get('FIX', '').split(',') if p)
random.seed(int(os.environ.get('SEED', '1')))
OPTS = list(AL) + DIG
N = 4
cribN = set(crib[i:i+N] for i in range(len(crib)-N+1))
syms = [s for s, _ in collections.Counter(toks).most_common() if s not in CODE]
D = pickle.load(open('lm.pkl', 'rb')); U1 = D['cnt'][1]
tot1 = sum(U1[c] for c in AL); PF = {c: U1[c]/tot1 for c in AL}
def render(m):
    return ' '.join(''.join(m[t] for t in run) for run in runs)
runs = []                      # code groups split the text into word-runs
cur = []
for t in toks:
    if t in CODE:
        if cur: runs.append(cur)
        cur = []
    else:
        cur.append(t)
if cur: runs.append(cur)
def score(m):
    txt = render(m)
    s = 0.0; ctx = ''; cnt = collections.Counter()
    for ch in txt:
        if ch == ' ':
            ctx = ''; continue
        s += logp(ctx, ch); ctx = (ctx+ch)[-5:]; cnt[ch] += 1
    nn = max(1, sum(cnt.values()))
    kl = sum((cnt[c]/nn)*math.log((cnt[c]/nn)/PF[c]) for c in AL if cnt[c])
    flat = txt.replace(' ', '')
    hit = sum(1 for i in range(len(flat)-N+1) if flat[i:i+N] in cribN)
    return s - 2.0*nn*kl + LAM*hit, hit, txt
SEED0 = {}
if os.environ.get('SEEDKEY'):
    import json
    k = json.load(open(os.environ['SEEDKEY']))
    SEED0 = {s: k[s][0] for s in syms if s in k and len(k[s][0]) == 1}
if os.environ.get('SEEDMAP'):
    for p in open(os.environ['SEEDMAP'], encoding='utf-8').read().split():
        if '=' in p:
            a, b = p.split('=', 1)
            if a in syms and b: SEED0[a] = b
best = None
for r in range(restarts):
    m = {s: random.choice(AL) for s in syms}
    for a, b in SEED0.items():
        if r == 0 or random.random() > 0.3: m[a] = b      # later restarts perturb the seed
    m.update({k: v for k, v in FIX.items() if k in syms})
    cur_s, hit, _ = score(m)
    bc, bm, bh = cur_s, dict(m), hit
    T0, T1 = 3.0, 0.05
    for it in range(iters):
        T = T0*(T1/T0)**(it/iters)
        s = random.choice(syms)
        if s in FIX: continue
        old = m[s]
        new = m[random.choice(syms)] if random.random() < 0.4 else random.choice(OPTS)
        if new == old: continue
        m[s] = new
        ns, hit, _ = score(m)
        if ns > cur_s or random.random() < math.exp((ns-cur_s)/max(T, 1e-9)):
            cur_s = ns
            if cur_s > bc: bc, bm, bh = cur_s, dict(m), hit
        else:
            m[s] = old
    print(f'  restart {r}: {bc:.1f}  crib 4-grams {bh}', file=sys.stderr)
    if best is None or bc > best[0]: best = (bc, bm, bh)
sc, m, hit = best
_, _, txt = score(m)
print(f'score {sc:.1f}   crib 4-grams matched {hit}')
print(segment(txt.replace(' ', '')))
print()
print('map:', ' '.join(f'{s}={m[s]}' for s in syms))
