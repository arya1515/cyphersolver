# Stage-2 annealing under charLM + WW * word-segmentation score, seeded from saved par.py keys. Incremental word scoring per chunk.
import sys,json,math,time,numpy as np,seg,wordscore,par
from multiprocessing import Pool
def chunks_of(toks):
    # list of (list of token positions) between breaks
    out=[];cur=[]
    for i,t in enumerate(toks):
        if t[0]=='#':
            if cur: out.append(cur); cur=[]
        else: cur.append(i)
    if cur: out.append(cur)
    return out
def wchunk(text): return wordscore.score(text)[0]
def run(args):
    kind,arg,seed,k0,iters,WW,T0=args
    rnd=np.random.default_rng(seed)
    toks,pl,key=par.build(kind,arg); syms,idx,W,free=seg.prep(toks)
    ch=chunks_of(toks); sym2ch={}
    for ci,pos in enumerate(ch):
        for p in pos: sym2ch.setdefault(idx[p],set()).add(ci)
    k=np.array(k0)
    def ctext(ci,k): return ''.join(seg.AL[k[idx[p]]] for p in ch[ci])
    ws=[wchunk(ctext(ci,k)) for ci in range(len(ch))]
    cur=seg.score(k,idx,W,lam=0.0)+WW*sum(ws); best=cur; bestk=k.copy(); lam=math.log(0.05/T0)/iters
    free=np.array(free)
    for it in range(iters):
        T=T0*math.exp(lam*it); k2=k.copy(); r=rnd.random()
        if r<0.7:
            s=free[rnd.integers(len(free))]; k2[s]=seg.LET[rnd.integers(len(seg.LET))]; changed={s}
        else:
            a,b=rnd.choice(free,2,replace=False); k2[a],k2[b]=k2[b],k2[a]; changed={a,b}
        aff=set().union(*(sym2ch.get(s,set()) for s in changed))
        ws2=dict(); 
        for ci in aff: ws2[ci]=wchunk(ctext(ci,k2))
        sc=seg.score(k2,idx,W,lam=0.0)+WW*(sum(ws)-sum(ws[ci] for ci in aff)+sum(ws2.values()))
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            k=k2; cur=sc
            for ci,v in ws2.items(): ws[ci]=v
            if cur>best: best=cur; bestk=k.copy()
    k=bestk; dec=''.join('#' if syms[i][0]=='#' else seg.AL[k[i]] for i in idx)
    acc=None
    if pl: acc=sum(a==b for a,b in zip(dec,pl) if b!='#')/sum(1 for c in pl if c!='#')
    n=len(dec.replace('#','')); c=seg.score(k,idx,W,lam=0.0)/len(W); w=wordscore.score(dec)
    return best/n,c,w[0]/n,acc,seed,dec,w[1],[int(v) for v in k]
if __name__=='__main__':
    kind,arg=sys.argv[1],sys.argv[2]; topn=int(sys.argv[3]); iters=int(sys.argv[4]); WW=float(sys.argv[5]); T0=float(sys.argv[6]); workers=int(sys.argv[7])
    res=json.load(open(f'par_{kind}_{arg}.json'))[:topn]
    jobs=[(kind,arg,5000+i,k,iters,WW,T0) for i,(sc,seed,k) in enumerate(res)]
    t=time.time()
    with Pool(workers) as p: out=p.map(run,jobs)
    out.sort(key=lambda r:-r[0])
    print(f'{kind} {arg}: {len(jobs)} seeds x {iters} iters, WW={WW} T0={T0}, {time.time()-t:.0f}s')
    for b,c,w,acc,seed,dec,segm,k in out[:5]:
        print(f'combined {b:.3f} char {c:.3f} word {w:.2f} acc={acc} | {segm[:160]}')
    json.dump([(r[0],r[4],r[7]) for r in out],open(f'a2_{kind}_{arg}.json','w'))
