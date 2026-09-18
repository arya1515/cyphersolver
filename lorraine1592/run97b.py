"""Best-effort solve of fr. 3621 no. 97, with a non-degenerate selection rule.

Two failures had to be fixed. (1) Selecting the key with the best unpenalised 4-gram score
picks a degenerate key that maps a dozen symbols onto e and reads "etenete...": such keys
are rejected here by requiring the induced letter frequency to lie within L1 distance 0.25
of French. (2) Forcing the ~20 symbols that occur six times or fewer to be letters corrupts
every 4-gram they touch; --rare lets them instead break the letter stream, which is what
they would do if they are nulls or word-signs.
"""
import re, sys, collections, argparse
_ARGV=list(sys.argv)
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])
from search import ils

A=_ARGV
def flag(n,d=None):
    if n in A: return A[A.index(n)+1]
    return d
MERGE='--merge' in A
RARE=int(flag('--rare','0'))
ITERS=int(flag('--iters','250'))
NSEED=int(flag('--seeds','16'))

def read_ct2(path, merge, rare):
    """Like read_ct but symbols occurring <= rare times become stream breaks."""
    raw=[]
    for ln in open(path):
        if ln.startswith('#') or not ln.strip(): continue
        ln2=re.sub(r'\[\[.*?\]\]',' | ',ln)
        parts=ln2.split(None,1)
        if len(parts)<2: continue
        for t in parts[1].split():
            t=t.rstrip('?')
            raw.append('|' if (t.startswith('<') or t in ('|','.',':','/','-','#','..'))
                       else (MERGE_TBL.get(t,t) if merge else t))
    c=collections.Counter(x for x in raw if x!='|')
    drop={s for s,k in c.items() if k<=rare} if rare else set()
    segs=[]; cur=[]
    for t in raw:
        if t=='|' or t in drop:
            if len(cur)>=4: segs.append(cur)
            cur=[]
        else: cur.append(t)
    if len(cur)>=4: segs.append(cur)
    return segs, drop
MERGE_TBL={'L':'l','T':'t','G':'g','C':'c','K':'c','N':'n','J':'n','S':'s','O':'o','M':'m'}

class P2(Problem):
    def __init__(self, path='ct/no97_eye.txt', merge=False, rare=0):
        self.segs, self.dropped = read_ct2(path, merge, rare)
        self.syms=sorted({s for g in self.segs for s in g}); self.ns=len(self.syms)
        self.idx={s:i for i,s in enumerate(self.syms)}
        self.iseg=[[self.idx[s] for s in g] for g in self.segs]
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

def diverge(P,key):
    ctr=[0]*NA
    for si in P.flat: ctr[key[si]]+=1
    return sum(abs(ctr[i]/P.nf-FREQ[i]) for i in range(NA))

P=P2(merge=MERGE, rare=RARE)
print(f'merge={MERGE} rare<={RARE} dropped={len(P.dropped)} segments={len(P.segs)} chars={P.nf} symbols={P.ns}', flush=True)
best=-9e9; bestk=None; tag=None
for mu in (0.0,1.0,2.0,3.0):
    for sd in range(1,NSEED+1):
        b,k=ils(P,State,NA,iters=ITERS,kick=4,mu=mu,seed=sd,FREQ=FREQ)
        raw,_=P.full(k); dv=diverge(P,k)
        if dv>0.25: continue                     # reject degenerate keys
        if raw>best:
            best=raw; bestk=list(k); tag=(mu,sd,dv)
            print(f'  mu={mu} seed={sd}  raw {raw:.4f}  divergence {dv:.3f}', flush=True)
if bestk is None:
    print('every key was degenerate'); sys.exit(0)
print(f'\nBEST non-degenerate raw {best:.4f}   divergence {tag[2]:.3f}')
print('  reference: real French -1.93; control true keys -1.63; control recovered 99% keys -1.62\n')
print('KEY')
for s in P.syms: print(f'  {s} -> {AL[bestk[P.idx[s]]]}')
if P.dropped: print('  broken out as nulls/word-signs: '+' '.join(sorted(P.dropped)))
print()
km={s:AL[bestk[P.idx[s]]] for s in P.syms}
for ln in open('ct/no97_eye.txt'):
    if ln.startswith('#') or not ln.strip(): continue
    parts=ln.split(None,1)
    if len(parts)<2: continue
    res=[]
    for t in re.findall(r'\[\[.*?\]\]|\S+', parts[1]):
        if t.startswith('[[') or t.startswith('<'): res.append(' '+t+' ')
        elif t in ('.',':','/','-','#','..'): res.append(t)
        else:
            s=t.rstrip('?'); s=MERGE_TBL.get(s,s) if MERGE else s
            res.append(km.get(s,'·'))
    print(parts[0]+' '+''.join(res))
