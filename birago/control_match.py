# Control matched to the target's token profile: 228 letter tokens, ~62 distinct two-digit symbols (vowels 5-7 homophones,
# common consonants 2-3, rare 1), 16 code groups, 9 inline signs, Italian diplomatic text.
import random,collections,json,sys
def make(seed):
    rnd=random.Random(seed); txt=open('corpus_clean.txt').read()
    alloc={'a':6,'e':7,'i':6,'o':6,'u':3,'n':3,'r':3,'s':3,'t':3,'l':3,'c':2,'d':2,'m':2,'p':2,'g':1,'b':1,'f':1,'h':1,'q':1,'z':1}
    pool=[f'{i:02d}' for i in range(100)]; rnd.shuffle(pool); key={}; pi=0
    for L,k in alloc.items(): key[L]=pool[pi:pi+k]; pi+=k
    i=rnd.randrange(2500000,len(txt)-2000); p=txt[i:i+1200]
    out=[];plain=[]
    for ch in p:
        if ch not in key: continue
        out.append(rnd.choice(key[ch])); plain.append(ch)
        if len(out)>=228: break
    pos=sorted(rnd.sample(range(len(out)),25)); ins={}
    for q,ps in enumerate(pos): ins[ps]='#'+f'{rnd.randrange(100):02d}'+rnd.choice('-.:+') if q<16 else '#|'
    toks=[];pl=[]
    for q,(t,c) in enumerate(zip(out,plain)):
        if q in ins: toks.append(ins[q]); pl.append('#')
        toks.append(t); pl.append(c)
    return toks,''.join(pl),key
if __name__=='__main__':
    import seg,time
    restarts,iters=int(sys.argv[1]),int(sys.argv[2])
    seeds=[int(x) for x in sys.argv[3].split(',')]
    for seed in seeds:
        toks,pl,key=make(seed); c=collections.Counter(t for t in toks if t[0]!='#')
        t=time.time(); r=seg.solve(toks,restarts=restarts,iters=iters)
        acc=sum(a==b for a,b in zip(r[1],pl) if b!='#')/sum(1 for ch in pl if ch!='#')
        # true key score
        import numpy as np
        syms,idx,W,free=seg.prep(toks)
        inv={v:k for k,vs in key.items() for v in vs}
        tk=np.array([seg.AL.index(inv[s]) if s[0]!='#' else 0 for s in syms])
        print(f'seed={seed} distinct={len(c)} hapax={sum(1 for v in c.values() if v==1)} true={seg.score(tk,idx,W)/len(W):.3f} found={r[0]:.3f} acc={acc:.2f} {r[1][:70]} ({time.time()-t:.0f}s)',flush=True)
