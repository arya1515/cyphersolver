# Search the cluster -> polyphonic class assignment that maximises the French 5-gram score of the beam-decoded text.
# usage: anneal_poly.py clusters.json "sep_clusters" "junk_clusters" iters restarts seed [maxlines]
import sys, json, random, math, time, numpy as np
from numba import njit
sys.path.insert(0, 'sp53')
from homo import ALPHA
K=len(ALPHA)
tab=np.load('sp53/fr5.npy')
PAIRS=['an','bo','cp','dq','er','fs','gt','hu','ix','ly','mz']
CODES=['que','qui','pour']
NCLS=len(PAIRS)+len(CODES)   # 14 ; class 14 = SEP (emit nothing)
# option table: for class c, up to 2 options, each a sequence of letter indices (max len 4)
opt_len=np.zeros((NCLS+1,2),np.int64); opt_seq=np.zeros((NCLS+1,2,4),np.int64); opt_n=np.zeros(NCLS+1,np.int64)
for c,p in enumerate(PAIRS):
    opt_n[c]=2
    for j,ch in enumerate(p): opt_len[c,j]=1; opt_seq[c,j,0]=ALPHA.index(ch)
for c,w in enumerate(CODES):
    cc=len(PAIRS)+c; opt_n[cc]=1; opt_len[cc,0]=len(w)
    for j,ch in enumerate(w): opt_seq[cc,0,j]=ALPHA.index(ch)
opt_n[NCLS]=0

@njit(cache=True)
def beam(tokens, mapping, tab, opt_n, opt_len, opt_seq, B):
    n=tokens.shape[0]
    # state: last 4 letters as codes (K^4), score
    st_ctx=np.zeros((B,4),np.int64); st_sc=np.zeros(B); nst=1
    for i in range(4): st_ctx[0,i]=4  # 'e' filler context
    new_ctx=np.zeros((2*B,4),np.int64); new_sc=np.zeros(2*B)
    total_letters=0
    for t in range(n):
        c=mapping[tokens[t]]
        no=opt_n[c]
        if no==0: continue
        m=0
        for s in range(nst):
            for o in range(no):
                ctx=st_ctx[s].copy(); sc=st_sc[s]
                for j in range(opt_len[c,o]):
                    ch=opt_seq[c,o,j]
                    sc+=tab[ctx[0],ctx[1],ctx[2],ctx[3],ch]
                    ctx[0]=ctx[1]; ctx[1]=ctx[2]; ctx[2]=ctx[3]; ctx[3]=ch
                new_ctx[m]=ctx; new_sc[m]=sc; m+=1
        total_letters+=opt_len[c,0]
        if m>B:
            idx=np.argsort(-new_sc[:m])[:B]
        else:
            idx=np.arange(m)
        nst=idx.shape[0]
        for s in range(nst):
            st_ctx[s]=new_ctx[idx[s]]; st_sc[s]=new_sc[idx[s]]
    best=-1e18
    for s in range(nst):
        if st_sc[s]>best: best=st_sc[s]
    return best, total_letters

def decode_text(tokens, mapping, B=400):
    # full beam with backpointers (python, once)
    beams=[('',0.0)]
    for t in tokens:
        c=mapping[t]
        if c==NCLS: beams=[(txt+' ',sc) for txt,sc in beams]; continue
        opts=[PAIRS[c][0],PAIRS[c][1]] if c<len(PAIRS) else [CODES[c-len(PAIRS)]]
        new=[]
        for txt,sc in beams:
            for o in opts:
                s2=sc; ctx=[ALPHA.index(ch) for ch in (txt.replace(' ','')[-4:]).rjust(4,'e')]
                for ch in o:
                    s2+=tab[ctx[0],ctx[1],ctx[2],ctx[3],ALPHA.index(ch)]; ctx=ctx[1:]+[ALPHA.index(ch)]
                new.append((txt+o,s2))
        new.sort(key=lambda x:-x[1]); beams=new[:B]
    return beams[0]

if __name__=='__main__':
    cl=json.load(open(sys.argv[1]))
    seps=set(int(x) for x in sys.argv[2].split(',') if x); junk=set(int(x) for x in sys.argv[3].split(',') if x)
    iters=int(sys.argv[4]); restarts=int(sys.argv[5]); seed=int(sys.argv[6]); maxl=int(sys.argv[7]) if len(sys.argv)>7 else 10**6
    toks=[]
    for k in sorted(cl,key=int)[:maxl]:
        toks+= [c for c in cl[k] if c not in junk]
    ncl=max(toks)+1
    tokens=np.array(toks,np.int64)
    free=[c for c in range(ncl) if c not in seps and c in set(toks)]
    rnd=random.Random(seed)
    EXP=np.array([0.1524,0.064,0.064,0.057,0.2301,0.0913,0.0824,0.088,0.082,0.0574,0.0315])
    LAM=float(__import__('os').environ.get('LAM','4.0'))
    counts=np.bincount(tokens,minlength=ncl).astype(float)
    nonsep=sum(counts[c] for c in free)
    def score(mp):
        s,nl=beam(tokens,mp,tab,opt_n,opt_len,opt_seq,64)
        f=np.zeros(NCLS+1)
        for c in free: f[mp[c]]+=counts[c]
        fp=f[:11]/max(1.0,f[:11].sum())
        pen=np.abs(fp-EXP).sum()
        return s-LAM*nonsep*pen
    best_all=None
    for r in range(restarts):
        mp=np.full(ncl,NCLS,np.int64)
        for c in free: mp[c]=rnd.randrange(len(PAIRS))
        cur=score(mp); best=cur; bestmp=mp.copy()
        T0,T1=3.0,0.05
        for it in range(iters):
            T=T0*(T1/T0)**(it/iters)
            mp2=mp.copy()
            c=rnd.choice(free)
            if rnd.random()<0.7: mp2[c]=rnd.randrange(NCLS)
            else:
                c2=rnd.choice(free); mp2[c],mp2[c2]=mp2[c2],mp2[c]
            s2=score(mp2)
            if s2>cur or rnd.random()<math.exp((s2-cur)/T):
                mp=mp2; cur=s2
                if cur>best: best=cur; bestmp=mp.copy()
        print(f'restart {r} best {best:.1f} per-token {best/len(tokens):.3f}',flush=True)
        if best_all is None or best>best_all[0]: best_all=(best,bestmp)
    best,mp=best_all
    txt,sc=decode_text(tokens,mp)
    print('BEST',round(best,1)); print(txt)
    print('MAP',{c:(PAIRS+CODES+['SEP'])[mp[c]] for c in range(ncl) if c in set(toks)})

@njit(cache=True)
def forward(tokens, mapping, tab, opt_n, opt_len, opt_seq):
    # exact log P(cipher | mapping) under the 5-gram LM, summing over letter choices.
    # state = last 4 emitted letters; at most 2^4 = 16 distinct states (plus code words fixed).
    n=tokens.shape[0]
    ctx=np.zeros((64,4),np.int64); lp=np.zeros(64); ns=1
    for i in range(4): ctx[0,i]=4
    nctx=np.zeros((64,4),np.int64); nlp=np.zeros(64)
    for t in range(n):
        c=mapping[tokens[t]]; no=opt_n[c]
        if no==0: continue
        m=0
        for s in range(ns):
            for o in range(no):
                cc=ctx[s].copy(); sc=lp[s]
                for j in range(opt_len[c,o]):
                    ch=opt_seq[c,o,j]
                    sc+=tab[cc[0],cc[1],cc[2],cc[3],ch]
                    cc[0]=cc[1]; cc[1]=cc[2]; cc[2]=cc[3]; cc[3]=ch
                # merge identical contexts
                found=-1
                for q in range(m):
                    if nctx[q,0]==cc[0] and nctx[q,1]==cc[1] and nctx[q,2]==cc[2] and nctx[q,3]==cc[3]:
                        found=q; break
                if found>=0:
                    a=nlp[found]; b=sc
                    if a>b: nlp[found]=a+np.log(1.0+np.exp(b-a))
                    else: nlp[found]=b+np.log(1.0+np.exp(a-b))
                else:
                    nctx[m]=cc; nlp[m]=sc; m+=1
        ns=m
        for s in range(ns):
            ctx[s]=nctx[s]; lp[s]=nlp[s]
    best=lp[0]
    for s in range(1,ns):
        a=best; b=lp[s]
        if a>b: best=a+np.log(1.0+np.exp(b-a))
        else: best=b+np.log(1.0+np.exp(a-b))
    return best

@njit(cache=True)
def beam_text(tokens, mapping, tab, opt_n, opt_len, opt_seq, B):
    # beam search returning the best letter sequence (as indices) and its score
    n=tokens.shape[0]
    maxlen=n*4+8
    st_ctx=np.zeros((B,4),np.int64); st_sc=np.zeros(B); nst=1
    hist=np.zeros((B,maxlen),np.int64); hlen=np.zeros(B,np.int64)
    for i in range(4): st_ctx[0,i]=4
    new_ctx=np.zeros((2*B,4),np.int64); new_sc=np.zeros(2*B); new_hist=np.zeros((2*B,maxlen),np.int64); new_hlen=np.zeros(2*B,np.int64)
    for t in range(n):
        c=mapping[tokens[t]]; no=opt_n[c]
        if no==0: continue
        m=0
        for s in range(nst):
            for o in range(no):
                ctx=st_ctx[s].copy(); sc=st_sc[s]
                L=hlen[s]
                for j in range(L): new_hist[m,j]=hist[s,j]
                for j in range(opt_len[c,o]):
                    ch=opt_seq[c,o,j]
                    sc+=tab[ctx[0],ctx[1],ctx[2],ctx[3],ch]
                    ctx[0]=ctx[1]; ctx[1]=ctx[2]; ctx[2]=ctx[3]; ctx[3]=ch
                    new_hist[m,L]=ch; L+=1
                new_hlen[m]=L; new_ctx[m]=ctx; new_sc[m]=sc; m+=1
        if m>B: idx=np.argsort(-new_sc[:m])[:B]
        else: idx=np.arange(m)
        nst=idx.shape[0]
        for s in range(nst):
            st_ctx[s]=new_ctx[idx[s]]; st_sc[s]=new_sc[idx[s]]; hlen[s]=new_hlen[idx[s]]
            for j in range(hlen[s]): hist[s,j]=new_hist[idx[s],j]
    bi=0
    for s in range(1,nst):
        if st_sc[s]>st_sc[bi]: bi=s
    return st_sc[bi], hist[bi,:hlen[bi]]
