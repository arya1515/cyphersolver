"""Second-stage solver for BnF fr. 3621 no. 97.

Adds to solve97.py: (a) an optional merge of the diacritic variants onto their base
letterform, to test whether the 44-symbol alphabet is an artefact of over-splitting pen
marks; (b) nulls - a symbol may be assigned "delete" rather than a plaintext letter, which
is how 16th-century French ciphers of this type dispose of their padding symbols; (c) a
full (non-incremental) scorer used to polish the incremental annealer's key.
"""
import re, json, math, random, collections, sys

M=json.load(open('src/fr_lm.json'))
AL=M['al']; N1=M['n1']; N2=M['n2']; N3=M['n3']; N4=M['n4']
TOT=sum(N1.values()); LAM=0.4
AI={c:i for i,c in enumerate(AL)}; NA=len(AL); NULL=NA

def _p(g):
    if len(g)==4:
        c=N4.get(g); return c/N3[g[:3]] if c else LAM*_p(g[1:])
    if len(g)==3:
        c=N3.get(g); return c/N2[g[:2]] if c else LAM*_p(g[1:])
    if len(g)==2:
        c=N2.get(g); return c/N1[g[0]] if c else LAM*_p(g[1:])
    return N1.get(g,1)/TOT

LP4=[0.0]*(NA**4)
for a in AL:
    for b in AL:
        for c in AL:
            base=(AI[a]*NA+AI[b])*NA*NA+AI[c]*NA
            for d in AL: LP4[base+AI[d]]=math.log(_p(a+b+c+d))
FREQ=[M['uni'].get(c,0.0) for c in AL]

# variant -> base letterform, for the --merge experiment
MERGE={'L':'l','T':'t','G':'g','C':'c','K':'c','N':'n','J':'n','S':'s','O':'o','M':'m'}

def read_ct(path, merge=False):
    segs=[]
    for ln in open(path):
        if ln.startswith('#') or not ln.strip(): continue
        ln=re.sub(r'\[\[.*?\]\]',' | ',ln)
        parts=ln.split(None,1)
        if len(parts)<2: continue
        cur=[]
        for t in parts[1].split():
            t=t.rstrip('?')
            if t.startswith('<') or t in ('|','.',':','/','-','#','..'):
                if len(cur)>=4: segs.append(cur)
                cur=[]
            else:
                cur.append(MERGE.get(t,t) if merge else t)
        if len(cur)>=4: segs.append(cur)
    return segs

class Problem:
    def __init__(self, path='ct/no97_eye.txt', merge=False):
        self.segs=read_ct(path,merge)
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

    # ---- full scorer, supports NULL ----
    def full(self, key, mu=0.0):
        tot=0.0; n=0; ctr=[0]*NA
        for g in self.iseg:
            d=[key[i] for i in g]
            d=[x for x in d if x!=NULL]
            for x in d: ctr[x]+=1
            n+=len(d)
            for i in range(len(d)-3):
                tot+=LP4[((d[i]*NA+d[i+1])*NA+d[i+2])*NA+d[i+3]]
        if n==0: return -99.0, 0
        raw=tot/n
        if mu:
            pen=sum(abs(ctr[i]/n-FREQ[i]) for i in range(NA))
            return raw-mu*pen, n
        return raw, n

class State:
    __slots__=('P','key','cnt','wv','tot','mu')
    def __init__(self,P,key,mu):
        self.P=P; self.key=list(key); self.mu=mu
        self.cnt=[0]*NA
        for si in P.flat: self.cnt[key[si]]+=1
        self.wv=[0.0]*len(P.win); self.tot=0.0
        k=self.key; f=P.flat
        for wi,(a,b,c,d) in enumerate(P.win):
            v=LP4[((k[f[a]]*NA+k[f[b]])*NA+k[f[c]])*NA+k[f[d]]]
            self.wv[wi]=v; self.tot+=v
    def obj(self):
        nf=self.P.nf; pen=0.0
        for i in range(NA): pen+=abs(self.cnt[i]/nf-FREQ[i])
        return self.tot/nf-self.mu*pen
    def set(self,si,letter):
        old=self.key[si]
        if old==letter: return None
        P=self.P; k=self.key; f=P.flat; k[si]=letter
        n=len(P.sympos[si]); self.cnt[old]-=n; self.cnt[letter]+=n
        d=0.0; wv=self.wv; tw=P.symwin[si]
        for wi in tw:
            a,b,c,dd=P.win[wi]
            v=LP4[((k[f[a]]*NA+k[f[b]])*NA+k[f[c]])*NA+k[f[dd]]]
            d+=v-wv[wi]; wv[wi]=v
        self.tot+=d; return (si,old,letter,tw)
    def undo(self,u):
        si,old,letter,tw=u
        P=self.P; k=self.key; f=P.flat; k[si]=old
        n=len(P.sympos[si]); self.cnt[letter]-=n; self.cnt[old]+=n
        d=0.0; wv=self.wv
        for wi in tw:
            a,b,c,dd=P.win[wi]
            v=LP4[((k[f[a]]*NA+k[f[b]])*NA+k[f[c]])*NA+k[f[dd]]]
            d+=v-wv[wi]; wv[wi]=v
        self.tot+=d

def anneal(P,restarts,iters,mu,seed):
    rnd=random.Random(seed)
    order=[s for s,_ in P.cnt.most_common()]
    fr=sorted(range(NA), key=lambda i:-FREQ[i])
    best=-1e9; bestk=None
    for r in range(restarts):
        key=[fr[0]]*P.ns
        for rank,si in enumerate(order):
            key[si]=fr[min(rank,NA-1)] if r==0 else (rnd.choice(fr[:10]) if rank<10 else rnd.choice(fr))
        st=State(P,key,mu); cur=st.obj(); T0=0.30
        for it in range(iters):
            T=T0*(1.0-it/iters)+0.003
            si=rnd.randrange(P.ns)
            u=st.set(si,rnd.randrange(NA))
            if u is None: continue
            new=st.obj()
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: st.undo(u)
        if cur>best: best=cur; bestk=list(st.key)
    return best,bestk

def polish(P,key,rounds=8,allow_null=True,mu=4.0,maxnull=3):
    """Greedy full-scorer polish: try every letter, and NULL, for every symbol.

    The frequency penalty is kept during polishing and the number of nulls is capped:
    without both, the search discovers that deleting every hard position and mapping the
    rest onto e/t/n/r/s scores better than French, which is an artefact of normalising the
    log-probability per surviving character."""
    key=list(key); cur,_=P.full(key,mu)
    opts=list(range(NA))+([NULL] if allow_null else [])
    for _ in range(rounds):
        improved=False
        for si in range(P.ns):
            b=key[si]; bs=cur
            for v in opts:
                if v==key[si]: continue
                old=key[si]; key[si]=v
                if v==NULL and sum(1 for z in key if z==NULL)>maxnull:
                    key[si]=old; continue
                s,_=P.full(key,mu)
                if s>bs: bs=s; b=v
                key[si]=old
            if b!=key[si]:
                key[si]=b; cur=bs; improved=True
        if not improved: break
    return cur,key

def decode(P,key,path='ct/no97_eye.txt',merge=False):
    out=[]
    for ln in open(path):
        if ln.startswith('#') or not ln.strip(): continue
        parts=ln.split(None,1)
        if len(parts)<2: continue
        res=[]
        for t in re.findall(r'\[\[.*?\]\]|\S+', parts[1]):
            if t.startswith('[[') or t.startswith('<'): res.append(' '+t+' ')
            elif t in ('.',':','/','-','#','..'): res.append(t)
            else:
                s=t.rstrip('?'); s=MERGE.get(s,s) if merge else s
                if s in P.idx:
                    v=key[P.idx[s]]
                    res.append('' if v==NULL else AL[v])
                else: res.append('?')
        out.append(parts[0]+' '+''.join(res))
    return '\n'.join(out)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--merge',action='store_true'); ap.add_argument('--restarts',type=int,default=40)
    ap.add_argument('--iters',type=int,default=120000); ap.add_argument('--mu',type=float,default=4.0)
    ap.add_argument('--seed',type=int,default=1); ap.add_argument('--nonull',action='store_true')
    ap.add_argument('--maxnull',type=int,default=3)
    a=ap.parse_args()
    P=Problem(merge=a.merge)
    print(f'merge={a.merge} segments={len(P.segs)} chars={P.nf} symbols={P.ns}', file=sys.stderr)
    b,k=anneal(P,a.restarts,a.iters,a.mu,a.seed)
    raw,_=P.full(k)
    print(f'anneal obj {b:.4f}  raw {raw:.4f}', file=sys.stderr, flush=True)
    c,k=polish(P,k,allow_null=not a.nonull,mu=a.mu,maxnull=a.maxnull)
    raw,n=P.full(k)
    print(f'polished obj {c:.4f}  raw {raw:.4f} over {n} chars   (real French approx -1.93)')
    print('\nKEY')
    for s in P.syms:
        v=k[P.idx[s]]
        print(f'  {s} -> {"(null)" if v==NULL else AL[v]}')
    print()
    print(decode(P,k,merge=a.merge))
