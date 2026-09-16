import sys,json,time,numpy as np,seg,par
from multiprocessing import Pool
def work(a):
    kind,arg,seed,iters=a
    toks,pl,key=par.build(kind,arg); syms,idx,W,free=seg.prep(toks)
    b,k=seg.anneal(idx,len(syms),W,free,iters=iters,T0=8.0,Tend=0.05,seed=seed)
    dec=''.join('#' if syms[i][0]=='#' else seg.AL[k[i]] for i in idx)
    acc=None
    if pl: acc=sum(x==y for x,y in zip(dec,pl) if y!='#')/sum(1 for c in pl if c!='#')
    return kind,arg,seed,b/len(W),acc,dec
if __name__=='__main__':
    iters=int(sys.argv[1]); jobs=[('control','0',s,iters) for s in (11,12,13)]+[('pairing','0',s,iters) for s in (11,12,13)]
    t=time.time()
    with Pool(6) as p:
        for kind,arg,seed,sc,acc,dec in p.imap_unordered(work,jobs):
            print(f'{kind} {arg} seed {seed}: {sc:.3f} acc={acc} {dec[:150]} ({time.time()-t:.0f}s)',flush=True)
