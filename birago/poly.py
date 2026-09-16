# Polyphonic figure cipher: each digit stands for a set of letters; marked digit = letter doubled; wavy sign = break; letters = nulls.
# Anneal the letter->digit assignment; score = Viterbi over a trigram model (state = last two letters). 5-gram rescoring at the end.
import sys,math,json,collections,numpy as np,re,time
import ng5it,seg
LETTERS='abcdefghilmnopqrstuz'; L=len(LETTERS); LI={c:i for i,c in enumerate(LETTERS)}
def build_trigram():
    t=open('corpus_clean.txt').read(); idx=np.array([LI.get(c,-1) for c in t]); idx=idx[idx>=0]
    c3=np.zeros((L,L,L)); np.add.at(c3,(idx[:-2],idx[1:-1],idx[2:]),1)
    c2=c3.sum(2,keepdims=True); p1=np.bincount(idx,minlength=L)/len(idx)
    p3=(c3+2*p1[None,None,:])/(c2+2)
    return np.log(p3)
def load_tri():
    try: return np.load('tri_it.npy')
    except: t=build_trigram(); np.save('tri_it.npy',t); return t
TRI=load_tri()
import os
LETMODE=os.environ.get('LET','null'); MARKMODE=os.environ.get('MARK','double'); WAVY=os.environ.get('WAVY','break')
NSYM=10+(10 if MARKMODE=='sep' else 0)+(1 if WAVY=='sym' else 0)
WSYM=10+(10 if MARKMODE=='sep' else 0)
def parse(path):
    """glyph file -> symbol ids: 0-9 digits; 10-19 marked digits (MARK=sep); WSYM wavy (WAVY=sym); 100+k fixed letter k (LET=letter); None = break"""
    items=[]
    for g in open(path).read().split():
        if g=='|': items.append(None if WAVY=='break' else WSYM)
        elif g.isalpha():
            if LETMODE=='letter' and g in LI: items.append(100+LI[g])
            continue
        elif len(g)>1:
            d=int(g[0])
            if MARKMODE=='double': items+= [d,d]
            elif MARKMODE=='sep': items.append(10+d)
            else: items.append(d)
        else: items.append(int(g))
    return items
def expand(items):
    segs=[];cur=[]
    for v in items:
        if v is None:
            if cur: segs.append(cur); cur=[]
        else: cur.append(v)
    if cur: segs.append(cur)
    return segs
def viterbi(seg_digits,allowed):
    """allowed: list of 10 arrays of letter indices. Returns best log-prob and path."""
    n=len(seg_digits)
    if n==0: return 0.0,[]
    NEG=-1e9
    # state = (prev2,prev1); start with uniform-ish: use unigram-free start by allowing any first two letters at cost 0
    a0=allowed[seg_digits[0]]
    if n==1: return 0.0,[a0[0]]
    a1=allowed[seg_digits[1]]
    score=np.full((L,L),NEG); score[np.ix_(a0,a1)]=0.0
    back=[]
    for t in range(2,n):
        at=allowed[seg_digits[t]]
        # new[prev1,cur] = max_prev2 score[prev2,prev1] + TRI[prev2,prev1,cur]
        cand=score[:,:,None]+TRI[:,:,at]          # prev2,prev1,cur'
        bp=cand.argmax(0)                           # prev1,cur'
        new=np.full((L,L),NEG); new[:,at]=cand.max(0)
        back.append((at,bp)); score=new
    best=score.max(); i1,i0=np.unravel_index(score.argmax(),score.shape)
    path=[i0,i1]  # cur, prev1 reversed
    for at,bp in reversed(back):
        cur=path[-1]; prev1=path[-2] if len(path)>1 else None
    # reconstruct properly
    path=[]; p1,c=i1,i0  # score indexed [prev1,cur]
    path=[c,p1]
    for at,bp in reversed(back):
        j=np.where(at==c)[0][0]; p2=bp[p1,j]; path.append(p2); c,p1=p1,p2
    path=path[::-1]
    return float(best),path
def total(segs,assign):
    allowed=[np.array([i for i in range(L) if assign[i]==d],dtype=int) for d in range(NSYM)]
    if any(len(allowed[d])==0 for d in range(10)): return -1e9,None
    for d in range(10,NSYM):
        if len(allowed[d])==0: allowed[d]=np.arange(L)   # unassigned extra symbol: any letter
    allowed=allowed+[None]*(100-len(allowed))+[np.array([k]) for k in range(L)]
    s=0.0; paths=[]
    for sg in segs:
        b,p=viterbi(sg,allowed); s+=b; paths.append(p)
    return s,paths
def anneal(segs,iters=3000,T0=20.0,Tend=0.5,seed=0,fixed=None):
    rnd=np.random.default_rng(seed)
    assign=rnd.integers(0,NSYM,L)
    for d in range(10):
        if not (assign==d).any(): assign[rnd.integers(L)]=d
    if fixed:
        for c,d in fixed.items(): assign[LI[c]]=d
    cur,_=total(segs,assign); best=cur; bestA=assign.copy(); lam=math.log(Tend/T0)/iters
    for it in range(iters):
        T=T0*math.exp(lam*it); a2=assign.copy()
        if rnd.random()<0.7: a2[rnd.integers(L)]=rnd.integers(NSYM)
        else:
            i,j=rnd.choice(L,2,replace=False); a2[i],a2[j]=a2[j],a2[i]
        if fixed:
            for c,d in fixed.items(): a2[LI[c]]=d
        sc,_=total(segs,a2)
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            assign,cur=a2,sc
            if cur>best: best,bestA=cur,assign.copy()
    return best,bestA
def render(segs,assign):
    s,paths=total(segs,assign); return ' # '.join(''.join(LETTERS[i] for i in p) for p in paths),s
if __name__=='__main__':
    src=sys.argv[1]; iters=int(sys.argv[2]); seeds=int(sys.argv[3])
    items=parse(src); segs=expand(items); n=sum(len(s) for s in segs); print('letters',n,'segments',len(segs))
    tab=ng5it.load()
    for sd in range(seeds):
        t=time.time(); b,A=anneal(segs,iters=iters,seed=sd); txt,s=render(segs,A)
        flat=txt.replace(' # ','')
        five=ng5it.score(tab,ng5it.toidx(flat))/(len(flat)-4)
        key={d:''.join(LETTERS[i] for i in range(L) if A[i]==d) for d in range(NSYM)}
        print(f'seed {sd}: tri/letter {b/n:.3f} 5gram/letter {five:.3f} key {key} ({time.time()-t:.0f}s)'); print(txt[:300],flush=True)
