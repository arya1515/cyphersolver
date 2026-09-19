import math,random,collections
import solve as B
LQ,FL=B.LQ,B.FL
ALPH='abcdefghijlmnopqrstuvxyz'
SYL=['de','le','la','les','des','que','qui','et','en','es','re','ou','on','ent','ai','an','in','ion','ment','par','pour','roi','se','ce','ne','ur','er','ns','nt','te','me','st','il']
VALS=list(ALPH)+SYL
UF=collections.Counter(B.corp); _n=sum(UF.values()); UF={c:UF.get(c,1)/_n for c in ALPH}
def run(segsI,nsym,rounds=20,seed=0,W=10,restarts=5,log=False,init=None,vals=VALS):
  rnd=random.Random(seed)
  occ=collections.defaultdict(list)
  for k,sg in enumerate(segsI):
    for i in set(sg): occ[i].append(k)
  sf=collections.Counter(i for sg in segsI for i in sg)
  def segsc(key,k):
    t=''.join(key[i] for i in segsI[k]); return sum(LQ.get(t[j:j+4],FL) for j in range(len(t)-3))
  def pen(LC):
    NT=sum(LC.values())
    return -W*NT*sum((LC[c]/NT)*math.log10(LC[c]/NT/UF[c]) for c in ALPH if LC[c]>0)
  def addv(LC,v,m):
    for ch in v: LC[ch]+=m
  best=(-1e18,None)
  for r in range(restarts):
    if r==0 and init: key=list(init)
    elif best[1]:
      key=best[1][:]
      for s in rnd.sample(range(nsym),nsym//4): key[s]=rnd.choice('esaitnrulodc')
    else: key=[rnd.choice('esaitnrulodc') for _ in range(nsym)]
    LC=collections.Counter()
    for s,c in sf.items(): addv(LC,key[s],c)
    SS=[segsc(key,k) for k in range(len(segsI))]
    for rd in range(rounds):
      ch=0
      for s in rnd.sample(range(nsym),nsym):
        old=key[s]; ks=occ[s]; base=sum(SS[k] for k in ks); addv(LC,old,-sf[s])
        bv=None
        for v in vals:
          key[s]=v; addv(LC,v,sf[s])
          val=sum(segsc(key,k) for k in ks)-base+pen(LC)
          addv(LC,v,-sf[s])
          if bv is None or val>bv: bv,bc=val,v
        key[s]=bc; addv(LC,bc,sf[s])
        for k in ks: SS[k]=segsc(key,k)
        if bc!=old: ch+=1
      if not ch: break
    NT=sum(LC.values()); tot=(sum(SS)+pen(LC))/NT
    if log: print(r,tot,flush=True)
    if tot>best[0]: best=(tot,key[:])
  return best
