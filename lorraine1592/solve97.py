"""Solve the cipher of BnF fr. 3621 no. 97 (Charles III de Lorraine to the comte de
Vaudemont, 18 June 1592), from the by-eye transcription in ct/no97_eye.txt.

The transcription's symbol frequencies match French rank-for-rank through the top fourteen
symbols, so the cipher is modelled as a substitution with homophones (44 symbols, 22
letters) plus a numeric nomenclator. Nomenclator figures, punctuation and the clear-text
stretches break the letter stream; no n-gram is scored across a break.

Scoring is a character 4-gram model of Montaigne with stupid backoff, plus a penalty on the
divergence between the induced letter frequency and French, which stops the annealer
collapsing the key onto a single high-frequency letter.
"""
import re, json, math, random, collections, sys

M=json.load(open('src/fr_lm.json'))
AL=M['al']; N1=M['n1']; N2=M['n2']; N3=M['n3']; N4=M['n4']
TOT=sum(N1.values()); LAM=0.4
AI={c:i for i,c in enumerate(AL)}; NA=len(AL)

def _p(g):
    if len(g)==4:
        c=N4.get(g)
        return c/N3[g[:3]] if c else LAM*_p(g[1:])
    if len(g)==3:
        c=N3.get(g)
        return c/N2[g[:2]] if c else LAM*_p(g[1:])
    if len(g)==2:
        c=N2.get(g)
        return c/N1[g[0]] if c else LAM*_p(g[1:])
    return N1.get(g,1)/TOT

# LP4 flat table indexed a*NA^3 + b*NA^2 + c*NA + d
LP4=[0.0]*(NA**4)
for a in AL:
    for b in AL:
        for c in AL:
            base=(AI[a]*NA+AI[b])*NA*NA+AI[c]*NA
            for d in AL: LP4[base+AI[d]]=math.log(_p(a+b+c+d))
FREQ=[M['uni'].get(c,0.0) for c in AL]

def read_ct(path='ct/no97_eye.txt'):
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
            else: cur.append(t)
        if len(cur)>=4: segs.append(cur)
    return segs

SEGS=read_ct()
SYMS=sorted({s for g in SEGS for s in g}); NS=len(SYMS)
IDX={s:i for i,s in enumerate(SYMS)}
ISEG=[[IDX[s] for s in g] for g in SEGS]
NCH=sum(len(g) for g in SEGS)
# flat position array with segment boundaries
POS=[]; WIN=[]          # WIN: list of 4-tuples of flat positions
flat=[]
for g in ISEG:
    st=len(flat); flat.extend(g)
    for i in range(len(g)-3): WIN.append((st+i,st+i+1,st+i+2,st+i+3))
NF=len(flat)
SYMPOS=[[] for _ in range(NS)]
for p,si in enumerate(flat): SYMPOS[si].append(p)
WINOF=[[] for _ in range(NF)]
for wi,w in enumerate(WIN):
    for p in w: WINOF[p].append(wi)
for p in range(NF): WINOF[p]=sorted(set(WINOF[p]))
SYMWIN=[sorted({wi for p in SYMPOS[s] for wi in WINOF[p]}) for s in range(NS)]

class State:
    __slots__=('key','cnt','wv','tot','mu')
    def __init__(self, key, mu):
        self.key=list(key); self.mu=mu
        self.cnt=[0]*NA
        for si in flat: self.cnt[key[si]]+=1
        self.wv=[0.0]*len(WIN); self.tot=0.0
        k=self.key
        for wi,(a,b,c,d) in enumerate(WIN):
            v=LP4[((k[flat[a]]*NA+k[flat[b]])*NA+k[flat[c]])*NA+k[flat[d]]]
            self.wv[wi]=v; self.tot+=v
    def obj(self):
        pen=0.0
        for i in range(NA): pen+=abs(self.cnt[i]/NF - FREQ[i])
        return self.tot/NF - self.mu*pen
    def set(self, si, letter):
        old=self.key[si]
        if old==letter: return None
        k=self.key; k[si]=letter
        n=len(SYMPOS[si])
        self.cnt[old]-=n; self.cnt[letter]+=n
        delta=0.0; touched=SYMWIN[si]; wv=self.wv
        for wi in touched:
            a,b,c,d=WIN[wi]
            v=LP4[((k[flat[a]]*NA+k[flat[b]])*NA+k[flat[c]])*NA+k[flat[d]]]
            delta+=v-wv[wi]; wv[wi]=v
        self.tot+=delta
        return (si,old,letter,touched)
    def undo(self, u):
        si,old,letter,touched=u
        k=self.key; k[si]=old
        n=len(SYMPOS[si])
        self.cnt[letter]-=n; self.cnt[old]+=n
        delta=0.0; wv=self.wv
        for wi in touched:
            a,b,c,d=WIN[wi]
            v=LP4[((k[flat[a]]*NA+k[flat[b]])*NA+k[flat[c]])*NA+k[flat[d]]]
            delta+=v-wv[wi]; wv[wi]=v
        self.tot+=delta

def solve(restarts, iters, mu, seed):
    rnd=random.Random(seed)
    cnt=collections.Counter(flat)
    order=[s for s,_ in cnt.most_common()]
    fr=sorted(range(NA), key=lambda i:-FREQ[i])
    best=-1e9; bestk=None
    for r in range(restarts):
        key=[fr[0]]*NS
        for rank,si in enumerate(order):
            key[si]=fr[min(rank,NA-1)] if r==0 else (rnd.choice(fr[:10]) if rank<10 else rnd.choice(fr))
        st=State(key,mu); cur=st.obj(); T0=0.30
        for it in range(iters):
            T=T0*(1.0-it/iters)+0.003
            si=rnd.randrange(NS)
            u=st.set(si, rnd.randrange(NA))
            if u is None: continue
            new=st.obj()
            if new>cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: st.undo(u)
        if cur>best:
            best=cur; bestk=list(st.key)
            print(f'  restart {r:3d} obj {cur:.4f}  raw {st.tot/NF:.4f}', file=sys.stderr, flush=True)
    return best,bestk

def decode(key):
    out=[]
    for ln in open('ct/no97_eye.txt'):
        if ln.startswith('#') or not ln.strip(): continue
        parts=ln.split(None,1)
        if len(parts)<2: continue
        res=[]
        for t in re.findall(r'\[\[.*?\]\]|\S+', parts[1]):
            if t.startswith('[[') or t.startswith('<'): res.append(' '+t+' ')
            elif t in ('.',':','/','-','#','..'): res.append(t)
            else:
                s=t.rstrip('?')
                res.append(AL[key[IDX[s]]] if s in IDX else '?')
        out.append(parts[0]+' '+''.join(res))
    return '\n'.join(out)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--restarts',type=int,default=30); ap.add_argument('--iters',type=int,default=40000)
    ap.add_argument('--mu',type=float,default=4.0); ap.add_argument('--seed',type=int,default=1)
    a=ap.parse_args()
    print(f'segments {len(SEGS)} chars {NF} symbols {NS} windows {len(WIN)}', file=sys.stderr)
    b,k=solve(a.restarts,a.iters,a.mu,a.seed)
    st=State(k,a.mu)
    print(f'\nbest obj {b:.4f}   raw 4-gram log-prob/char {st.tot/NF:.4f}   (real French approx -1.93)\n')
    print('KEY  (cipher symbol -> plaintext letter)')
    for s in SYMS: print(f'  {s} -> {AL[k[IDX[s]]]}')
    print()
    print(decode(k))
