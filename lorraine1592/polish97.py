"""Refine the recovered key for fr. 3621 no. 97 with a word-level score.

The 4-gram search reaches -2.17 and already yields readable French: "chasteau" twice,
munitions, promesses, resolution, secours, quartiers, "ramener mon armee". To sharpen the
remaining symbols this adds a dictionary-coverage term - the fraction of each decoded
segment that a concatenation of French word forms can cover - which rewards keys that make
whole words rather than merely plausible letter runs.
"""
import re, json, collections, random, sys
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])
from search import sweep

# ---- word list ----
raw=open('src/corpus_fr.txt',encoding='utf-8',errors='replace').read().lower()
raw=re.sub(r'[^a-z]',' ',raw).translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
wc=collections.Counter(raw.split())
WORDS={w for w,k in wc.items() if k>=8 and 2<=len(w)<=14}
WORDS |= {'a','y','i','o','u'}
# names and terms from this letter's own clear text and postscript
for w in ('chasteauuilain','chasteauuillain','chaulmont','buzonuille','uaudemont','lorraine',
          'nancy','lafauche','faulche','glosiere','munitions','munition','armee','artillerie',
          'siege','canon','poudre','soldatz','regiment','trouppes','monsieur','monseigneur',
          'filz','duc','conte','sieur','promesse','promesses','resolution','secours','quartiers'):
    WORDS.add(w)
MAXW=max(len(w) for w in WORDS)
print(f'word forms {len(WORDS)}', file=sys.stderr)

def coverage(s):
    """max characters of s coverable by non-overlapping dictionary words (gaps allowed)."""
    n=len(s); best=[0]*(n+1)
    for i in range(1,n+1):
        b=best[i-1]
        for L in range(2, min(MAXW,i)+1):
            if s[i-L:i] in WORDS:
                v=best[i-L]+L
                if v>b: b=v
        best[i]=b
    return best[n]

class WState(State):
    """State plus the word-coverage term."""
    def cov(self):
        k=self.key; tot=0; n=0
        for g in self.P.iseg:
            s=''.join(AL[k[i]] for i in g)
            tot+=coverage(s); n+=len(s)
        return tot/n

def objective(st, beta, mu):
    return st.tot/st.P.nf - mu*_pen(st) + beta*st.cov()
def _pen(st):
    nf=st.P.nf
    return sum(abs(st.cnt[i]/nf-FREQ[i]) for i in range(NA))

def wsweep(P, st, beta, mu):
    improved=False
    for si in range(P.ns):
        cur=objective(st,beta,mu); best=st.key[si]; bv=cur
        for L in range(NA):
            if L==st.key[si]: continue
            u=st.set(si,L)
            if u is None: continue
            v=objective(st,beta,mu)
            if v>bv: bv=v; best=L
            st.undo(u)
        if best!=st.key[si]:
            st.set(si,best); improved=True
    return improved

P=Problem()
# start from the key the 4-gram search found
START={'A':'e','B':'p','C':'t','D':'s','E':'c','F':'o','G':'u','H':'h','J':'s','K':'u','L':'u',
 'M':'e','N':'r','O':'d','P':'n','Q':'a','R':'o','S':'n','T':'e','U':'s','V':'c','W':'e','Y':'e',
 'Z':'r','a':'i','b':'p','c':'t','d':'q','f':'c','g':'u','i':'a','j':'n','m':'y','n':'s','o':'r',
 'p':'n','q':'d','r':'o','s':'n','t':'e','v':'r','x':'s','y':'l','z':'m'}
key=[AI[START.get(s,'e')] for s in P.syms]
rnd=random.Random(5)
best=None; bestk=None
for beta in (0.0,0.6,1.2,2.0):
    st=WState(P,key,0.0)
    for _ in range(30):
        if not wsweep(P,st,beta,1.0): break
    for kick in range(60):
        for _ in range(3): st.set(rnd.randrange(P.ns), rnd.randrange(NA))
        for _ in range(30):
            if not wsweep(P,st,beta,1.0): break
        o=objective(st,beta,1.0)
        if best is None or o>best:
            best=o; bestk=list(st.key)
        else:
            for si in range(P.ns): st.set(si,bestk[si])
    st2=WState(P,bestk,0.0)
    raw,_=P.full(bestk)
    print(f'beta={beta}  raw {raw:.4f}  coverage {st2.cov()*100:.1f}%', file=sys.stderr, flush=True)
st=WState(P,bestk,0.0)
raw,_=P.full(bestk)
print(f'\nFINAL raw {raw:.4f}   word coverage {st.cov()*100:.1f}%\n')
print('KEY  (cipher symbol -> plaintext; u covers u and v, i covers i and j)')
for s in P.syms: print(f'  {s} -> {AL[bestk[P.idx[s]]]}')
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
        else: res.append(km.get(t.rstrip('?'),'·'))
    print(parts[0]+' '+''.join(res))
