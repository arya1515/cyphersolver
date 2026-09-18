"""Solve a homophonic substitution from scratch: simulated annealing over symbol->letter maps,
scored by the period-French character model.
   python hillclimb.py <cipher.txt> [restarts] [iters]"""
import sys, random, math, collections
from solve import logp, segment
AL = 'abcdefghilmnopqrstuxyz'
FR = 'esaitnrulodcmpvqfgbhxyz'.replace('v', '')   # rough French frequency order, period spelling
toks = open(sys.argv[1], encoding='utf-8').read().split()
restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 6
iters = int(sys.argv[3]) if len(sys.argv) > 3 else 12000
syms = [s for s, _ in collections.Counter(toks).most_common()]
freq = collections.Counter(toks)
import pickle
D = pickle.load(open('lm.pkl', 'rb')); U = D['cnt'][1]
tot1 = sum(U[c] for c in AL)
PF = {c: U[c]/tot1 for c in AL}          # French letter frequencies
BETA = float(__import__('os').environ.get('BETA', '2.0'))
def score(m):
    s = 0.0; ctx = ''; cnt = collections.Counter()
    for t in toks:
        ch = m[t]; s += logp(ctx, ch); ctx = (ctx+ch)[-6:]; cnt[ch] += 1
    n = len(toks)
    # KL(decoded letters || French): stops the search collapsing onto one letter
    kl = sum((cnt[c]/n)*math.log((cnt[c]/n)/PF[c]) for c in AL if cnt[c])
    return s - BETA*n*kl
best_overall = None
for r in range(restarts):
    # seed: most frequent figure -> most frequent French letter, with jitter
    m = {}
    for i, s in enumerate(syms):
        m[s] = FR[min(i % len(FR), len(FR)-1)] if r == 0 else random.choice(AL)
    cur = score(m); T0, T1 = 3.0, 0.15
    bestc, bestm = cur, dict(m)
    for it in range(iters):
        T = T0*(T1/T0)**(it/iters)
        s = random.choice(syms); old = m[s]; new = random.choice(AL)
        if new == old: continue
        m[s] = new; nxt = score(m)
        if nxt > cur or random.random() < math.exp((nxt-cur)/max(T, 1e-6)):
            cur = nxt
            if bestm is None or cur > bestc: bestc, bestm = cur, dict(m)
        else:
            m[s] = old
    if best_overall is None or bestc > best_overall[0]:
        best_overall = (bestc, bestm)
    print(f'  restart {r}: {bestc:.1f}', file=sys.stderr)
sc, m = best_overall
txt = ''.join(m[t] for t in toks)
print(f'score {sc:.1f}  ({len(toks)} figures, {len(syms)} symbols)')
print(segment(txt))
print()
print('map:', ' '.join(f'{s}={m[s]}' for s in syms))
