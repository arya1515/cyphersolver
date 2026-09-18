"""Final solve of fr. 3621 no. 97 with the crib locked.

The group f H i n c t i G decodes to "chasteau" at two independent places in the cipher,
and Chasteauvillain stands in the clear on the same page, so those seven symbol values are
fixed here and the remaining symbols are searched against them.
"""
import re, random, collections, sys
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])

LOCK={'f':'c','H':'h','i':'a','n':'s','c':'t','t':'e','G':'u'}

def sweepL(P, st, mu, locked):
    improved=False
    for si in range(P.ns):
        if si in locked: continue
        cur=st.obj(); best=st.key[si]; bv=cur
        for L in range(NA):
            if L==st.key[si]: continue
            u=st.set(si,L)
            if u is None: continue
            v=st.obj()
            if v>bv: bv=v; best=L
            st.undo(u)
        if best!=st.key[si]:
            st.set(si,best); improved=True
    return improved

def run(P, mu, seed, iters):
    rnd=random.Random(seed)
    locked={P.idx[s] for s in LOCK if s in P.idx}
    fr=sorted(range(NA), key=lambda i:-FREQ[i])
    order=[s for s,_ in P.cnt.most_common()]
    key=[fr[0]]*P.ns
    for rank,si in enumerate(order): key[si]=fr[min(rank,NA-1)]
    for s,c in LOCK.items():
        if s in P.idx: key[P.idx[s]]=AI[c]
    st=State(P,key,mu)
    for _ in range(40):
        if not sweepL(P,st,mu,locked): break
    best=st.obj(); bestk=list(st.key)
    for it in range(iters):
        for _ in range(4):
            si=rnd.randrange(P.ns)
            if si in locked: continue
            st.set(si, rnd.randrange(NA))
        for _ in range(40):
            if not sweepL(P,st,mu,locked): break
        c=st.obj()
        if c>best: best=c; bestk=list(st.key)
        else:
            for si in range(P.ns): st.set(si,bestk[si])
    return best,bestk

def diverge(P,key):
    ctr=[0]*NA
    for si in P.flat: ctr[key[si]]+=1
    return sum(abs(ctr[i]/P.nf-FREQ[i]) for i in range(NA))

P=Problem()
best=-9e9; bestk=None
for mu in (0.0,1.0,2.0):
    for sd in range(1,13):
        b,k=run(P,mu,sd,220)
        raw,_=P.full(k)
        if diverge(P,k)>0.26: continue
        if raw>best:
            best=raw; bestk=list(k)
            print(f'  mu={mu} seed={sd} raw {raw:.4f}', file=sys.stderr, flush=True)
print(f'\nFINAL raw {best:.4f}  (real French -1.93; clean control -1.63;')
print( '   control with 6-12 systematically merged symbol pairs -2.15 to -2.23)\n')
print('KEY  (cipher symbol -> plaintext; the model folds u/v and i/j, as the period does)')
for s in P.syms:
    mark=' *locked by the chasteau crib' if s in LOCK else ''
    print(f'  {s} -> {AL[bestk[P.idx[s]]]}{mark}')
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
