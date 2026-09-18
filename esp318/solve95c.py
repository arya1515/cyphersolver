import pickle, numpy as np, sys, math, random, collections
from lm import ALPHA, IDX
from assign95 import CL2L
L=len(ALPHA)
src=sys.argv[1] if len(sys.argv)>1 else 'f122r_reseg.pkl'
seeds=int(sys.argv[2]) if len(sys.argv)>2 else 6; iters=int(sys.argv[3]) if len(sys.argv)>3 else 40000
# dense tables for orders 1..5 (interpolated), built from lm5.pkl counts
cnt=pickle.load(open('lm5.pkl','rb'))['cnt']
tot1=sum(cnt[1].values()); p1=np.array([(cnt[1].get(c,0)+1)/(tot1+L) for c in ALPHA])
tabs=[None,np.log(p1)]; prev=p1
for n in range(2,6):
    shape=(L,)*n; tab=np.zeros(shape)
    ctx_tot=collections.Counter(); ctx_ty=collections.Counter()
    for g,c in cnt[n].items(): ctx_tot[g[:-1]]+=c; ctx_ty[g[:-1]]+=1
    for ci in np.indices(shape[:-1]).reshape(n-1,-1).T:
        ctx=''.join(ALPHA[i] for i in ci); T=ctx_tot.get(ctx,0); ty=ctx_ty.get(ctx,0)
        lam=T/(T+ty) if T>0 else 0.0
        back=prev[tuple(ci[1:])] if n>2 else prev
        row=np.array([cnt[n].get(ctx+ch,0)/T for ch in ALPHA]) if T>0 else np.zeros(L)
        tab[tuple(ci)]=lam*row+(1-lam)*back
    prev=tab; tabs.append(np.log(tab))
lp1,lp2,lp3,lp4,lp5=tabs[1],tabs[2],tabs[3],tabs[4],tabs[5]
items=pickle.load(open(src,'rb'))
seq=np.array([t[2] for t in items]); lines=np.array([t[0] for t in items])
S=max(seq.max()+1,111)
gapmask=(seq==-1)
# runs of non-gap symbols; for each position, order = min(5, position-in-run+1)
runpos=np.zeros(len(seq),int); r=0
for i in range(len(seq)):
    r=0 if gapmask[i] else r+1; runpos[i]=r
order=np.minimum(runpos,5)
idx=np.arange(len(seq))
i5=idx[order==5]; i4=idx[order==4]; i3=idx[order==3]; i2=idx[order==2]; i1=idx[order==1]
print('positions scored by order 5/4/3/2/1:',len(i5),len(i4),len(i3),len(i2),len(i1),'gaps',gapmask.sum())
def score(key):
    d=key[np.maximum(seq,0)]
    s=lp5[d[i5-4],d[i5-3],d[i5-2],d[i5-1],d[i5]].sum()
    s+=lp4[d[i4-3],d[i4-2],d[i4-1],d[i4]].sum()
    s+=lp3[d[i3-2],d[i3-1],d[i3]].sum()
    s+=lp2[d[i2-1],d[i2]].sum()
    s+=lp1[d[i1]].sum()
    return s
fixed={c:IDX[l.lower()] for c,l in CL2L.items()}
present=[s for s in range(S) if (seq==s).any() and s!=-1]
free=[s for s in present if s not in fixed]
freq=collections.Counter(seq.tolist())
def anneal(seed,iters,unfix_pass=True):
    rng=random.Random(seed); key=np.zeros(S,int)
    for s in range(S): key[s]=fixed.get(s,rng.randrange(L))
    def run(movable,T0,T1,iters):
        nonlocal key
        cur=score(key); best=cur; bk=key.copy()
        for it in range(iters):
            T=T0*(T1/T0)**(it/iters); s=rng.choice(movable); old=key[s]; key[s]=rng.randrange(L)
            if key[s]==old: continue
            new=score(key)
            if new>=cur or rng.random()<math.exp((new-cur)/T): cur=new
            else: key[s]=old
            if cur>best: best,bk=cur,key.copy()
        key=bk.copy(); return best
    b=run(free,2.0,0.05,iters)
    if unfix_pass: b=run(present,0.3,0.02,iters//2)
    return b,key.copy()
res=[]
for sd in range(seeds):
    b,k=anneal(sd,iters); res.append((b,k)); print('seed',sd,round(b,1),flush=True)
b,k=max(res,key=lambda r:r[0]); nsc=len(i5)+len(i4)+len(i3)+len(i2)+len(i1)
print('best',round(b,1),'per scored symbol',round(b/nsc,3))
changed={s:(ALPHA[fixed[s]],ALPHA[k[s]]) for s in fixed if k[s]!=fixed[s] and (seq==s).any()}
print('fixed clusters the unfix pass changed:',changed)
agree={s:(ALPHA[k[s]],sum(ALPHA[r[1][s]]==ALPHA[k[s]] for r in res),freq[s]) for s in free}
print('free (letter, agree/%d, n):'%seeds,dict(sorted(agree.items(),key=lambda t:-t[1][2])))
dec=''.join('.' if s==-1 else ALPHA[k[s]] for s in seq)
out=[]; pos=0
for ln in sorted(set(lines.tolist())):
    n=(lines==ln).sum(); out.append(dec[pos:pos+n]); pos+=n
open(src.replace('.pkl','_solved.txt'),'w').write('\n'.join('%2d %s'%(i+1,t) for i,t in enumerate(out)))
pickle.dump(dict(key=k,score=b),open(src.replace('.pkl','_key.pkl'),'wb'))
print('\n'.join('%2d %s'%(i+1,t) for i,t in enumerate(out)))
