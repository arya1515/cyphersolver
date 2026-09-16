# Syllabic hypothesis: each two-digit token is a letter or a CV syllable; code groups and wavy sign are breaks; nulls dropped.
import sys,json,math,time,random,numpy as np,ng5it
from multiprocessing import Pool
tab=ng5it.load()
CONS='bcdfghlmnpqrstz'; VOW='aeiou'
UNITS=list('abcdefghilmnopqrstuz')+[c+v for c in CONS for v in VOW]+['ch'+v for v in VOW]+['gh'+v for v in VOW]+['qu'+v for v in 'aeio']
def render(toks,mp):
    segs=[];cur=[]
    for t in toks:
        if t[0]=='#':
            if cur: segs.append(''.join(cur)); cur=[]
        else: cur.append(mp[t])
    if cur: segs.append(''.join(cur))
    return segs
def score(segs):
    s=0.0; n=0
    for sg in segs:
        if len(sg)>=5: s+=ng5it.score(tab,ng5it.toidx(sg)); n+=len(sg)-4
    return s,n
def anneal(toks,iters,seed,T0=6.0,Tend=0.1):
    rnd=random.Random(seed); syms=sorted(set(t for t in toks if t[0]!='#'))
    mp={s:rnd.choice(UNITS) for s in syms}
    cur,n=score(render(toks,mp)); best=cur; bestmp=dict(mp); lam=math.log(Tend/T0)/iters
    for it in range(iters):
        T=T0*math.exp(lam*it); s=rnd.choice(syms); old=mp[s]
        if rnd.random()<0.85: mp[s]=rnd.choice(UNITS)
        else:
            s2=rnd.choice(syms); mp[s],mp[s2]=mp[s2],mp[s]; old=(s2,mp[s2],old)
        sc,n=score(render(toks,mp))
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            cur=sc
            if cur>best: best=cur; bestmp=dict(mp)
        else:
            if isinstance(old,tuple): s2,v2,v=old; mp[s2]=v2; mp[s]=v
            else: mp[s]=old
    segs=render(toks,bestmp); sc,n=score(segs)
    return sc/n,bestmp,' # '.join(segs)
def make_control(seed,ntok=228):
    rnd=random.Random(seed); txt=open('corpus_clean.txt').read()
    i=rnd.randrange(500000,len(txt)-3000); p=txt[i:i+2000]
    # segment plaintext greedily into CV syllables and letters, encipher with a random table
    units=[];j=0
    while j<len(p) and len(units)<ntok:
        if j+2<len(p) and p[j:j+2] in ('ch','gh') and p[j+2] in VOW: units.append(p[j:j+3]); j+=3
        elif j+1<len(p) and p[j] in CONS and p[j+1] in VOW: units.append(p[j:j+2]); j+=2
        elif p[j] in 'abcdefghilmnopqrstuz': units.append(p[j]); j+=1
        else: j+=1
    table={}; nums=[f'{k:02d}' for k in range(100)]; rnd.shuffle(nums)
    toks=[]
    for u in units:
        if u not in table:
            if not nums: return None
            table[u]=nums.pop()
        toks.append(table[u])
    for pos in sorted(rnd.sample(range(len(toks)),25),reverse=True): toks.insert(pos,'#x')
    return toks,''.join(units),table
def job(a):
    kind,arg,seed,iters=a
    if kind=='control':
        toks,pl,table=make_control(int(arg))
    else:
        P=json.load(open('pairings.json')); toks=[t if t!='|' else '#|' for t in P[int(arg)]]; pl=None
    sc,mp,txt=anneal(toks,iters,seed)
    acc=None
    if pl:
        inv={v:k for k,v in table.items()}; syms=sorted(set(t for t in toks if t[0]!='#'))
        acc=sum(1 for s in syms if mp[s]==inv.get(s))/len(syms)
    return kind,arg,seed,sc,acc,txt
if __name__=='__main__':
    kind,arg,iters,seeds=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
    t=time.time()
    with Pool(min(seeds,7)) as p:
        for kind,arg,seed,sc,acc,txt in p.imap_unordered(job,[(kind,arg,s,iters) for s in range(seeds)]):
            print(f'{kind} {arg} seed {seed}: 5gram/letter {sc:.3f} unit-acc={acc} | {txt[:220]} ({time.time()-t:.0f}s)',flush=True)
