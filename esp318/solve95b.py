import pickle, numpy as np, sys, math, random
from lm import ALPHA, IDX
from assign95 import CL2L
from solve95 import load_cipher
L = len(ALPHA)
JUNK = {20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
lp = np.load('lm5_dense.npy')
seq, lines, lab = load_cipher()
S = seq.max()+1
gap = np.array([s in JUNK for s in range(S)])
isgap = gap[seq]
# windows of 5 with no gap
ok = np.array([not isgap[i:i+5].any() for i in range(len(seq)-4)])
print('symbols', len(seq), 'gap symbols', isgap.sum(), 'scored windows', ok.sum())
def score(key):
    d = key[seq]
    v = lp[d[:-4], d[1:-3], d[2:-2], d[3:-1], d[4:]]
    return v[ok].sum()
fixed = {c: IDX[l.lower()] for c, l in CL2L.items()}
free = [s for s in range(1, S) if s not in fixed and not gap[s] and (seq==s).any()]
print('fixed', len(fixed), 'free', len(free), 'free sizes', sorted([(int((seq==s).sum()), s) for s in free], reverse=True)[:25])
def anneal(seed, iters=30000, T0=2.0, T1=0.05, unfix=False):
    rng = random.Random(seed)
    key = np.zeros(S, int)
    for s in range(S): key[s] = fixed.get(s, rng.randrange(L))
    movable = free + (list(fixed) if unfix else [])
    cur = score(key); best = cur; bk = key.copy()
    for it in range(iters):
        T = T0*(T1/T0)**(it/iters)
        s = rng.choice(movable); old = key[s]; key[s] = rng.randrange(L)
        if key[s] == old: continue
        new = score(key)
        if new >= cur or rng.random() < math.exp((new-cur)/T): cur = new
        else: key[s] = old
        if cur > best: best, bk = cur, key.copy()
    return best, bk
res = []
for seed in range(6):
    b, k = anneal(seed); res.append((b, k)); print('seed', seed, round(b,1), flush=True)
b, k = max(res, key=lambda r: r[0])
print('best', round(b,1), 'per window', round(b/ok.sum(),3))
# report free-cluster assignments with agreement across seeds
agree = {}
for s in free:
    vals = [ALPHA[r[1][s]] for r in res]
    agree[s] = (ALPHA[k[s]], sum(v==ALPHA[k[s]] for v in vals), int((seq==s).sum()))
print('free assignments (letter, agreement/6, n):', {s:agree[s] for s in sorted(agree, key=lambda s:-agree[s][2])})
dec = ''.join('.' if gap[s] else ALPHA[k[s]] for s in seq)
out=[]; pos=0
for ln in sorted(set(lines.tolist())):
    n=(lines==ln).sum(); out.append(dec[pos:pos+n]); pos+=n
open('f122r_solved.txt','w').write('\n'.join(f'{i+1:2d} {t}' for i,t in enumerate(out)))
pickle.dump(dict(key=k, free=free, fixed=fixed, junk=JUNK), open('f122r_key.pkl','wb'))
print('\n'.join(f'{i+1:2d} {t}' for i,t in enumerate(out)))
