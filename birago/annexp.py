import seg,sys,time
from pairctl import toks_from_spaced
name=sys.argv[1]; iters=int(sys.argv[2]); T0=float(sys.argv[3]); restarts=int(sys.argv[4])
toks=toks_from_spaced(f'{name}.txt'); pl=open(f'{name}_plain.txt').read()
syms,idx,W,free=seg.prep(toks)
best=None
for r in range(restarts):
    t=time.time(); b,k=seg.anneal(idx,len(syms),W,free,iters=iters,T0=T0,seed=100+r)
    dec=''.join(seg.AL[k[i]] for i in idx)
    acc=sum(a==b_ for a,b_ in zip(dec,pl) if b_!='#')/sum(1 for c in pl if c!='#')
    print(f'{name} iters={iters} T0={T0} seed={100+r} score={b/len(W):.3f} acc={acc:.2f} {dec[:60]} ({time.time()-t:.0f}s)',flush=True)
