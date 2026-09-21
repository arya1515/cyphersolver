import re,sys,random,math,os
sys.path.insert(0,'..')
from lang import lm
import numpy as np
M=lm.load('it-cinquecento',order=int(os.environ.get('ORD','4')),spaces=False)
A='abcdefghilmnopqrstuxz'
def load(fn):
    t=open(fn).read(); t=re.sub(r'#.*','',t); t=re.sub(r'\{.*?\}',' / ',t)
    return [x for x in t.split() if x not in '|.?']
def solve(toks,restarts=10,iters=30000,seed=0):
    syms=sorted(set(toks),key=lambda s:-toks.count(s))
    segs=[];cur=[]
    for x in toks:
        if x=='/': segs.append(cur);cur=[]
        else: cur.append(x)
    segs.append(cur)
    idx={s:i for i,s in enumerate(syms)}
    segi=[np.array([idx[x] for x in s]) for s in segs if s]
    def sc(key):
        L=np.array([M.encode(c)[0] for c in key]) if False else None
        return sum(M.score_idx(M.encode(''.join(key[i] for i in s))) for s in segi)
    best=(-1e9,None); rng=random.Random(seed)
    freq='eaionlrtscdupmvgbfhqzx'.replace('v','')
    for r in range(restarts):
        key=list((freq*3)[:len(syms)]) if r==0 else [rng.choice(A) for _ in syms]
        cur=sc(key);T=4.0
        for it in range(iters):
            k=key[:]
            if rng.random()<.5:
                i,j=rng.sample(range(len(syms)),2);k[i],k[j]=k[j],k[i]
            else: k[rng.randrange(len(syms))]=rng.choice(A)
            n=sc(k)
            if n>cur or rng.random()<math.exp((n-cur)/T): key,cur=k,n
            T=max(.1,T*.9997)
        if cur>best[0]: best=(cur,key[:])
        print(r,round(cur,1),' / '.join(''.join(key[i] for i in s) for s in segi)[:300],flush=True)
    return syms,best
if __name__=='__main__':
    syms,b=solve(load(sys.argv[1]),int(sys.argv[2]))
    print(dict(zip(syms,b[1])))
