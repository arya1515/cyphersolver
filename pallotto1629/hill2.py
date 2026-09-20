import sys, random, math, numpy as np, json
sys.path.insert(0,'../../cypher-lang')
from lang import lm
from solve import load_doc
from collections import Counter
FREQ=dict(a=11.7,e=11.8,i=11.3,o=9.8,n=6.9,r=6.4,t=5.6,l=6.5,s=5.0,c=4.5,d=3.7,u=5.1,p=3.0,m=2.5,g=1.6,f=1.2,b=0.9,h=1.5,q=0.5,z=0.5)
def model():
    meta=json.load(open('it_clean5.json'))
    return lm.DenseLM(np.load('it_clean5.npy'),meta['order'],meta['alpha'],meta)
def stream(docs,k=2,phase=0):
    out=[]
    for d in docs:
        C,_=load_doc(d); out+=[C[i:i+k] for i in range(phase,len(C)-k+1,k)]
    return out
def multiset(n,A):
    tot=sum(FREQ.values()); out=[]
    for L,f in sorted(FREQ.items(), key=lambda x:-x[1]):
        out += [A.index(L)]*max(1,int(round(f/tot*n)))
    while len(out)<n: out.append(A.index('e'))
    return out[:n]
def solve(codes,M,iters=300000,restarts=5,seed=1):
    A=M.alpha; rng=random.Random(seed)
    vocab=sorted(set(codes)); idx={c:i for i,c in enumerate(vocab)}
    arr=np.array([idx[c] for c in codes],dtype=np.int64)
    cnt=Counter(codes); order=[c for c,_ in cnt.most_common()]
    ms=multiset(len(vocab),A)
    bestall=None
    for R in range(restarts):
        a=list(ms)
        if R: rng.shuffle(a)
        key=np.zeros(len(vocab),dtype=np.int64)
        for i,c in enumerate(order): key[idx[c]]=a[i]
        cur=M.score_idx(key[arr]); best=cur; bkey=key.copy()
        T0,T1=2.5,0.05
        for it in range(iters):
            T=T0*(T1/T0)**(it/iters)
            p=rng.randrange(len(vocab)); q=rng.randrange(len(vocab))
            if key[p]==key[q]: continue
            key[p],key[q]=key[q],key[p]
            s=M.score_idx(key[arr])
            if s>cur or rng.random()<math.exp((s-cur)/max(T,1e-9)):
                cur=s
                if s>best: best=s; bkey=key.copy()
            else: key[p],key[q]=key[q],key[p]
        print('  R',R,'best/char %.4f'%(best/len(arr)),flush=True)
        if bestall is None or best>bestall[0]: bestall=(best,bkey,vocab)
    return bestall
