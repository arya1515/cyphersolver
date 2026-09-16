import numpy as np,random,math,sys
toks=open('ct.txt').read().split()
mode=sys.argv[2] if len(sys.argv)>2 else 'nums'
seq=[]
for t in toks:
    if t.isdigit(): seq.append(t)
    elif mode=='withletters' and t in ('a','m'): seq.append(t)
segs=[];cur=[]
for t in seq:
    if t.isdigit() and len(t)==3:
        if cur: segs.append(cur); cur=[]
    else: cur.append(t)
if cur: segs.append(cur)
syms=sorted(set(t for s in segs for t in s)); pos={s:i for i,s in enumerate(syms)}
core=[i for i,s in enumerate(syms) if s.isdigit() and 12<=int(s)<=33]
lp=np.load('../lucca/it5.npy')
letters=[ord(ch)-97 for ch in 'abcdefghilmnopqrstuz']
segi=[np.array([pos[x] for x in s]) for s in segs if len(s)>=5]
ngr=sum(len(s)-4 for s in segi)
def score(key):
    tot=0.0
    for ci in segi:
        p=key[ci]; q=p[:-4]*456976+p[1:-3]*17576+p[2:-2]*676+p[3:-1]*26+p[4:]
        tot+=float(lp[q].sum())
    return tot
def anneal(seed,iters=80000,T0=6.0):
    rnd=random.Random(seed)
    key=np.array([rnd.choice(letters) for _ in syms])
    perm=letters[:]; rnd.shuffle(perm)
    for k,i in enumerate(core): key[i]=perm[k%len(perm)]
    cur=score(key); best=(cur,key.copy())
    for it in range(iters):
        T=max(0.02,T0*(1-it/iters))
        s=rnd.randrange(len(syms)); old=key[s]
        if s in core or rnd.random()<0.3:
            t=rnd.randrange(len(syms)); key[s],key[t]=key[t],key[s]
            new=score(key)
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: key[s],key[t]=key[t],key[s]
        else:
            key[s]=rnd.choice(letters); new=score(key)
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: key[s]=old
        if cur>best[0]: best=(cur,key.copy())
    return best
n=int(sys.argv[1]); print(mode,'symbols',len(syms),'5-grams',ngr)
res=[]
for seed in range(n):
    b=anneal(seed); res.append(b)
    print(seed,round(b[0]/ngr,3),' | '.join(''.join(chr(97+b[1][x]) for x in ci) for ci in segi),flush=True)
b=max(res); print('KEY',{s:chr(97+b[1][i]) for i,s in enumerate(syms)})
