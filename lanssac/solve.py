"""Homophonic annealer for the Lanssac 1573 cipher: symbol -> letter (or short code), French 5-gram score.
usage: python solve.py [seeds] [--free]   (--free drops the pinned letters, as a control)"""
import sys, random, math, numpy as np, collections
ALPHA='abcdefghiklmnopqrstuvxyz'; IDX={c:i for i,c in enumerate(ALPHA)}
TAB=np.load('../sp53/fr5.npy')
CODES=['et','pour','de','que','il','st','ch','ou','en','nous','vous','par','les','la','le','car','qu','ie','ent']
PIN={'X':'e','ast':'e','G':'e','i':'i','s':'n','nn':'n','pi':'a','T':'a','Y':'p','g':'s','7':'c','8':'m','c':'o',
     '3':'t','oo':'g','F':'r','phi':'r','ff':'u','ot':'u','Z':'car','st':'st'}
def load(path='tokens.txt'):
    lines=[]; sec=None
    for l in open(path,encoding='utf-8'):
        l=l.strip()
        if not l or l.startswith('#'): continue
        if l.startswith('@'): sec=l[1:]; continue
        lines.append((sec,l.split()))
    return lines
def score(text):
    t=np.fromiter((IDX[ch] for ch in text),dtype=np.int64)
    if len(t)<5: return 0.0
    return float(TAB[t[:-4],t[1:-3],t[2:-2],t[3:-1],t[4:]].sum())
def render(lines,m):
    return ''.join(''.join(m[t] for t in toks) for _,toks in lines)
def anneal(lines,pin,seed,iters=60000,T0=3.0):
    rnd=random.Random(seed)
    syms=sorted({t for _,toks in lines for t in toks})
    free=[s for s in syms if s not in pin]
    cands=list(ALPHA)+CODES
    m={s:pin[s] for s in syms if s in pin}
    for s in free: m[s]=rnd.choice(list(ALPHA))
    cur=score(render(lines,m)); best=(cur,dict(m))
    for k in range(iters):
        T=T0*(1-k/iters)+0.05
        s=rnd.choice(free); old=m[s]
        if rnd.random()<0.85: m[s]=rnd.choice(ALPHA)
        else: m[s]=rnd.choice(cands)
        new=score(render(lines,m))
        if new>=cur or rnd.random()<math.exp((new-cur)/T): cur=new
        else: m[s]=old
        if cur>best[0]: best=(cur,dict(m))
    return best
if __name__=='__main__':
    seeds=int(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1].isdigit() else 4
    pin={} if '--free' in sys.argv else PIN
    lines=load()
    n=sum(len(t) for _,t in lines); print('tokens',n)
    res=[]
    for sd in range(seeds):
        sc,m=anneal(lines,pin,sd); res.append((sc,m)); print('seed',sd,round(sc,1),flush=True)
    res.sort(key=lambda r:-r[0]); sc,m=res[0]
    print('BEST',round(sc,1))
    for s in sorted(m,key=lambda s:-sum(t==s for _,tk in lines for t in tk)): print(f'{s}={m[s]}',end=' ')
    print()
    for sec,toks in lines: print(sec[:6].ljust(6),' '.join(m[t] for t in toks))
    # agreement between seeds
    for sc2,m2 in res[1:]:
        dif=[s for s in m if m[s]!=m2[s]]; print('seed diff',round(sc2,1),len(dif),dif)
