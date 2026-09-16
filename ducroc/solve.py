import numpy as np,random,math,sys,collections
import os
V=27; lp=np.load(os.environ.get('LM','frn5.npy'))
DOTS=os.environ.get('DOTS','ignore')
LET=[ord(c)-97 for c in 'abcdefghilmnopqrstuxz']  # v->u, j->i, y kept? (y common in 16c: 'roy','moy') 
LET=[ord(c)-97 for c in 'abcdefghilmnopqrstuxyz']
def load(fn):
    toks=open(fn).read().split()
    if DOTS=='ignore': toks=[t for t in toks if t!='.']
    return toks
def prep(toks):
    syms=sorted(set(t for t in toks if t!='.')); pos={s:i for i,s in enumerate(syms)}
    seq=[(-1 if t=='.' else pos[t]) for t in toks]
    return syms,np.array(seq)
def score(key,seq):
    p=np.where(seq<0,26,key[np.maximum(seq,0)])
    p=np.concatenate([[26,26,26,26],p,[26]])
    q=((((p[:-4]*V+p[1:-3])*V+p[2:-2])*V+p[3:-1])*V+p[4:])
    return float(lp[q].sum())
def anneal(syms,seq,seed,iters=80000,T0=5.0,fixed=None):
    rnd=random.Random(seed)
    key=np.array([rnd.choice(LET) for _ in syms])
    if rnd.random()<0.5:
        cnt=collections.Counter(seq[seq>=0].tolist()); order=[s for s,_ in cnt.most_common()]
        fr='eaisntrulodcmpuqvgbfhxyz'
        for r,sidx in enumerate(order): key[sidx]=ord(fr[min(r,len(fr)-1)])-97
    if fixed:
        for s,l in fixed.items():
            if s in syms: key[syms.index(s)]=ord(l)-97
    cur=score(key,seq); best=(cur,key.copy())
    free=[i for i in range(len(syms)) if not (fixed and syms[i] in fixed)]
    for it in range(iters):
        T=max(0.05,T0*(1-it/iters))
        s=rnd.choice(free); old=key[s]
        if rnd.random()<0.25:
            t=rnd.choice(free); key[s],key[t]=key[t],key[s]
            new=score(key,seq)
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: key[s],key[t]=key[t],key[s]
        else:
            key[s]=rnd.choice(LET); new=score(key,seq)
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: key[s]=old
        if cur>best[0]: best=(cur,key.copy())
    return best
def render(key,seq):
    return ''.join(' ' if x<0 else chr(97+key[x]) for x in seq)
if __name__=='__main__':
    toks=load(sys.argv[1]); n=int(sys.argv[2]) if len(sys.argv)>2 else 8
    syms,seq=prep(toks)
    res=[]
    for seed in range(n):
        b=anneal(syms,seq,seed); res.append(b)
        print(seed,round(b[0],1),render(b[1],seq),flush=True)
    b=max(res,key=lambda r:r[0])
    print('KEY',{s:chr(97+b[1][i]) for i,s in enumerate(syms)})
