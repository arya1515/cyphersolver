"""Is the recovered reading real, or does the search manufacture French from anything?

The claim to have solved fr. 3621 no. 97 rests on a decode that contains recognisable French.
But the search maximises a French 4-gram score over 44 free parameters on ~1050 characters, so
it has a standing incentive to produce French-looking strings whether or not any plaintext is
there. This runs the identical pipeline on nulls that carry no plaintext at all - the same
symbols, the same frequencies, the same segment lengths, shuffled - and measures the same
quantities. If the nulls score as well as the manuscript, the reading is an artefact.

Scoring is deliberately blind: dictionary coverage and long-word counts over a word list built
from the corpus, NOT a grep for words I expected to see.
"""
import re, random, collections, sys
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])
from search import ils

# ---- blind word list from the corpus (no names, nothing from this letter) ----
raw=open('src/corpus_fr.txt',encoding='utf-8',errors='replace').read().lower()
raw=re.sub(r'[^a-z]',' ',raw).translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
wc=collections.Counter(raw.split())
WORDS={w for w,k in wc.items() if k>=8 and 2<=len(w)<=14}
LONG={w for w in WORDS if len(w)>=6}
MAXW=14

def coverage(s):
    n=len(s); best=[0]*(n+1)
    for i in range(1,n+1):
        b=best[i-1]
        for L in range(2,min(MAXW,i)+1):
            if s[i-L:i] in WORDS:
                v=best[i-L]+L
                if v>b: b=v
        best[i]=b
    return best[n]/max(1,n)

def longwords(s):
    out=[]
    for i in range(len(s)):
        for L in range(6,min(MAXW,len(s)-i)+1):
            w=s[i:i+L]
            if w in LONG: out.append(w)
    # keep only maximal, non-overlapping-ish: count distinct long forms found
    return out

def measure(P,key):
    segs=[''.join(AL[key[i]] for i in g) for g in P.iseg]
    txt=''.join(segs)
    cov=sum(coverage(s)*len(s) for s in segs)/sum(len(s) for s in segs)
    lw=set()
    for s in segs: lw.update(longwords(s))
    raw_,_=P.full(key)
    return raw_, cov, len(lw), sorted(lw, key=lambda w:-len(w))[:12]

def solve(P, seeds=8):
    best=-9e9; bk=None
    for mu in (0.0,1.0,2.0):
        for sd in range(1,seeds+1):
            b,k=ils(P,State,NA,iters=180,kick=4,mu=mu,seed=sd,FREQ=FREQ)
            r,_=P.full(k)
            ctr=[0]*NA
            for si in P.flat: ctr[k[si]]+=1
            dv=sum(abs(ctr[i]/P.nf-FREQ[i]) for i in range(NA))
            if dv>0.26: continue
            if r>best: best=r; bk=k
    return bk

class Shuf(Problem):
    """Same symbols, same frequencies, same segment lengths - order destroyed."""
    def __init__(self, base, seed):
        rnd=random.Random(seed)
        flat=list(base.flat); rnd.shuffle(flat)
        self.ns=base.ns; self.syms=base.syms; self.idx=base.idx
        self.iseg=[]; k=0
        for g in base.iseg:
            self.iseg.append(flat[k:k+len(g)]); k+=len(g)
        self.segs=self.iseg
        self.flat=[]; self.win=[]
        for g in self.iseg:
            st=len(self.flat); self.flat.extend(g)
            for i in range(len(g)-3): self.win.append((st+i,st+i+1,st+i+2,st+i+3))
        self.nf=len(self.flat)
        self.sympos=[[] for _ in range(self.ns)]
        for p,si in enumerate(self.flat): self.sympos[si].append(p)
        winof=[[] for _ in range(self.nf)]
        for wi,w in enumerate(self.win):
            for p in w: winof[p].append(wi)
        self.symwin=[sorted({wi for p in self.sympos[s] for wi in winof[p]}) for s in range(self.ns)]
        self.cnt=collections.Counter(self.flat)

P=Problem()
k=solve(P)
r,cov,nlw,ex = measure(P,k)
print('MANUSCRIPT   raw %.4f   word-coverage %.1f%%   distinct long words %d' % (r,cov*100,nlw))
print('   longest found:', ', '.join(ex))
print()
print('NULLS  (same symbols and frequencies, order shuffled - no plaintext present)')
rs=[];cs=[];ls=[]
for sd in (101,102,103,104,105):
    Q=Shuf(P,sd)
    kq=solve(Q,seeds=8)
    rq,cq,lq,exq = measure(Q,kq)
    rs.append(rq); cs.append(cq); ls.append(lq)
    print('  null %d  raw %.4f   coverage %.1f%%   long words %2d   e.g. %s' % (sd,rq,cq*100,lq,', '.join(exq[:6])))
m=lambda L: sum(L)/len(L)
print()
print('  null mean: raw %.4f  coverage %.1f%%  long words %.1f' % (m(rs),m(cs)*100,m(ls)))
print('  manuscript: raw %.4f  coverage %.1f%%  long words %d' % (r,cov*100,nlw))
