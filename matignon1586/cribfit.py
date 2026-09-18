"""Fit a cipher key by aligning the decoded figures to a known plaintext (a margin decipherment),
instead of to the language model alone. The crib need not be complete or exactly ordered: the score
counts how many of the decoded text's n-grams occur in the crib, so partial and out-of-order matches
still pull the search the right way.
   python cribfit.py <cipher.txt> <crib.txt> [restarts] [iters]      env: LAM, SEED, FIX"""
import sys, os, re, math, random, collections, pickle
from solve import logp, segment
AL = 'abcdefghilmnopqrstuxyz'
toks = open(sys.argv[1], encoding='utf-8').read().split()
CODE = {t for t in toks if re.fullmatch(r'\d+', t)}   # code groups stand for words, not letters
crib = open(sys.argv[2], encoding='utf-8').read().lower()
crib = re.sub(r'[^a-z]', '', crib.replace('v', 'u').replace('j', 'i'))
restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 6
iters = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
LAM = float(os.environ.get('LAM', '3.0'))
FIX = dict(p.split('=') for p in os.environ.get('FIX', '').split(',') if p)
random.seed(int(os.environ.get('SEED', '1')))
N = 4
cribN = collections.Counter(crib[i:i+N] for i in range(len(crib)-N+1))
n = len(toks)
syms = [s for s, _ in collections.Counter(toks).most_common() if s not in CODE]
D = pickle.load(open('lm.pkl', 'rb')); U1 = D['cnt'][1]
tot1 = sum(U1[c] for c in AL); PF = {c: U1[c]/tot1 for c in AL}
def score(ch):
    s = 0.0; cnt = collections.Counter()
    for i, c in enumerate(ch):
        if c == ' ': continue
        s += logp(''.join(ch[max(0, i-5):i]).rsplit(' ', 1)[-1], c); cnt[c] += 1
    nn = max(1, sum(cnt.values()))
    kl = sum((cnt[c]/nn)*math.log((cnt[c]/nn)/PF[c]) for c in AL if cnt[c])
    txt = ''.join(ch)
    hit = sum(1 for i in range(len(txt)-N+1) if txt[i:i+N] in cribN)
    return s - 2.0*n*kl + LAM*hit, hit
best_overall = None
for r in range(restarts):
    m = {s: random.choice(AL) for s in syms}
    m.update({k: v for k, v in FIX.items() if k in syms})
    ch = [(' ' if t in CODE else m[t]) for t in toks]
    cur, hit = score(ch)
    bestc, bestm, besth = cur, dict(m), hit
    T0, T1 = 2.5, 0.05
    for it in range(iters):
        T = T0*(T1/T0)**(it/iters)
        s = random.choice(syms)
        if s in FIX: continue
        old = m[s]
        new = m[random.choice(syms)] if random.random() < 0.45 else random.choice(AL)
        if new == old: continue
        m[s] = new
        ch = [(' ' if t in CODE else m[t]) for t in toks]
        nxt, hit = score(ch)
        if nxt > cur or random.random() < math.exp((nxt-cur)/max(T, 1e-9)):
            cur = nxt
            if cur > bestc: bestc, bestm, besth = cur, dict(m), hit
        else:
            m[s] = old
    print(f'  restart {r}: {bestc:.1f}  crib 4-grams matched {besth}', file=sys.stderr)
    if best_overall is None or bestc > best_overall[0]:
        best_overall = (bestc, bestm, besth)
sc, m, hit = best_overall
txt = ''.join((' ' if t in CODE else m[t]) for t in toks)
print(f'score {sc:.1f}   crib 4-grams matched {hit}/{len(txt)-N+1}')
print(segment(txt))
print()
print('map:', ' '.join(f'{s}={m[s]}' for s in syms))
