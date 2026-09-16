# Control for the crib-fixed reading: the same procedure on shuffled ciphertexts (same figures, same counts, same 8 fixed letters).
import numpy as np,solve,random,math
solve.lp=np.load('it5.npy')
ct=[int(x) for x in open('ct.txt').read().split()]
letters=solve.letters
FIXED={3:'a',11:'l',8:'d',17:'i',26:'p',21:'r',1:'e',19:'t'}
def run(ct,fixed,seeds=2,iters=100000,T0=6.0):
    syms=sorted(set(ct)); pos={s:i for i,s in enumerate(syms)}; ci=np.array([pos[x] for x in ct])
    solve.ci=ci; solve.syms=syms; best=None
    for seed in range(seeds):
        rnd=random.Random(seed); key=np.array([rnd.choice(letters) for _ in syms])
        for s,l in fixed.items(): key[syms.index(s)]=ord(l)-97
        free=[i for i in range(len(syms)) if syms[i] not in fixed]
        cur=solve.score(key); b=(cur,key.copy())
        for it in range(iters):
            T=max(0.05,T0*(1-it/iters)); s=rnd.choice(free); old=key[s]
            key[s]=rnd.choice(letters); new=solve.score(key)
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: key[s]=old
            if cur>b[0]: b=(cur,key.copy())
        if best is None or b[0]>best[0]: best=b
    return best[0]/(len(ct)-4), ''.join(chr(97+best[1][x]) for x in ci)
if __name__=='__main__':
    r=run(ct,FIXED,seeds=3); print('REAL',round(r[0],3),r[1][:80])
    rnd=random.Random(11)
    for k in range(5):
        sh=ct[:]; rnd.shuffle(sh); r=run(sh,FIXED); print('SHUF',k,round(r[0],3),r[1][:80],flush=True)
# Result 2026-09-16: REAL -2.496; SHUF -3.395 -3.493 -3.599 -3.682 -3.453
