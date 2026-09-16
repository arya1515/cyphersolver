import numpy as np,random,math,collections,sys
ct=[int(x) for x in open('ct.txt').read().split()]
lp=np.load('it5.npy')
syms=sorted(set(ct)); pos={s:i for i,s in enumerate(syms)}
ci=np.array([pos[x] for x in ct])
letters=[ord(ch)-97 for ch in 'abcdefghilmnopqrstuz']
def score(key):
    p=key[ci]
    q=p[:-4]*456976+p[1:-3]*17576+p[2:-2]*676+p[3:-1]*26+p[4:]
    return float(lp[q].sum())
def anneal(seed,iters=100000,T0=8.0):
    rnd=random.Random(seed)
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
    n=int(sys.argv[1]) if len(sys.argv)>1 else 10
    res=[]
    for seed in range(n):
        b=anneal(seed); res.append(b)
        print(seed,round(b[0],1),''.join(chr(97+b[1][x]) for x in ci),flush=True)
    b=max(res)
    print('KEY',{s:chr(97+b[1][i]) for i,s in enumerate(syms)})
