# Crib-fixed annealing for R2159: fix the eight letters Tomokiyo's crib gives without contradiction, anneal the rest.
import numpy as np,solve,random,math,sys
solve.lp=np.load('it5.npy')
ct=[int(x) for x in open('ct.txt').read().split()]
syms=solve.syms; ci=solve.ci; letters=solve.letters
FIXED={3:'a',11:'l',8:'d',17:'i',26:'p',21:'r',1:'e',19:'t'}
def anneal(seed,iters=100000,T0=6.0,fixed=FIXED):
    rnd=random.Random(seed)
    key=np.array([rnd.choice(letters) for _ in syms])
    for s,l in fixed.items(): key[syms.index(s)]=ord(l)-97
    free=[i for i in range(len(syms)) if syms[i] not in fixed]
    cur=solve.score(key); best=(cur,key.copy())
    for it in range(iters):
        T=max(0.05,T0*(1-it/iters)); s=rnd.choice(free); old=key[s]
        key[s]=rnd.choice(letters); new=solve.score(key)
        if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
        else: key[s]=old
        if cur>best[0]: best=(cur,key.copy())
    return best
if __name__=='__main__':
    for seed in range(int(sys.argv[1]) if len(sys.argv)>1 else 6):
        b=anneal(seed); print(seed,round(b[0],1),round(b[0]/(len(ct)-4),3),''.join(chr(97+b[1][x]) for x in ci),flush=True)
