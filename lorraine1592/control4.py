"""Systematic transcription error: merged symbol pairs, not random noise.

A real by-eye transcription fails by not seeing a crossbar or a dot, which merges two
distinct cipher symbols into one everywhere they occur. That is a many-to-one relabelling
and it collapses two plaintext letters together, which is far more damaging than the random
substitution modelled in control3.py. This measures how many merged pairs the search
tolerates, so the manuscript's score can be read against a merge scale.
"""
import re, random, collections, sys
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])
from search import ils

P0=Problem(); seglens=[len(g) for g in P0.segs]; nsym=P0.ns
txt=open('src/corpus_fr.txt',encoding='utf-8',errors='replace').read().lower()
txt=re.sub(r'[^a-z]',' ',txt).translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
txt=''.join(txt.split())

def mkP(ct, ns):
    class Pc: pass
    Q=Pc(); Q.ns=ns; Q.syms=[str(i) for i in range(ns)]; Q.idx={str(i):i for i in range(ns)}
    Q.iseg=[]; k=0
    for L in seglens: Q.iseg.append(ct[k:k+L]); k+=L
    Q.segs=Q.iseg; Q.flat=[]; Q.win=[]
    for g in Q.iseg:
        st=len(Q.flat); Q.flat.extend(g)
        for i in range(len(g)-3): Q.win.append((st+i,st+i+1,st+i+2,st+i+3))
    Q.nf=len(Q.flat)
    Q.sympos=[[] for _ in range(ns)]
    for p,si in enumerate(Q.flat): Q.sympos[si].append(p)
    winof=[[] for _ in range(Q.nf)]
    for wi,w in enumerate(Q.win):
        for p in w: winof[p].append(wi)
    Q.symwin=[sorted({wi for p in Q.sympos[s] for wi in winof[p]}) for s in range(ns)]
    Q.cnt=collections.Counter(Q.flat)
    Q.full=lambda key,mu=0.0: Problem.full(Q,key,mu)
    return Q

def diverge(Q,key,NAx=None):
    ctr=[0]*NA
    for si in Q.flat: ctr[key[si]]+=1
    return sum(abs(ctr[i]/Q.nf-FREQ[i]) for i in range(NA))

def ic1(seq):
    c=collections.Counter(seq); n=len(seq)
    return sum(k*(k-1) for k in c.values())/(n*(n-1))

print('merged_pairs  distinct_syms  IC1      recovered_raw  letter_acc')
for nmerge in (0,3,6,9,12):
    accs=[]; raws=[]; ics=[]; nds=[]
    for seed in (51,52,53):
        rnd=random.Random(seed)
        p=rnd.randrange(len(txt)-5000); pt=txt[p:p+sum(seglens)]
        # a partially homophonic cipher: 22 base symbols plus 22 extra homophones used less
        order=sorted(range(NA), key=lambda i:-FREQ[i])
        base={li:[li] for li in range(NA)}
        extra=nsym-NA
        for j in range(extra): base[order[j%NA]].append(NA+j)
        ct=[]
        for ch in pt:
            li=AI[ch]; opts=base[li]
            ct.append(opts[0] if rnd.random()<0.6 or len(opts)==1 else rnd.choice(opts[1:]))
        # systematic merge: pick nmerge disjoint pairs of symbols and collapse each
        syms=list(range(nsym)); rnd.shuffle(syms)
        relab={s:s for s in range(nsym)}
        for j in range(nmerge):
            a,b=syms[2*j],syms[2*j+1]; relab[b]=a
        ct=[relab[s] for s in ct]
        used=sorted(set(ct)); ren={s:i for i,s in enumerate(used)}
        ct=[ren[s] for s in ct]
        Q=mkP(ct,len(used))
        best=-9e9; bk=None
        for mu in (0.0,2.0):
            for sd in (seed,seed+70):
                b,key=ils(Q,State,NA,iters=150,kick=4,mu=mu,seed=sd,FREQ=FREQ)
                r,_=Q.full(key)
                if diverge(Q,key)>0.25: continue
                if r>best: best=r; bk=key
        if bk is None: continue
        dec=''.join(AL[bk[si]] for si in Q.flat)
        accs.append(sum(1 for x,y in zip(dec,pt) if x==y)/len(pt))
        raws.append(best); ics.append(ic1(Q.flat)); nds.append(len(used))
    m=lambda L: sum(L)/len(L) if L else float('nan')
    print(f'{nmerge:8d}      {m(nds):8.1f}    {m(ics):.5f}   {m(raws):8.4f}     {m(accs)*100:5.1f}%')
print()
print('manuscript: 44 distinct, IC1 0.05915, best non-degenerate raw see run97b')
