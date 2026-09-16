import random,math,pickle,sys,collections,json
from lm import LM
counts=pickle.load(open('lm5.pkl','rb')); lm=LM(counts)
AL='abcdefghijklmnopqrstuvwxyz'
def load_ct(path='elizabeth_moray.txt'):
    t=open(path).read()
    return [x for line in t.splitlines() if not line.startswith('#') for x in line.strip().split(';') if x]
def decode(ct,key): return ''.join(key[s] for s in ct)
def anneal(ct,syms,iters=40000,T0=3.0,seed=None,fixed=None):
    rnd=random.Random(seed)
    key={s:rnd.choice(AL) for s in syms}
    if fixed: key.update(fixed)
    free=[s for s in syms if not fixed or s not in fixed]
    cur=lm.score(decode(ct,key)); best=cur; bestkey=dict(key)
    for it in range(iters):
        T=T0*(1-it/iters)+0.05
        k2=dict(key)
        if rnd.random()<0.7:
            s=rnd.choice(free); k2[s]=rnd.choice(AL)
        else:
            a,b=rnd.sample(free,2); k2[a],k2[b]=k2[b],k2[a]
        sc=lm.score(decode(ct,k2))
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            key,cur=k2,sc
            if cur>best: best,bestkey=cur,dict(key)
    return best,bestkey
if __name__=='__main__':
    ct=load_ct(sys.argv[1] if len(sys.argv)>1 else 'elizabeth_moray.txt')
    n=int(sys.argv[2]) if len(sys.argv)>2 else 40
    syms=sorted(set(ct))
    res=[]
    for r in range(n):
        b,k=anneal(ct,syms,seed=r)
        res.append((b,k)); print(r,round(b,1),decode(ct,k),flush=True)
    res.sort(key=lambda x:-x[0])
    print('BEST',res[0][0]); print(decode(ct,res[0][1]))
    print(json.dumps(res[0][1],sort_keys=True))
    # consensus over top 10
    top=res[:10]
    for s in syms:
        c=collections.Counter(k[s] for _,k in top)
        print(s,c.most_common(3))
