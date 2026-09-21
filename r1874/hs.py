import sys,random,math,json,numpy as np
sys.path.insert(0,'..'); from lang import lm
from seg import seq
m=lm.load('it-cinquecento',order=5,spaces=False); alpha=m.alpha; A=len(alpha); k=5; lp=m.lp
units=[u for _,u in seq if u.isdigit()]
types=sorted(set(units)); ti={t:i for i,t in enumerate(types)}
x=np.array([ti[u] for u in units]); N=len(x)
pos=[np.where(x==i)[0] for i in range(len(types))]
# ngram start indices affected by each type
aff=[np.unique(np.clip((p[:,None]-np.arange(k)[None,:]).ravel(),0,N-k)) for p in pos]
W=A**np.arange(k-1,-1,-1)
F=dict(a=11.7,b=0.9,c=4.5,d=3.7,e=11.8,f=1.0,g=1.6,h=1.5,i=10.1,l=6.5,m=2.5,n=6.9,o=9.8,p=3.0,q=0.5,r=6.4,s=5.0,t=5.6,u=3.4,z=0.5)
exp=np.array([F.get(c,0.02) for c in alpha]); exp=exp/exp.sum()*N
cnt_t=np.bincount(x,minlength=len(types))
def ng(y,st):
    idx=st[:,None]+np.arange(k)[None,:]; return lp[(y[idx]*W).sum(1)].sum()
def pen(o): return 2.0*float(((o-exp)**2/(exp+5)).sum())
seed=int(sys.argv[1]); NIT=int(sys.argv[2]); rng=random.Random(seed)
key=np.array([rng.choice([alpha.index(c) for c in 'aeiostnrl']) for _ in types])
y=key[x]; o=np.bincount(y,minlength=A).astype(float)
S=ng(y,np.arange(N-k+1))-pen(o); T=15.0; best=(S,key.copy())
for it in range(NIT):
    i=rng.randrange(len(types)); old=key[i]; new=rng.randrange(A)
    if new==old: continue
    st=aff[i]; before=ng(y,st)
    y[pos[i]]=new; after=ng(y,st)
    o2=o.copy(); o2[old]-=cnt_t[i]; o2[new]+=cnt_t[i]
    d=after-before-pen(o2)+pen(o)
    if d>=0 or rng.random()<math.exp(d/T): key[i]=new; o=o2; S+=d
    else: y[pos[i]]=old
    T=max(0.2,15.0*(1-it/NIT))
    if S>best[0]: best=(S,key.copy())
    if it%500000==0: print(it,round(S/N,3),''.join(alpha[c] for c in y[:150]),flush=True)
key=best[1]; txt=''.join(alpha[c] for c in key[x])
print('FINAL',round(best[0]/N,3)); print(txt)
json.dump({t:alpha[key[i]] for i,t in enumerate(types)},open(f'hs_{seed}.json','w'))
