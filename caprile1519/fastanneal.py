"""Fast homophonic anneal: token->letter, vectorised n-gram score + unigram KL penalty."""
import sys, os, math, random, numpy as np
sys.path.insert(0, r'C:\Users\dbour\cypher\.worktrees\bonzagni1512')
from lang import lm
from anneal import runs
ORDER=int(os.environ.get('ORDER','4')); KLW=float(os.environ.get('KLW','3'))
M=lm.load('it-cinquecento',order=ORDER,spaces=False)
A=M.A; lp=M.lp
IT='eaoinlrtscdpumghfbqz'
F=np.array([11.8,11.7,9.8,10.1,6.9,6.5,6.4,5.6,5.0,4.5,3.7,3.0,5.1,2.5,1.6,1.1,1.0,0.9,0.5,0.9]);F/=F.sum()
letters=[M.index[c] for c in IT]
freq=np.full(A,0.002);freq[letters]=F
def setup(seqs):
    toks=sorted({t for s in seqs for t in s}); ti={t:i for i,t in enumerate(toks)}
    x=np.concatenate([np.array([ti[t] for t in s]) for s in seqs])
    cnt=np.bincount(x,minlength=len(toks)).astype(float)
    return toks,x,cnt
def score(key,x,cnt,N):
    y=key[x]; k=ORDER
    ctx=np.zeros(len(y)-k+1,dtype=np.int64)
    for j in range(k): ctx=ctx*A+y[j:len(y)-k+1+j]
    s=lp[ctx].sum()
    obs=np.bincount(key,weights=cnt,minlength=A)/N
    m=obs>0
    return s-KLW*N*float((obs[m]*np.log(obs[m]/freq[m])).sum())
def run(seqs,iters=200000,restarts=30,seed=1,fixed=None):
    toks,x,cnt=setup(seqs);N=cnt.sum();rnd=random.Random(seed);best=None
    for r in range(restarts):
        key=np.array([rnd.choice(letters) for _ in toks])
        if fixed:
            for t,c in fixed.items():
                if t in toks: key[toks.index(t)]=M.index[c]
        free=[i for i,t in enumerate(toks) if not fixed or t not in fixed]
        cur=score(key,x,cnt,N);T=15.0
        for it in range(iters):
            i=rnd.choice(free);old=key[i];key[i]=rnd.choice(letters)
            s=score(key,x,cnt,N)
            if s>=cur or rnd.random()<math.exp((s-cur)/T): cur=s
            else: key[i]=old
            T=max(0.3,T*0.99995)
        if best is None or cur>best[0]: best=(cur,key.copy())
        print(r,round(cur,1),flush=True)
    return best,toks
if __name__=='__main__':
    seqs=runs(sys.argv[1]);it=int(sys.argv[2]);rs=int(sys.argv[3])
    (sc,key),toks=run(seqs,it,rs)
    print('best',sc);print({t:M.alpha[k] for t,k in zip(toks,key)})
    ti={t:i for i,t in enumerate(toks)}
    for s in seqs: print(''.join(M.alpha[key[ti[t]]] for t in s))
