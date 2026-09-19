import math,random,collections
import solve as B
LQ,FL=B.LQ,B.FL
ALPH='abcdefghijlmnopqrstuvxyz'
UF=collections.Counter(B.corp); _n=sum(UF.values()); UF={c:UF.get(c,1)/_n for c in ALPH}
def run(segsI,nsym,allowed=None,rounds=30,seed=0,fixed=None,init=None,W=1.0,restarts=5,log=False):
  rnd=random.Random(seed)
  text=[]
  for sg in segsI: text+=sg+[-1,-1,-1]
  n=len(text)
  occ=collections.defaultdict(set)
  for i,t in enumerate(text):
    if t>=0:
      for j in range(i-3,i+1):
        if 0<=j<=n-4: occ[t].add(j)
  occ={k:sorted(v) for k,v in occ.items()}
  sf=collections.Counter(t for t in text if t>=0); NT=sum(sf.values()); W=W*NT
  fixed=fixed or {}
  free=[s for s in occ if s not in fixed]
  def q(key,j):
    a,b,c,d=text[j],text[j+1],text[j+2],text[j+3]
    if a<0 or b<0 or c<0 or d<0: return 0.0
    return LQ.get(key[a]+key[b]+key[c]+key[d],FL)
  def pen(LC): return -W*sum((LC[c]/NT)*math.log10(LC[c]/NT/UF[c]) for c in ALPH if LC[c]>0)
  def total(key):
    LC=collections.Counter()
    for t,c in sf.items(): LC[key[t]]+=c
    return sum(q(key,j) for j in range(n-3))+pen(LC)
  best=(-1e18,None)
  for r in range(restarts):
    if init and r==0: key=list(init)
    elif best[1] and r>0:
      key=best[1][:]
      for s in rnd.sample(free,max(1,len(free)//4)): key[s]=rnd.choice(allowed[s] if allowed else 'esaitnrulodc')
    else: key=[rnd.choice(allowed[i] if allowed else 'esaitnrulodc') for i in range(nsym)]
    for s,c in fixed.items(): key[s]=c
    LC=collections.Counter()
    for t,c in sf.items(): LC[key[t]]+=c
    for rd in range(rounds):
      changed=0; order=free[:]; rnd.shuffle(order)
      for s in order:
        old=key[s]; js=occ[s]; LC[old]-=sf[s]
        bestc,bestv=old,None
        for c in (allowed[s] if allowed else ALPH):
          key[s]=c; LC[c]+=sf[s]
          v=sum(q(key,j) for j in js)+pen(LC)
          LC[c]-=sf[s]
          if bestv is None or v>bestv: bestv,bestc=v,c
        key[s]=bestc; LC[bestc]+=sf[s]
        if bestc!=old: changed+=1
      if not changed: break
    sc=total(key)
    if log: print(r,sc/NT)
    if sc>best[0]: best=(sc,key[:])
  return best
