import pickle, numpy as np, sys, math, random
from scipy.cluster.hierarchy import fcluster
from lm import ALPHA, IDX
from assign95 import CL2L

L = len(ALPHA)
def dense_lm(lmp='lm5.pkl'):
    d = pickle.load(open(lmp,'rb')); cnt = d['cnt']
    # interpolated Witten-Bell-ish backoff into a dense 5-gram table
    tot1 = sum(cnt[1].values())
    p1 = np.array([(cnt[1].get(c,0)+1)/(tot1+L) for c in ALPHA])
    # build order-n tables progressively
    tabs = [None, p1]
    for n in range(2, 6):
        prev = tabs[n-1]
        shape = (L,)*n
        tab = np.zeros(shape, np.float64)
        # context counts and type counts
        ctx_tot = {}; ctx_types = {}
        for g, c in cnt[n].items():
            ctx = g[:-1]; ctx_tot[ctx] = ctx_tot.get(ctx,0)+c; ctx_types[ctx] = ctx_types.get(ctx,0)+1
        it = np.nditer(tab, flags=['multi_index'], op_flags=['writeonly'])
        # vectorised fill: iterate contexts
        idxs = np.indices(shape[:-1]).reshape(n-1, -1).T
        for ci in idxs:
            ctx = ''.join(ALPHA[i] for i in ci)
            T = ctx_tot.get(ctx,0); ty = ctx_types.get(ctx,0)
            lam = T/(T+ty) if T>0 else 0.0
            back = prev[tuple(ci[1:])] if n>2 else prev
            row = np.zeros(L)
            if T>0:
                for k,ch in enumerate(ALPHA):
                    row[k] = cnt[n].get(ctx+ch,0)/T
            tab[tuple(ci)] = lam*row + (1-lam)*back
        tabs.append(tab)
    lp = np.log(tabs[5])
    np.save('lm5_dense.npy', lp)
    return lp

def load_cipher(pkl='f122r_glyphs.pkl', nc=110):
    d = pickle.load(open(pkl,'rb'))
    lab = fcluster(d['Z'], nc, 'maxclust'); meta = d['meta']
    order = sorted(range(len(meta)), key=lambda i: (meta[i]['line'], meta[i]['x0']))
    seq = np.array([int(lab[i]) for i in order]); lines = np.array([meta[i]['line'] for i in order])
    return seq, lines, lab

def score(lp, dec):
    # dec: int array of letter indices
    n = len(dec)
    s = 0.0
    if n >= 5:
        s = lp[dec[:-4], dec[1:-3], dec[2:-2], dec[3:-1], dec[4:]].sum()
    return s

def anneal(lp, seq, init, iters=60000, T0=3.0, T1=0.05, seed=0, fixed=None):
    rng = random.Random(seed)
    syms = sorted(set(seq.tolist())); S = max(syms)+1
    key = np.array([init.get(s, rng.randrange(L)) for s in range(S)])
    dec = key[seq]; cur = score(lp, dec); best = cur; bestkey = key.copy()
    freq = np.bincount(seq, minlength=S)
    for it in range(iters):
        T = T0*(T1/T0)**(it/iters)
        s = rng.choice(syms)
        if fixed and s in fixed: continue
        old = key[s]
        if rng.random() < 0.15:
            s2 = rng.choice(syms)
            if fixed and s2 in fixed: continue
            key[s], key[s2] = key[s2], key[s]
            dec = key[seq]; new = score(lp, dec)
            if new >= cur or rng.random() < math.exp((new-cur)/T): cur = new
            else: key[s], key[s2] = key[s2], key[s]
        else:
            key[s] = rng.randrange(L)
            if key[s] == old: continue
            dec = key[seq]; new = score(lp, dec)
            if new >= cur or rng.random() < math.exp((new-cur)/T): cur = new
            else: key[s] = old
        if cur > best: best = cur; bestkey = key.copy()
    return best, bestkey

if __name__ == '__main__':
    import os
    lp = np.load('lm5_dense.npy') if os.path.exists('lm5_dense.npy') else dense_lm()
    seq, lines, lab = load_cipher()
    init = {c: IDX[l.lower()] for c, l in CL2L.items()}
    init_key = np.array([init.get(s, 0) for s in range(seq.max()+1)])
    print('init score', score(lp, init_key[seq]))
    results = []
    for seed in range(int(sys.argv[1]) if len(sys.argv)>1 else 4):
        b, k = anneal(lp, seq, init, iters=int(sys.argv[2]) if len(sys.argv)>2 else 60000, seed=seed)
        results.append((b, k)); print('seed', seed, 'score', round(b,1), flush=True)
    b, k = max(results, key=lambda r: r[0])
    dec = ''.join(ALPHA[i] for i in k[seq])
    out = []
    pos = 0
    for ln in sorted(set(lines.tolist())):
        n = (lines==ln).sum(); out.append(dec[pos:pos+n]); pos += n
    open('f122r_solved.txt','w').write('\n'.join(f'{i+1:2d} {t}' for i,t in enumerate(out)))
    pickle.dump(dict(key=k, score=b), open('f122r_key.pkl','wb'))
    print('\n'.join(f'{i+1:2d} {t}' for i,t in enumerate(out)))
