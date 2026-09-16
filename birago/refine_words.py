# Stage 2: from the saved top keys of par.py, hill-climb single-symbol reassignments under charLM + WW*wordscore.
import sys,json,numpy as np,seg,wordscore,par
kind,arg=sys.argv[1],sys.argv[2]; WW=float(sys.argv[3]) if len(sys.argv)>3 else 1.0; topn=int(sys.argv[4]) if len(sys.argv)>4 else 5
toks,pl,key=par.build(kind,arg); syms,idx,W,free=seg.prep(toks)
def render(k): return ''.join('#' if syms[i][0]=='#' else seg.AL[k[i]] for i in idx)
def total(k):
    return seg.score(k,idx,W,lam=0.0)+WW*wordscore.score(render(k))[0]
res=json.load(open(f'par_{kind}_{arg}.json'))
out=[]
for sc0,seed,k in res[:topn]:
    k=np.array(k); cur=total(k); improved=True
    while improved:
        improved=False
        for s in free:
            old=k[s]; best=(cur,old)
            for L in seg.LET:
                if L==old: continue
                k[s]=L; t=total(k)
                if t>best[0]: best=(t,L)
            k[s]=best[1]
            if best[0]>cur+1e-9: cur=best[0]; improved=True
    dec=render(k); ws,segm=wordscore.score(dec)
    line=f'seed {seed}: char {seg.score(k,idx,W,lam=0.0)/len(W):.3f} word {ws/len(dec.replace("#","")):.2f} | {segm}'
    if pl: acc=sum(a==b for a,b in zip(dec,pl) if b!='#')/sum(1 for c in pl if c!='#'); line+=f' | acc={acc:.2f}'
    print(line,flush=True); out.append((cur,seed,[int(v) for v in k]))
json.dump(sorted(out,key=lambda r:-r[0]),open(f'refined_{kind}_{arg}.json','w'))
