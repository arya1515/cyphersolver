# Parallel many-restart driver. Usage: python par.py <kind> <arg> <restarts> <iters> <workers>
# kind=control -> arg=seed of control_match; kind=pairing -> arg=index into pairings.json
import sys,json,time,collections
from multiprocessing import Pool
import numpy as np
def build(kind,arg):
    if kind=='control':
        import control_match; toks,pl,key=control_match.make(int(arg)); return toks,pl,key
    if kind=='control_hx':
        import control_match,collections; toks,pl,key=control_match.make(int(arg)); c=collections.Counter(t for t in toks if t[0]!='#')
        toks=[('#'+t) if (t[0]!='#' and c[t]==1) else t for t in toks]; pl=''.join('#' if (t[0]=='#') else p for t,p in zip(toks,pl)); return toks,pl,key
    P=json.load(open('pairings.json')); toks=[t if t!='|' else '#|' for t in P[int(arg)]]
    if kind=='pairing_hx':
        import collections; c=collections.Counter(t for t in toks if t[0]!='#'); toks=[('#'+t) if (t[0]!='#' and c[t]==1) else t for t in toks]
    return toks,None,None
def work(args):
    kind,arg,seed,iters=args
    import seg
    toks,pl,key=build(kind,arg); syms,idx,W,free=seg.prep(toks)
    b,k=seg.anneal(idx,len(syms),W,free,iters=iters,T0=8.0,seed=seed)
    return b/len(W),seed,[int(v) for v in k]
if __name__=='__main__':
    kind,arg,restarts,iters,workers=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
    import seg
    toks,pl,key=build(kind,arg); syms,idx,W,free=seg.prep(toks)
    t=time.time()
    with Pool(workers) as p: res=p.map(work,[(kind,arg,1000+s,iters) for s in range(restarts)])
    res.sort(key=lambda r:-r[0])
    print(f'{kind} {arg}: {restarts} restarts x {iters}, {time.time()-t:.0f}s; top scores {[round(r[0],3) for r in res[:8]]}')
    if key:
        inv={v:k for k,vs in key.items() for v in vs}
        tk=np.array([seg.AL.index(inv[s.lstrip('#')]) if (s[0]!='#' and s in inv) or (s.lstrip('#') in inv) else 0 for s in syms]); print('true score',round(seg.score(tk,idx,W)/len(W),3))
    for sc,seed,k in res[:3]:
        k=np.array(k); dec=''.join('#' if syms[i][0]=='#' else seg.AL[k[i]] for i in idx)
        line=f'{sc:.3f} seed {seed}: {dec}'
        if pl: acc=sum(a==b for a,b in zip(dec,pl) if b!='#')/sum(1 for c in pl if c!='#'); line+=f'  acc={acc:.2f}'
        print(line)
    json.dump([(r[0],r[1],r[2]) for r in res[:20]],open(f'par_{kind}_{arg}.json','w'))
