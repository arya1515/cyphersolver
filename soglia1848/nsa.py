import numpy as np, re, sys, math, collections
from numba import njit
A=27
LP=np.load(sys.argv[1] if len(sys.argv)>1 and sys.argv[1].endswith('.npy') else 'lm5sp.npy')

def load_units(fn='ct2.txt'):
    s=open(fn).read().strip()
    out=[]
    for r in re.split('5',s):
        if len(r)%2==0: out+=[r[i:i+2] for i in range(0,len(r),2)]
        else: out+=[r[i:i+2] for i in range(0,len(r)-1,2)]+['L'+r[-1]]
        out.append('_')
    o=[]
    for u in out:
        if u=='_' and (not o or o[-1]=='_'): continue
        o.append(u)
    return o

@njit(cache=True)
def score(seq,m,LP):
    tot=0.0
    h0=0;h1=0;h2=0;h3=0
    for k in seq:
        c=0 if k<0 else m[k]
        if c<0: continue   # null
        tot+=LP[(((h0*27+h1)*27+h2)*27+h3)*27+c]
        h0=h1;h1=h2;h2=h3;h3=c
    tot+=LP[(((h0*27+h1)*27+h2)*27+h3)*27+0]
    return tot

@njit(cache=True)
def anneal(seq,m,LP,fixed,iters,T0,T1,seed,allowed):
    np.random.seed(seed)
    n=len(m)
    cur=score(seq,m,LP)
    best=cur;bm=m.copy()
    na=len(allowed)
    for i in range(iters):
        T=T0*(T1/T0)**(i/iters)
        k=np.random.randint(n)
        if fixed[k]: continue
        old=m[k]
        if np.random.random()<0.8:
            m[k]=allowed[np.random.randint(na)]
            k2=-1
        else:
            k2=np.random.randint(n)
            if fixed[k2]: continue
            old2=m[k2]; m[k]=old2; m[k2]=old
        new=score(seq,m,LP)
        if new>=cur or np.random.random()<math.exp((new-cur)/T):
            cur=new
            if cur>best: best=cur;bm[:]=m
        else:
            m[k]=old
            if k2>=0: m[k2]=old2
    return best,bm

def show(seq,m,types):
    return ''.join(' ' if k<0 else ('' if m[k]<0 else chr(96+m[k])) for k in seq)
