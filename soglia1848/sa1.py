import numpy as np, re, random, math, sys, collections
from lmscore import LM
s=open('ct.txt').read()
def units(s):
    out=[]
    for r in re.split('5',s):
        if len(r)%2==0: out+= [r[i:i+2] for i in range(0,len(r),2)]
        else: out+= [r[i:i+2] for i in range(0,len(r)-1,2)]+['L'+r[-1]]
        out.append('_')
    # collapse spaces
    o=[]
    for u in out:
        if u=='_' and (not o or o[-1]=='_'): continue
        o.append(u)
    return o
U=units(s)
types=sorted(set(u for u in U if u!='_'))
ti={t:i for i,t in enumerate(types)}
seq=np.array([ -1 if u=='_' else ti[u] for u in U])
mode=sys.argv[1] if len(sys.argv)>1 else 'sp'
L=LM('lm5sp.npy' if mode=='sp' else 'lm5ns.npy')
def text(m):
    if mode=='sp':
        return np.array([0 if k<0 else m[k] for k in seq])
    return np.array([m[k] for k in seq if k>=0])
def sc(m): return L.score(text(m))
def show(m):
    return ''.join(' ' if k<0 else chr(96+m[k]) for k in seq)
seed=int(sys.argv[2]) if len(sys.argv)>2 else 0
random.seed(seed); np.random.seed(seed)
freq=collections.Counter(u for u in U if u!='_')
it_let='eaioenltrscdupmvgfbhzq'
best=None
for restart in range(int(sys.argv[3]) if len(sys.argv)>3 else 4):
    m=np.array([random.randint(1,26) for _ in types])
    cur=sc(m); T=20.0
    iters=int(sys.argv[4]) if len(sys.argv)>4 else 60000
    for i in range(iters):
        T=8.0*(0.05/8.0)**(i/iters)
        k=random.randrange(len(types)); old=m[k]; k2=None
        if random.random()<0.7:
            m[k]=random.randint(1,26)
        else:
            k2=random.randrange(len(types)); old2=m[k2]; m[k],m[k2]=m[k2],m[k]
        new=sc(m)
        if new>=cur or random.random()<math.exp((new-cur)/T): cur=new
        else:
            m[k]=old
            if k2 is not None: m[k2]=old2
    print(restart,cur,show(m)[:300],flush=True)
    if best is None or cur>best[0]: best=(cur,m.copy())
print('BEST',best[0]); print(show(best[1]))
print({t:chr(96+best[1][i]) for i,t in enumerate(types)})
