# two-stage: 5-gram anneal, then polish with 5-gram + word-segmentation score
import numpy as np,math,sys,json,collections
import ng5, wordscore
from solve3 import load_ct,anneal,AL
tab=ng5.load()
LAM=1.0
def comb(p):
    s=''.join(AL[i] for i in p)
    return ng5.score(tab,p)+LAM*wordscore.score(s)
def polish(ctidx,key,free,iters=15000,T0=3.0,Tend=0.1,seed=0):
    rnd=np.random.default_rng(seed); key=key.copy()
    cur=comb(key[ctidx]); best=cur; bestkey=key.copy(); lam=math.log(Tend/T0)/iters
    for it in range(iters):
        T=T0*math.exp(lam*it); k2=key.copy()
        if rnd.random()<0.75: k2[free[rnd.integers(len(free))]]=rnd.integers(26)
        else:
            a,b=rnd.choice(free,2,replace=False); k2[a],k2[b]=k2[b],k2[a]
        sc=comb(k2[ctidx])
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            key,cur=k2,sc
            if cur>best: best,bestkey=cur,key.copy()
    return best,bestkey
def run(ct,restarts=8,fixed=None,verbose=True):
    syms=sorted(set(ct)); si={s:i for i,s in enumerate(syms)}; ctidx=np.array([si[s] for s in ct])
    fx={si[s]:AL.index(l) for s,l in (fixed or {}).items()}
    free=[i for i in range(len(syms)) if i not in fx]
    res=[]
    for r in range(restarts):
        b,k=anneal(ctidx,len(syms),iters=200000,seed=r,fixed=fx)
        b2,k2=polish(ctidx,k,free,seed=r)
        dec=''.join(AL[i] for i in k2[ctidx])
        res.append((b2,dec,{s:AL[k2[si[s]]] for s in syms},b))
        if verbose: print(r,round(b2,1),round(b,1),dec,'|',wordscore.segment(dec),flush=True)
    res.sort(key=lambda x:-x[0]); return res
if __name__=='__main__':
    ct=load_ct(sys.argv[1]); n=int(sys.argv[2]) if len(sys.argv)>2 else 8
    fixed=json.loads(sys.argv[3]) if len(sys.argv)>3 else None
    res=run(ct,n,fixed)
    print('BEST',res[0][0]); print(res[0][1]); print(wordscore.segment(res[0][1])); print(json.dumps(res[0][2],sort_keys=True))
