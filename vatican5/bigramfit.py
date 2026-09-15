"""Fit a polyphonic single-digit key to the Vatican-5 digit bigram counts.
Model: plaintext letters ~ Italian bigram model; each letter maps to one digit; 4 = null (word end); dotted digit and
the digit after it are codes (treated as boundaries). Objective = multinomial log-likelihood of observed digit bigrams
under the grouped letter-bigram distribution.  (a) exhaustive over permutations of Meister key-1 groups;
(b) simulated annealing over free partitions of the alphabet into the 9 digits."""
import json, math, random, itertools, sys, collections
import numpy as np
from parse5 import load, digit_stream
AL='abcdefghilmnopqrstuvz'; LI={c:i for i,c in enumerate(AL)}; B=len(AL)  # index B = boundary
ng=json.load(open('it_ngrams.json',encoding='utf-8'))
P=np.full((B+1,B+1),1e-9)
for k,v in ng['2'].items():
    a,b=k[0],k[1]
    ia=LI.get(a,B if a==' ' else None); ib=LI.get(b,B if b==' ' else None)
    if ia is None or ib is None: continue
    P[ia,ib]+=v
P/=P.sum()
# cipher bigrams
runs=digit_stream(load())
DIG='0123456789'; C=np.zeros((10,10))
for r in runs:
    prev=None
    for i,t in enumerate(r):
        d=t[0]; dotted='^' in t or '_' in t
        after_dot = i>0 and ('^' in r[i-1] or '_' in r[i-1])
        if dotted or after_dot or d=='4' or '?' in t: prev=None; continue
        if prev is not None: C[int(prev),int(d)]+=1
        prev=d
digits=[0,1,2,3,5,6,7,8,9]
def ll(groups):  # groups: dict digit->list of letter indices (B for boundary-like)
    G=np.zeros((10,B+1))
    for d,ls in groups.items():
        for l in ls: G[d,l]=1
    Q=G@P@G.T; Q=Q/ Q.sum()
    Qn=Q+1e-12
    return float((C*np.log(Qn)).sum())
def show(groups):
    return ' '.join(f"{d}={''.join(AL[l] if l<B else '_' for l in sorted(groups[d]))}" for d in digits)
key1=[[LI['a'],LI['c']],[LI['e'],LI['u']],[LI['i'],LI['d']],[LI['o'],LI['t']],[LI['b'],LI['f'],LI['g']],[LI['l'],LI['n']],[LI['p'],LI['r'],LI['z']],[LI['m'],LI['s']],[B]]
best=[]
for perm in itertools.permutations(range(9)):
    groups={digits[i]:key1[perm[i]] for i in range(9)}
    best.append((ll(groups),perm))
best.sort(reverse=True)
print('--- key-1 groups, best permutations:')
for s,perm in best[:5]:
    groups={digits[i]:key1[perm[i]] for i in range(9)}; print(round(s,1), show(groups))
print('rank gap top1-top2:', round(best[0][0]-best[1][0],1), ' top1-top20:', round(best[0][0]-best[19][0],1))
# (b) free partition SA
rnd=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 1)
letters=list(range(B))
def sa(iters=200000):
    assign={l:rnd.choice(digits) for l in letters}
    def groups_of(a):
        g={d:[] for d in digits}
        for l,d in a.items(): g[d].append(l)
        return g
    cur=ll(groups_of(assign)); bestv=(cur,dict(assign)); T=50.0
    for it in range(iters):
        l=rnd.choice(letters); old=assign[l]; new=rnd.choice(digits)
        if new==old: continue
        assign[l]=new; g=groups_of(assign)
        if any(len(g[d])==0 for d in digits): assign[l]=old; continue
        v=ll(g)
        if v>cur or rnd.random()<math.exp((v-cur)/T): cur=v
        else: assign[l]=old
        if cur>bestv[0]: bestv=(cur,dict(assign))
        T=max(0.5,T*0.99997)
    return bestv
for trial in range(3):
    v,a=sa(60000)
    g={d:[] for d in digits}
    for l,d in a.items(): g[d].append(l)
    print('SA trial',trial,round(v,1),show(g))
