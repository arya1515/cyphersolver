"""How much transcription noise does the search tolerate?

The control with a clean ciphertext recovers known keys at ~99%. The manuscript run stalls
at -2.46. This injects a controlled rate of transcription error - a symbol read as the wrong
symbol, as happens when a crossbar or a dot is missed - and measures the recovered accuracy
and score, so the manuscript's score can be read against a noise scale.
"""
import re, random, sys, collections
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])
from search import ils

P0=Problem(); seglens=[len(g) for g in P0.segs]; nsym=P0.ns
txt=open('src/corpus_fr.txt',encoding='utf-8',errors='replace').read().lower()
txt=re.sub(r'[^a-z]',' ',txt).translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
txt=''.join(txt.split())

def mkP(ct):
    class Pc: pass
    Q=Pc(); Q.ns=nsym; Q.syms=[str(i) for i in range(nsym)]; Q.idx={str(i):i for i in range(nsym)}
    Q.iseg=[]; k=0
    for L in seglens: Q.iseg.append(ct[k:k+L]); k+=L
    Q.segs=Q.iseg; Q.flat=[]; Q.win=[]
    for g in Q.iseg:
        st=len(Q.flat); Q.flat.extend(g)
        for i in range(len(g)-3): Q.win.append((st+i,st+i+1,st+i+2,st+i+3))
    Q.nf=len(Q.flat)
    Q.sympos=[[] for _ in range(nsym)]
    for p,si in enumerate(Q.flat): Q.sympos[si].append(p)
    winof=[[] for _ in range(Q.nf)]
    for wi,w in enumerate(Q.win):
        for p in w: winof[p].append(wi)
    Q.symwin=[sorted({wi for p in Q.sympos[s] for wi in winof[p]}) for s in range(nsym)]
    Q.cnt=collections.Counter(Q.flat)
    Q.full=lambda key,mu=0.0: Problem.full(Q,key,mu)
    return Q

def make(seed, mono=True, noise=0.0):
    rnd=random.Random(seed)
    p=rnd.randrange(len(txt)-5000)
    pt=txt[p:p+sum(seglens)]
    if mono:
        # monoalphabetic: one cipher symbol per letter, the spare symbols are nulls that
        # the transcriber would have recorded but which stand for nothing
        perm=list(range(nsym)); rnd.shuffle(perm)
        m={AL[i]:perm[i] for i in range(NA)}
        ct=[m[ch] for ch in pt]
        slots=[0]*nsym
        for i in range(NA): slots[perm[i]]=i
        for i in range(NA,nsym): slots[perm[i]]=rnd.randrange(NA)
    else:
        order=sorted(range(NA), key=lambda i:-FREQ[i])
        sl=[order[i%NA] for i in range(nsym)]; rnd.shuffle(sl)
        homo=collections.defaultdict(list)
        for si,li in enumerate(sl): homo[li].append(si)
        for li in range(NA):
            if not homo[li]: homo[li]=[rnd.randrange(nsym)]
        ct=[rnd.choice(homo[AI[ch]]) for ch in pt]; slots=sl
    if noise:
        ct=[(rnd.randrange(nsym) if rnd.random()<noise else s) for s in ct]
    return pt, ct, slots

print('mode        noise   recovered_raw   TRUE_raw   letter_acc')
for mono in (True,False):
    for noise in (0.0,0.03,0.06,0.10,0.15):
        accs=[]; raws=[]; tr=[]
        for seed in (31,32,33):
            pt,ct,slots=make(seed,mono,noise); Q=mkP(ct)
            best=-9e9; bk=None
            for sd in (seed, seed+100):
                for mu in (0.0,2.0):
                    b,key=ils(Q,State,NA,iters=120,kick=4,mu=mu,seed=sd,FREQ=FREQ)
                    r,_=Q.full(key)
                    if r>best: best=r; bk=key
            dec=''.join(AL[bk[si]] for si in Q.flat)
            accs.append(sum(1 for x,y in zip(dec,pt) if x==y)/len(pt))
            raws.append(best); t,_=Q.full(slots); tr.append(t)
        m=lambda L: sum(L)/len(L)
        print(f'{"mono" if mono else "homo":10s}  {noise*100:4.0f}%   {m(raws):8.4f}     {m(tr):8.4f}    {m(accs)*100:5.1f}%')
