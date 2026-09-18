"""Cold solve of a homophonic substitution: annealing over figure->letter maps, scored by the
period-French character model with a penalty on the decoded letter distribution.
Scoring is incremental - changing one figure only disturbs its own positions and the few
characters that follow them - which is what makes the search affordable.
   python hillclimb.py <cipher.txt> [restarts] [iters]      env: BETA (default 2.0), SEED"""
import sys, os, re, math, random, collections, pickle
from solve import logp, segment
AL = 'abcdefghilmnopqrstuxyz'
W = 6                                   # model order
toks = open(sys.argv[1], encoding='utf-8').read().split()
CODE = {t for t in toks if re.fullmatch(r'\d+', t)}   # code groups stand for words, not letters
restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 6
iters = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
BETA = float(os.environ.get('BETA', '2.0'))
random.seed(int(os.environ.get('SEED', '1')))
n = len(toks)
syms = [s for s, _ in collections.Counter(toks).most_common() if s not in CODE]
pos = collections.defaultdict(list)
for i, t in enumerate(toks): pos[t].append(i)
D = pickle.load(open('lm.pkl', 'rb')); U1 = D['cnt'][1]
tot1 = sum(U1[c] for c in AL); PF = {c: U1[c]/tot1 for c in AL}
def ctxof(ch, i):
    c = ''.join(ch[max(0, i-W+1):i])
    return c.rsplit(' ', 1)[-1]          # a code group breaks the context, like a word end
def full(ch):
    s = 0.0
    for i in range(n):
        if ch[i] == ' ': continue
        s += logp(ctxof(ch, i), ch[i])
    return s
def kl(cnt):
    return sum((cnt[c]/n)*math.log((cnt[c]/n)/PF[c]) for c in AL if cnt[c])
best_overall = None
FIX = dict(p.split('=') for p in os.environ.get('FIX','').split(',') if p)
SEEDKEY = os.environ.get('SEEDKEY')       # start from a known key instead of at random
import json
seed = {}
if SEEDKEY:
    k = json.load(open(SEEDKEY))
    seed = {t: k[t][0] for t in k if t in pos and len(k[t][0]) == 1}
for r in range(restarts):
    m = {s: random.choice(AL) for s in syms}
    m.update({k: v for k, v in FIX.items() if k in pos})
    if SEEDKEY:
        for t, c in seed.items():
            if r == 0 or random.random() > 0.25: m[t] = c   # later restarts perturb the seed
    ch = [(' ' if t in CODE else m[t]) for t in toks]
    cnt = collections.Counter(c for c in ch if c != ' ')
    lm = full(ch); cur = lm - BETA*n*kl(cnt)
    bestc, bestm = cur, dict(m)
    T0, T1 = 2.5, 0.08
    for it in range(iters):
        T = T0*(T1/T0)**(it/iters)
        s = random.choice(syms)
        if s in FIX: continue
        old = m[s]
        # two move types: a fresh letter, or the letter another figure already carries.
        # Homophonic keys give several figures per letter, so copying an existing
        # assignment is the move that actually finds them.
        new = m[random.choice(syms)] if random.random() < 0.45 else random.choice(AL)
        if new == old: continue
        idx = pos[s]
        touched = sorted({j for i in idx for j in range(i, min(n, i+W))})
        before = sum(logp(ctxof(ch, j), ch[j]) for j in touched if ch[j] != ' ')
        for i in idx: ch[i] = new
        after = sum(logp(ctxof(ch, j), ch[j]) for j in touched if ch[j] != ' ')
        cnt[old] -= len(idx); cnt[new] += len(idx)
        nlm = lm - before + after
        nxt = nlm - BETA*n*kl(cnt)
        if nxt > cur or random.random() < math.exp((nxt-cur)/max(T, 1e-9)):
            cur, lm, m[s] = nxt, nlm, new
            if cur > bestc: bestc, bestm = cur, dict(m)
        else:
            for i in idx: ch[i] = old
            cnt[old] += len(idx); cnt[new] -= len(idx)
    print(f'  restart {r}: {bestc:.1f}', file=sys.stderr)
    if best_overall is None or bestc > best_overall[0]:
        best_overall = (bestc, bestm)
sc, m = best_overall
txt = ''.join((' ' if t in CODE else m[t]) for t in toks)
print(f'score {sc:.1f}  ({n} figures, {len(syms)} symbols, {sc/n:.2f}/fig)')
print(segment(txt))
print()
print('map:', ' '.join(f'{s}={m[s]}' for s in syms))
