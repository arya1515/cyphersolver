"""Control: can the solver recover a KNOWN key at this data size and segmentation?

Encipher a genuine passage of Montaigne with a random homophonic key having the same
number of symbols and the same per-symbol frequency profile as the fr. 3621 transcription,
cut it into segments of the same lengths, and run the same annealer. If the control fails,
the method is too weak for 1054 characters and no conclusion can be drawn about the
manuscript; if the control succeeds, the failure on the manuscript is in the transcription
or in the assumption of letter substitution.
"""
import re, random, sys, collections
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])

P0=Problem()
seglens=[len(g) for g in P0.segs]
nsym=P0.ns

txt=open('src/corpus_fr.txt',encoding='utf-8',errors='replace').read().lower()
txt=re.sub(r'[^a-z]',' ',txt).translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
txt=''.join(txt.split())

def make(seed):
    rnd=random.Random(seed)
    p=rnd.randrange(len(txt)-5000)
    pt=txt[p:p+sum(seglens)]
    # homophonic key: assign nsym cipher symbols to letters in proportion to letter frequency
    letters=[]
    for i,c in enumerate(AL):
        letters.append(c)
    # give extra symbols to the most frequent letters, as a period cipher would
    order=sorted(range(NA), key=lambda i:-FREQ[i])
    slots=[order[i%NA] for i in range(nsym)]
    rnd.shuffle(slots)
    homo=collections.defaultdict(list)
    for si,li in enumerate(slots): homo[li].append(si)
    for li in range(NA):
        if not homo[li]: homo[li]=[rnd.randrange(nsym)]
    ct=[]
    for ch in pt:
        li=AI[ch]; ct.append(rnd.choice(homo[li]))
    return pt, ct, slots

def run(seed, restarts, iters, mu):
    pt, ct, slots = make(seed)
    class Pc: pass
    Q=Pc()
    Q.ns=nsym; Q.syms=[str(i) for i in range(nsym)]; Q.idx={str(i):i for i in range(nsym)}
    Q.iseg=[]; k=0
    for L in seglens:
        Q.iseg.append(ct[k:k+L]); k+=L
    Q.segs=Q.iseg
    Q.flat=[]; Q.win=[]
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
    b,key=anneal(Q,restarts,iters,mu,seed)
    raw,_=Q.full(key)
    # recovered plaintext
    dec=''.join(AL[key[si]] for si in Q.flat)
    truth=''.join(pt)
    acc=sum(1 for x,y in zip(dec,truth) if x==y)/len(truth)
    # what does the TRUE key score?
    tk=[slots[i] for i in range(nsym)]
    traw,_=Q.full(tk)
    return raw, traw, acc, truth[:120], dec[:120]

for seed in (21,22,23):
    raw,traw,acc,t,d = run(seed, 25, 150000, 4.0)
    print(f'seed {seed}:  recovered raw {raw:.4f}   TRUE-key raw {traw:.4f}   letter accuracy {acc*100:.1f}%')
    print(f'   truth: {t}')
    print(f'   found: {d}')
    print()
