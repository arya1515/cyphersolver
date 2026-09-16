# Consensus stage: from saved par.py keys, fix symbols whose letter agrees across the top-N optima, re-anneal the rest; iterate.
import sys,json,collections,numpy as np,seg,par
kind,arg=sys.argv[1],sys.argv[2]; topn=int(sys.argv[3]); thresh=float(sys.argv[4]); restarts=int(sys.argv[5]); iters=int(sys.argv[6])
toks,pl,key=par.build(kind,arg); syms,idx,W,free=seg.prep(toks)
res=json.load(open(f'par_{kind}_{arg}.json'))[:topn]
keys=[np.array(k) for sc,seed,k in res]
cnt=collections.Counter(t for t in toks if t[0]!='#'); si={s:i for i,s in enumerate(syms)}
fixed={}
for s in free:
    votes=collections.Counter(int(k[s]) for k in keys); L,v=votes.most_common(1)[0]
    if v/len(keys)>=thresh: fixed[s]=L
print(f'fixed {len(fixed)} of {len(free)} symbols at agreement >= {thresh}')
if pl:
    inv={v:k for k,vs in key.items() for v in vs}
    right=sum(1 for s,L in fixed.items() if seg.AL[L]==inv.get(syms[s].lstrip('#'),'?')); print('of which right',right)
best=None
for r in range(restarts):
    b,k=seg.anneal(idx,len(syms),W,free,iters=iters,T0=6.0,seed=700+r,fixed=fixed)
    if best is None or b>best[0]: best=(b,k)
b,k=best; dec=''.join('#' if syms[i][0]=='#' else seg.AL[k[i]] for i in idx)
line=f'score {b/len(W):.3f} {dec[:160]}'
if pl: line+=f' acc={sum(a==b_ for a,b_ in zip(dec,pl) if b_!="#")/sum(1 for c in pl if c!="#"):.2f}'
print(line)
