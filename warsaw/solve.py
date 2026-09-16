import numpy as np,random,math,collections,sys
toks=open('ct.txt').read().split()
nums=[t for t in toks if t.isdigit()]
# segments: split at 3-digit code groups; keep all two-digit symbols
segs=[];cur=[]
for t in nums:
    if len(t)==3:
        if cur: segs.append(cur); cur=[]
    else: cur.append(t)
if cur: segs.append(cur)
syms=sorted(set(t for s in segs for t in s)); pos={s:i for i,s in enumerate(syms)}
lp=np.load('../lucca/it5.npy')
letters=[ord(ch)-97 for ch in 'abcdefghilmnopqrstuz']
segi=[np.array([pos[x] for x in s]) for s in segs if len(s)>=5]
def score(key):
    tot=0.0
    for ci in segi:
        p=key[ci]
        q=p[:-4]*456976+p[1:-3]*17576+p[2:-2]*676+p[3:-1]*26+p[4:]
        tot+=float(lp[q].sum())
    return tot
def anneal(seed,iters=60000,T0=6.0,shuffle=False):
    rnd=random.Random(seed)
    global segi
    if shuffle:
        allt=[x for s in segi for x in s]; rnd.shuffle(allt); k=0; ns=[]
        for s in segi: ns.append(np.array(allt[k:k+len(s)])); k+=len(s)
        segi=ns
    key=np.array([rnd.choice(letters) for _ in syms])
    cur=score(key); best=(cur,key.copy())
    for it in range(iters):
        T=max(0.02,T0*(1-it/iters))
        s=rnd.randrange(len(syms)); old=key[s]
        if rnd.random()<0.3:
            t=rnd.randrange(len(syms)); key[s],key[t]=key[t],key[s]
            new=score(key)
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: key[s],key[t]=key[t],key[s]
        else:
            key[s]=rnd.choice(letters)
            new=score(key)
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: key[s]=old
        if cur>best[0]: best=(cur,key.copy())
    return best
if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 6
    shuffle=len(sys.argv)>2 and sys.argv[2]=='shuffle'
    ngr=sum(len(s)-4 for s in segi); print('symbols',len(syms),'5-grams',ngr)
    res=[]
    for seed in range(n):
        b=anneal(seed,shuffle=shuffle); res.append(b)
        txt=' | '.join(''.join(chr(97+b[1][x]) for x in ci) for ci in segi)
        print(seed,round(b[0]/ngr,3),txt,flush=True)
    b=max(res)
    print('KEY',{s:chr(97+b[1][i]) for i,s in enumerate(syms)})
