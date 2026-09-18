"""Tune the iterated local search against controls with known keys."""
import re, random, sys, collections
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])
from search import ils, sweep

P0=Problem(); seglens=[len(g) for g in P0.segs]; nsym=P0.ns
txt=open('src/corpus_fr.txt',encoding='utf-8',errors='replace').read().lower()
txt=re.sub(r'[^a-z]',' ',txt).translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
txt=''.join(txt.split())

def make(seed):
    rnd=random.Random(seed)
    p=rnd.randrange(len(txt)-5000)
    pt=txt[p:p+sum(seglens)]
    order=sorted(range(NA), key=lambda i:-FREQ[i])
    slots=[order[i%NA] for i in range(nsym)]; rnd.shuffle(slots)
    homo=collections.defaultdict(list)
    for si,li in enumerate(slots): homo[li].append(si)
    for li in range(NA):
        if not homo[li]: homo[li]=[rnd.randrange(nsym)]
    ct=[rnd.choice(homo[AI[ch]]) for ch in pt]
    return pt, ct, slots

def mkP(ct):
    class Pc: pass
    Q=Pc(); Q.ns=nsym; Q.syms=[str(i) for i in range(nsym)]; Q.idx={str(i):i for i in range(nsym)}
    Q.iseg=[]; k=0
    for L in seglens: Q.iseg.append(ct[k:k+L]); k+=L
    Q.segs=Q.iseg; Q.flat=[]; Q.win=[]
    for g in Q.iseg:
        st=len(Q.flat); Q.flat.extend(g)
        for i in range(len(g)-3): Q.win.append((st+i,st+i+1,st+i+2,st+i+3))
    Q.nf=len(Q.flat)
    Q.sympos=[[] for _ in range(nsym)]
    for p,si in enumerate(Q.flat): Q.sympos[si].append(p)
    winof=[[] for _ in range(Q.nf)]
    for wi,w in enumerate(Q.win):
        for p in w: winof[p].append(wi)
    Q.symwin=[sorted({wi for p in Q.sympos[s] for wi in winof[p]}) for s in range(nsym)]
    Q.cnt=collections.Counter(Q.flat)
    Q.full=lambda key,mu=0.0: Problem.full(Q,key,mu)
    return Q

import time
for mu in (0.0, 2.0):
    for seed in (21,22,23):
        pt,ct,slots=make(seed); Q=mkP(ct)
        t=time.time()
        b,key=ils(Q,State,NA,iters=300,kick=4,mu=mu,seed=seed,FREQ=FREQ)
        raw,_=Q.full(key); traw,_=Q.full(slots)
        dec=''.join(AL[key[si]] for si in Q.flat)
        acc=sum(1 for x,y in zip(dec,pt) if x==y)/len(pt)
        print(f'mu={mu} seed {seed}: raw {raw:.4f}  TRUE {traw:.4f}  acc {acc*100:5.1f}%  {time.time()-t:.0f}s')
        print(f'   found: {dec[:110]}')
        print(f'   truth: {pt[:110]}')
