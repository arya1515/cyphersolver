# Variable-length figure cipher: scan segmentation rules x homophonic annealing (Italian 5-gram).
import re,sys,math,itertools,collections,json,time
import numpy as np, ng5it
AL='abcdefghijklmnopqrstuvwxyz'
LET=np.array([AL.index(c) for c in 'abcdefghilmnopqrstuz'])
import os
tab=np.load(os.environ.get('NG5','ng5it.npy'))
P1=np.load(os.environ.get('P1','p1it.npy')); LAMBDA=0.3
MU=float(os.environ.get('MU','0'))
CAP=np.full(26,3.0); CAP[[AL.index(c) for c in 'aeiou']]=8.0
def units(s):
    s=re.sub(r'\s+','',s)
    return re.findall(r'[%:+\-]\d\d|[a-z]|\d+',s)
def parse(u,S,U=set(),three1=False,letters='null'):
    toks=[]
    for x in u:
        if x[0] in '%:+-': toks.append('#'+x)
        elif x.isalpha():
            if letters=='null': continue
            elif letters=='sym': toks.append('L'+x)
            else: toks.append('#'+x)
        else:
            i=0
            while i<len(x):
                if three1 and x[i]=='1' and i+2<len(x): toks.append(x[i:i+3]); i+=3
                elif x[i] in S and i+1<len(x): toks.append(x[i:i+2]); i+=2
                elif i+1<len(x) and x[i+1] in U: toks.append(x[i:i+2]); i+=2
                else: toks.append(x[i]); i+=1
    return toks
def dangling(u,S):
    d=0
    for x in u:
        if x.isdigit():
            p=parse([x],S)
            if x[-1] in S and len(p[-1])==1: d+=1
    return d
def prep(toks):
    global FREEPOS
    syms=sorted(set(toks)); si={s:i for i,s in enumerate(syms)}
    idx=np.array([si[t] for t in toks]); isb=np.array([t[0]=='#' for t in toks])
    FREEPOS=np.where(~isb)[0]
    global FREESYM; FREESYM=np.array([i for i,s_ in enumerate(syms) if s_[0]!='#'])
    n=len(toks); W=np.array([i for i in range(n-4) if not isb[i:i+5].any()])
    free=[i for i,s in enumerate(syms) if s[0]!='#']
    return syms,idx,W,free
def score(key,idx,W,lam=None):
    p=key[idx]; q=p[W]*456976+p[W+1]*17576+p[W+2]*676+p[W+3]*26+p[W+4]
    s=float(tab[q].sum())
    lam=LAMBDA if lam is None else lam
    if lam:
        pf=p[FREEPOS]; n=len(pf); cnt=np.bincount(pf,minlength=26)
        exp=P1*n; s-=lam*float(((cnt-exp)**2/(exp+1)).sum())
    if MU:
        sc=np.bincount(key[FREESYM],minlength=26); s-=MU*float(np.clip(sc-CAP,0,None).sum())
    return s
def anneal(idx,nsym,W,free,iters=40000,T0=6.0,Tend=0.2,seed=0,fixed=None):
    rnd=np.random.default_rng(seed); key=LET[rnd.integers(0,len(LET),nsym)]
    if fixed:
        for k,v in fixed.items(): key[k]=v
        free=[f for f in free if f not in fixed]
    free=np.array(free)
    cur=score(key,idx,W); best=cur; bestkey=key.copy(); lam=math.log(Tend/T0)/iters
    for it in range(iters):
        T=T0*math.exp(lam*it); k2=key.copy(); r=rnd.random()
        if r<0.1:
            # Gibbs move: resample one symbol's letter from the Boltzmann distribution over all letters
            s_=free[rnd.integers(len(free))]; scs=np.empty(len(LET))
            for j,L in enumerate(LET):
                k2[s_]=L; scs[j]=score(k2,idx,W)
            pr=np.exp((scs-scs.max())/T); pr/=pr.sum(); j=rnd.choice(len(LET),p=pr)
            k2[s_]=LET[j]; key,cur=k2,scs[j]
            if cur>best: best,bestkey=cur,key.copy()
            continue
        if r<0.75: k2[free[rnd.integers(len(free))]]=LET[rnd.integers(len(LET))]
        elif r<0.93:
            a,b=rnd.choice(free,2,replace=False); k2[a],k2[b]=k2[b],k2[a]
        else:
            # letter-level swap: exchange the whole symbol sets of two letters
            x,y=LET[rnd.choice(len(LET),2,replace=False)]; fx=k2[free]==x; fy=k2[free]==y
            k2[free[fx]]=y; k2[free[fy]]=x
        sc=score(k2,idx,W)
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            key,cur=k2,sc
            if cur>best: best,bestkey=cur,key.copy()
    return best,bestkey
def solve(toks,restarts=2,iters=40000):
    syms,idx,W,free=prep(toks)
    if len(W)<50: return None
    best=max((anneal(idx,len(syms),W,free,iters=iters,seed=r) for r in range(restarts)),key=lambda t:t[0])
    key=best[1]
    dec=''.join('#' if syms[i][0]=='#' else AL[key[i]] for i in idx)
    return best[0]/len(W),dec,{syms[i]:AL[key[i]] for i in free},len(syms),len(W)
def scan(u,restarts=2,iters=40000,three1=False,Uopts=(set(),{'0'}),maxdangle=3,letters='null',log=None):
    res=[]
    for k in range(0,11):
        for S in itertools.combinations('0123456789',k):
            S=set(S)
            if dangling(u,S)>maxdangle: continue
            for U in Uopts:
                toks=parse(u,S,U,three1,letters)
                nd=len(set(t for t in toks if t[0]!='#'))
                if not 12<=nd<=90: continue
                r=solve(toks,restarts,iters)
                if r is None: continue
                res.append((r[0],''.join(sorted(S)),''.join(sorted(U)),nd,r[4],r[1]))
                if log: print(f'{r[0]:.3f} S={"".join(sorted(S)) or "-"} U={"".join(sorted(U)) or "-"} nsym={nd} win={r[4]} {r[1][:70]}',flush=True,file=log)
    res.sort(reverse=True)
    return res
if __name__=='__main__':
    src=sys.argv[1]; u=units(open(src).read()); letters=sys.argv[2] if len(sys.argv)>2 else 'null'
    t0=time.time()
    res=scan(u,log=sys.stdout,letters=letters)
    print('TOP'); 
    for r in res[:15]: print(r)
    print('time',time.time()-t0)
