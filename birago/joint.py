# Joint annealing over segmentation (tokens of 1 or 2 digits, no prefix rule) and homophonic key. Italian 5-gram + unigram penalty.
import sys,math,re,collections,json,numpy as np,seg
AL=seg.AL; LET=seg.LET
class Joint:
    def __init__(self,src,letters='null',maxlen=2,seed=0):
        self.rnd=np.random.default_rng(seed)
        u=seg.units(open(src).read())
        # items: list of (kind,text). digits kept as runs; marks -> break; letters -> null or break
        self.runs=[]; self.layout=[]  # layout: sequence of ('R',run_index) or ('B',)
        for x in u:
            if x[0] in '%:+-': self.layout.append(('B',x))
            elif x.isalpha():
                if letters=='break': self.layout.append(('B',x))
            else: self.layout.append(('R',len(self.runs))); self.runs.append(x)
        self.maxlen=maxlen
        # segmentation: for each run, list of cut flags per digit (1 = token starts here); position 0 always 1
        self.cuts=[]
        for r in self.runs:
            c=np.ones(len(r),dtype=np.int8)
            for i in range(1,len(r)):
                if c[i-1]==1 and self.rnd.random()<0.5: c[i]=0   # random 1/2-digit segmentation
            self.cuts.append(c)
        self.key={}  # token string -> letter index
        self.rebuild()
    def tokens(self):
        toks=[]
        for kind,v in self.layout:
            if kind=='B': toks.append('#')
            else:
                r=self.runs[v]; c=self.cuts[v]; i=0
                while i<len(r):
                    j=i+1
                    while j<len(r) and c[j]==0: j+=1
                    toks.append(r[i:j]); i=j
        return toks
    def rebuild(self):
        self.toks=self.tokens()
        for t in self.toks:
            if t!='#' and t not in self.key: self.key[t]=LET[self.rnd.integers(len(LET))]
    def text_score(self,toks,key):
        p=np.array([26 if t=='#' else key[t] for t in toks])
        n=len(p); ok=np.ones(n-4,dtype=bool)
        for k in range(5): ok&=(p[k:n-4+k]!=26)
        W=np.where(ok)[0]
        q=p[W]*456976+p[W+1]*17576+p[W+2]*676+p[W+3]*26+p[W+4]
        s=float(seg.tab[q].sum())
        pf=p[p!=26]; cnt=np.bincount(pf,minlength=26); exp=seg.P1*len(pf)
        s-=seg.LAMBDA*float(((cnt-exp)**2/(exp+1)).sum())
        return s,len(W)
    def anneal(self,iters=300000,T0=8.0,Tend=0.2,log=0):
        cur,_=self.text_score(self.toks,self.key); best=cur; bestc=[c.copy() for c in self.cuts]; bestk=dict(self.key)
        lam=math.log(Tend/T0)/iters
        for it in range(iters):
            T=T0*math.exp(lam*it); r=self.rnd.random()
            if r<0.45:   # letter change
                t=self.rnd.choice(list(self.key.keys())); old=self.key[t]; self.key[t]=LET[self.rnd.integers(len(LET))]
                sc,_=self.text_score(self.toks,self.key)
                if sc>cur or self.rnd.random()<math.exp((sc-cur)/T): cur=sc
                else: self.key[t]=old
            elif r<0.6: # swap two letters
                ks=list(self.key.keys()); a,b=self.rnd.choice(len(ks),2,replace=False); ta,tb=ks[a],ks[b]
                self.key[ta],self.key[tb]=self.key[tb],self.key[ta]
                sc,_=self.text_score(self.toks,self.key)
                if sc>cur or self.rnd.random()<math.exp((sc-cur)/T): cur=sc
                else: self.key[ta],self.key[tb]=self.key[tb],self.key[ta]
            else:       # flip a cut (respecting maxlen)
                ri=self.rnd.integers(len(self.runs)); c=self.cuts[ri]
                if len(c)<2: continue
                i=self.rnd.integers(1,len(c)); old=c[i]; c[i]=1-old
                # enforce token length <= maxlen
                ok=True; run=0
                for f in c:
                    run=1 if f else run+1
                    if run>self.maxlen: ok=False; break
                if not ok: c[i]=old; continue
                toks=self.tokens()
                newkeys={t:LET[self.rnd.integers(len(LET))] for t in toks if t!='#' and t not in self.key}
                key2=dict(self.key); key2.update(newkeys)
                sc,_=self.text_score(toks,key2)
                if sc>cur or self.rnd.random()<math.exp((sc-cur)/T):
                    cur=sc; self.toks=toks; self.key=key2
                else: c[i]=old
            if cur>best: best=cur; bestc=[c.copy() for c in self.cuts]; bestk=dict(self.key)
            if log and it%log==0: print(f'it {it} T {T:.2f} cur {cur:.1f} best {best:.1f}',flush=True)
        self.cuts=bestc; self.key=bestk; self.toks=self.tokens(); return best
    def render(self):
        return ''.join('#' if t=='#' else AL[self.key[t]] for t in self.toks)
if __name__=='__main__':
    src=sys.argv[1]; iters=int(sys.argv[2]); restarts=int(sys.argv[3]); letters=sys.argv[4] if len(sys.argv)>4 else 'null'
    outs=[]
    for r in range(restarts):
        J=Joint(src,letters=letters,seed=r); b=J.anneal(iters)
        sc,nw=J.text_score(J.toks,J.key); lm=(sc+seg.LAMBDA*0)/nw
        used=collections.Counter(J.toks); two=sum(1 for t in used if len(t)==2)
        print(f'restart {r} score/window {sc/nw:.3f} windows {nw} tokens {len(J.toks)} distinct {len(used)} two-digit {two}',flush=True)
        print(J.render(),flush=True)
        outs.append((sc/nw,J.render(),dict((t,AL[v]) for t,v in J.key.items())))
    outs.sort(reverse=True); print('BEST'); print(outs[0][0]); print(outs[0][1]); print(json.dumps(outs[0][2],sort_keys=True))
