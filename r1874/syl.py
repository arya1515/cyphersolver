import sys,random,math,json,numpy as np
sys.path.insert(0,'..'); from lang import lm
from seg import seq
m=lm.load('it-cinquecento',order=5,spaces=False); A=m.A; k=5; lp=m.lp
units=[u for _,u in seq if u.isdigit()]
types=sorted(set(units)); ti={t:i for i,t in enumerate(types)}
x=[ti[u] for u in units]
V='aeiou'; C='bcdfglmnprstuz'
cands=list('abcdefghilmnopqrstuz')+[c+v for c in C for v in V]+['qu','ch','gl','gn','che','chi','per','non','di','del','con','ne','il','et','la','le','li']
cands=list(dict.fromkeys(cands))
enc=[m.encode(c) for c in cands]
W=A**np.arange(k-1,-1,-1)
BETA=float(sys.argv[3]) if len(sys.argv)>3 else 2.2
def score(key):
    y=np.concatenate([enc[key[i]] for i in x]); n=len(y)-k+1
    idx=np.arange(n)[:,None]+np.arange(k)[None,:]
    return float(lp[(y[idx]*W).sum(1)].sum())+BETA*len(y), y
seed=int(sys.argv[1]); NIT=int(sys.argv[2]); rng=random.Random(seed)
key=[rng.randrange(20) for _ in types]; S,_=score(key); best=(S,list(key)); T=20.0
for it in range(NIT):
    i=rng.randrange(len(types)); old=key[i]; key[i]=rng.randrange(len(cands)) if rng.random()<0.5 else rng.randrange(20)
    S2,_=score(key); d=S2-S
    if d>=0 or rng.random()<math.exp(d/T): S=S2
    else: key[i]=old
    T=max(0.3,20*(1-it/NIT))
    if S>best[0]: best=(S,list(key))
    if it%100000==0: print(it,round(S,1),flush=True)
key=best[1]; print('FINAL',best[0]); print(''.join(cands[key[i]] for i in x))
json.dump({t:cands[key[i]] for i,t in enumerate(types)},open(f'syl_{seed}.json','w'))
