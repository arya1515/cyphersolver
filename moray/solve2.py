import numpy as np,random,math,sys,json,collections
import qg
tab=qg.load()
AL='abcdefghijklmnopqrstuvwxyz'
def load_ct(path):
    t=open(path).read()
    return [x for line in t.splitlines() if not line.startswith('#') for x in line.strip().split(';') if x]
def anneal(ctidx,nsym,iters=250000,T0=8.0,Tend=0.2,seed=0,fixed=None):
    rnd=np.random.default_rng(seed)
    key=rnd.integers(0,26,nsym)
    if fixed:
        for s,l in fixed.items(): key[s]=l
    free=[s for s in range(nsym) if not fixed or s not in fixed]
    p=key[ctidx]; cur=qg.score(tab,p); best=cur; bestkey=key.copy()
    lam=math.log(Tend/T0)/iters
    for it in range(iters):
        T=T0*math.exp(lam*it)
        k2=key.copy()
        if rnd.random()<0.75:
            s=free[rnd.integers(len(free))]; k2[s]=rnd.integers(26)
        else:
            a,b=rnd.choice(free,2,replace=False); k2[a],k2[b]=k2[b],k2[a]
        sc=qg.score(tab,k2[ctidx])
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            key,cur=k2,sc
            if cur>best: best,bestkey=cur,key.copy()
    return best,bestkey
def run(ct,restarts=30,fixed=None,verbose=True):
    syms=sorted(set(ct)); si={s:i for i,s in enumerate(syms)}
    ctidx=np.array([si[s] for s in ct])
    fx={si[s]:AL.index(l) for s,l in (fixed or {}).items()}
    res=[]
    for r in range(restarts):
        b,k=anneal(ctidx,len(syms),seed=r,fixed=fx)
        dec=''.join(AL[i] for i in k[ctidx])
        res.append((b,dec,{s:AL[k[si[s]]] for s in syms}))
        if verbose: print(r,round(b,1),dec,flush=True)
    res.sort(key=lambda x:-x[0])
    return res
if __name__=='__main__':
    ct=load_ct(sys.argv[1]); n=int(sys.argv[2]) if len(sys.argv)>2 else 30
    fixed=json.loads(sys.argv[3]) if len(sys.argv)>3 else None
    res=run(ct,n,fixed)
    print('BEST',res[0][0]); print(res[0][1]); print(json.dumps(res[0][2],sort_keys=True))
    syms=sorted(set(ct))
    for s in syms:
        c=collections.Counter(k[s] for _,_,k in res[:10]); print(s,c.most_common(3))
