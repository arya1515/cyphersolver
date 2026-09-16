# Second stage: long anneals for a given segmentation rule; letters as null / symbol / break; optional 1xx tokens.
import sys,json,collections,numpy as np,seg
def run(src,S,U='',three1=False,letters='null',restarts=8,iters=200000,seed0=0,fixed=None):
    u=seg.units(open(src).read()); toks=seg.parse(u,set(S),set(U),three1,letters)
    syms,idx,W,free=seg.prep(toks)
    fx=None
    if fixed: fx={syms.index(k):seg.AL.index(v) for k,v in fixed.items() if k in syms}
    results=[]
    for r in range(restarts):
        b,k=seg.anneal(idx,len(syms),W,free,iters=iters,T0=8.0,seed=seed0+r,fixed=fx)
        results.append((b,k))
    results.sort(key=lambda t:-t[0])
    b,k=results[0]
    lm=seg.score(k,idx,W,lam=0.0)/len(W)
    dec=[('#'+syms[i][1:]) if syms[i][0]=='#' else seg.AL[k[i]] for i in idx]
    key={syms[i]:seg.AL[k[i]] for i in free}
    cnt=collections.Counter(t for t in toks if t[0]!='#')
    return dict(score=b/len(W),lm=lm,windows=len(W),nsym=len(syms),dec=''.join(dec),key=key,count=dict(cnt),toks=toks,scores=[round(x[0]/len(W),3) for x,_ in [(t,0) for t in results]])
if __name__=='__main__':
    src=sys.argv[1]; S=sys.argv[2].replace('-',''); U=sys.argv[3].replace('-','') if len(sys.argv)>3 else ''
    for letters in ('null','sym'):
        for three1 in (False,True):
            r=run(src,S,U,three1,letters,restarts=int(sys.argv[4]) if len(sys.argv)>4 else 6)
            print(f'letters={letters} three1={three1} score={r["score"]:.3f} lm={r["lm"]:.3f} win={r["windows"]} nsym={r["nsym"]} restarts={r["scores"]}')
            print(r['dec']); print(json.dumps(r['key'],sort_keys=True)); print(flush=True)
