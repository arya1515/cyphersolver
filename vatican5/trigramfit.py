"""Trigram version of bigramfit: SA over partitions of 21 letters into 9 digits (4=null), objective = multinomial LL of
observed digit trigrams under the grouped Italian letter-trigram distribution (boundary = word space)."""
import json, math, random, sys
import numpy as np
from parse5 import load, digit_stream
AL='abcdefghilmnopqrstuvz'; LI={c:i for i,c in enumerate(AL)}; B=len(AL); N=B+1
ng=json.load(open('it_ngrams.json',encoding='utf-8'))
P3=np.full((N,N,N),1e-9)
for k,v in ng['3'].items():
    idx=[LI.get(ch, B if ch==' ' else None) for ch in k]
    if None in idx: continue
    P3[idx[0],idx[1],idx[2]]+=v
P3/=P3.sum()
runs=digit_stream(load()); digits=[0,1,2,3,5,6,7,8,9]
seq=[]  # digit ids with 4 -> boundary(4) and code positions -> None
for r in runs:
    for i,t in enumerate(r):
        d=t[0]; bad=('^' in t or '_' in t or '?' in t) or (i>0 and ('^' in r[i-1] or '_' in r[i-1]))
        seq.append(None if bad else int(d))
    seq.append(4)
C=np.zeros((10,10,10))
for a,b,c in zip(seq,seq[1:],seq[2:]):
    if None in (a,b,c): continue
    C[a,b,c]+=1
mask=C>0
def ll(assign):
    G=np.zeros((10,N)); G[4,B]=1
    for l,d in assign.items(): G[d,l]=1
    Q=np.einsum('ai,bj,ck,ijk->abc',G,G,G,P3); Q=Q/Q.sum()
    return float((C[mask]*np.log(Q[mask]+1e-12)).sum())
def show(assign):
    g={d:'' for d in digits}
    for l in sorted(assign,key=lambda x:AL[x]): g[assign[l]]+=AL[l]
    return ' '.join(f'{d}={g[d]}' for d in digits)
def sa(rnd,iters):
    letters=list(range(B)); assign={l:rnd.choice(digits) for l in letters}
    cur=ll(assign); best=(cur,dict(assign)); T=40.0
    for it in range(iters):
        if rnd.random()<0.8:
            l=rnd.choice(letters); old=assign[l]; new=rnd.choice(digits)
            if new==old: continue
            assign[l]=new
            if sum(1 for x in assign.values() if x==old)==0: assign[l]=old; continue
            v=ll(assign)
            if v>cur or rnd.random()<math.exp((v-cur)/T): cur=v
            else: assign[l]=old
        else:
            l1,l2=rnd.sample(letters,2)
            if assign[l1]==assign[l2]: continue
            assign[l1],assign[l2]=assign[l2],assign[l1]; v=ll(assign)
            if v>cur or rnd.random()<math.exp((v-cur)/T): cur=v
            else: assign[l1],assign[l2]=assign[l2],assign[l1]
        if cur>best[0]: best=(cur,dict(assign))
        T=max(0.3,T*0.99993)
    return best
seed=int(sys.argv[1]) if len(sys.argv)>1 else 0; iters=int(sys.argv[2]) if len(sys.argv)>2 else 60000
for trial in range(4):
    rnd=random.Random(seed*10+trial); v,a=sa(rnd,iters); print(f'seed {seed} trial {trial}: {v:.1f}  {show(a)}', flush=True)
