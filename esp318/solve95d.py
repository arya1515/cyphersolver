import pickle, numpy as np, sys, math, random, collections
from lm import ALPHA, IDX, norm
from assign95 import CL2L
L=len(ALPHA)
src=sys.argv[1]; seeds=int(sys.argv[2]) if len(sys.argv)>2 else 6; iters=int(sys.argv[3]) if len(sys.argv)>3 else 40000
CAP={'e':10,'a':12,'o':10,'s':6,'n':6,'r':6,'i':6,'d':5,'l':5,'u':5,'c':5,'t':5,'m':6,'p':3,'b':3,'q':2,'g':3,'h':3,'y':3,'f':2,'x':2,'z':2}
if not __import__('os').path.exists('lm_tabs.pkl'):
    cnt=pickle.load(open('lm5.pkl','rb'))['cnt']
    tot1=sum(cnt[1].values()); p1=np.array([(cnt[1].get(c,0)+1)/(tot1+L) for c in ALPHA]); tabs=[None,np.log(p1)]; prev=p1
    for n in range(2,6):
        shape=(L,)*n; tab=np.zeros(shape); ct=collections.Counter(); ty=collections.Counter()
        for g,c in cnt[n].items(): ct[g[:-1]]+=c; ty[g[:-1]]+=1
        for ci in np.indices(shape[:-1]).reshape(n-1,-1).T:
            ctx=''.join(ALPHA[i] for i in ci); T=ct.get(ctx,0); t=ty.get(ctx,0); lam=T/(T+t) if T>0 else 0.0
            back=prev[tuple(ci[1:])] if n>2 else prev
            row=np.array([cnt[n].get(ctx+ch,0)/T for ch in ALPHA]) if T>0 else np.zeros(L)
            tab[tuple(ci)]=lam*row+(1-lam)*back
        prev=tab; tabs.append(np.log(tab))
    pickle.dump(tabs,open('lm_tabs.pkl','wb'))
tabs=pickle.load(open('lm_tabs.pkl','rb')); lp1,lp2,lp3,lp4,lp5=tabs[1:]
pexp=np.exp(lp1)
items=pickle.load(open(src,'rb')); seq=np.array([t[2] for t in items]); lines=np.array([t[0] for t in items])
S=max(seq.max()+1,111); gap=(seq==-1)
runpos=np.zeros(len(seq),int); r=0
for i in range(len(seq)): r=0 if gap[i] else r+1; runpos[i]=r
order=np.minimum(runpos,5); idx=np.arange(len(seq))
I=[idx[order==o] for o in range(6)]
N=sum(len(I[o]) for o in range(1,6)); print('scored positions',N,'gaps',gap.sum())
def score(key):
    d=key[np.maximum(seq,0)]
    s=lp5[d[I[5]-4],d[I[5]-3],d[I[5]-2],d[I[5]-1],d[I[5]]].sum()+lp4[d[I[4]-3],d[I[4]-2],d[I[4]-1],d[I[4]]].sum()
    s+=lp3[d[I[3]-2],d[I[3]-1],d[I[3]]].sum()+lp2[d[I[2]-1],d[I[2]]].sum()+lp1[d[I[1]]].sum()
    # letter-frequency prior: -N * KL(observed || spanish), weight 0.5
    obs=np.bincount(d[~gap],minlength=L)/max(1,(~gap).sum())
    kl=(obs*np.log(np.maximum(obs,1e-9)/pexp)).sum()
    return s-0.5*N*kl
fixed={c:IDX[l.lower()] for c,l in CL2L.items()}
present=[s for s in range(S) if (seq==s).any() and s!=-1]; free=[s for s in present if s not in fixed]
freq=collections.Counter(seq.tolist())
def anneal(seed):
    rng=random.Random(seed); key=np.zeros(S,int)
    for s in range(S): key[s]=fixed.get(s,rng.randrange(L))
    ncl=collections.Counter(ALPHA[key[s]] for s in present)
    cur=score(key); best=cur; bk=key.copy()
    for it in range(iters):
        T=2.0*(0.05/2.0)**(it/iters); s=rng.choice(free); old=key[s]; new_l=rng.randrange(L)
        if new_l==old or ncl[ALPHA[new_l]]>=CAP.get(ALPHA[new_l],4): continue
        key[s]=new_l; new=score(key)
        if new>=cur or rng.random()<math.exp((new-cur)/T): cur=new; ncl[ALPHA[old]]-=1; ncl[ALPHA[new_l]]+=1
        else: key[s]=old
        if cur>best: best,bk=cur,key.copy()
    return best,bk
res=[]
for sd in range(seeds): b,k=anneal(sd); res.append((b,k)); print('seed',sd,round(b,1),flush=True)
b,k=max(res,key=lambda r:r[0]); print('best',round(b,1),'per symbol',round(b/N,3))
init=np.array([fixed.get(s,0) for s in range(S)])
print('free (letter, agree/%d, n):'%seeds,dict(sorted({s:(ALPHA[k[s]],sum(ALPHA[r[1][s]]==ALPHA[k[s]] for r in res),freq[s]) for s in free}.items(),key=lambda t:-t[1][2])))
dec=''.join('.' if s==-1 else ALPHA[k[s]] for s in seq); out=[]; pos=0
for ln in sorted(set(lines.tolist())): n=(lines==ln).sum(); out.append(dec[pos:pos+n]); pos+=n
open(src.replace('.pkl','_solved.txt'),'w').write('\n'.join('%2d %s'%(i+1,t) for i,t in enumerate(out)))
pickle.dump(dict(key=k,score=b),open(src.replace('.pkl','_key.pkl'),'wb'))
print('\n'.join('%2d %s'%(i+1,t) for i,t in enumerate(out)))
