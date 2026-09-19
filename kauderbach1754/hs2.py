import math,random,collections
import solve as B
LQ,FL=B.LQ,B.FL
ALPH='abcdefghijlmnopqrstuvxyz'
UF=collections.Counter(B.corp); _n=sum(UF.values()); UF={c:UF.get(c,1)/_n for c in ALPH}
def run(segsI,nsym,iters=200000,seed=0,T0=1.0,fixed=None,init=None,W=None):
  rnd=random.Random(seed)
  # text as list of symbols with -1 separators
  text=[]
  for sg in segsI: text+=sg+[-1,-1,-1]
  n=len(text)
  occ=collections.defaultdict(set)
  for i,t in enumerate(text):
    if t>=0:
      for j in range(i-3,i+1):
        if 0<=j<=n-4: occ[t].add(j)
  occ={k:sorted(v) for k,v in occ.items()}
  key=list(init) if init else [rnd.choice('esaitnrulodcmp') for _ in range(nsym)]
  if fixed:
    for s,c in fixed.items(): key[s]=c
  def q(j):
    a,b,c,d=text[j],text[j+1],text[j+2],text[j+3]
    if a<0 or b<0 or c<0 or d<0: return 0.0
    return LQ.get(key[a]+key[b]+key[c]+key[d],FL)
  def full(): return sum(q(j) for j in range(n-3))
  sf=collections.Counter(t for t in text if t>=0); NT=sum(sf.values()); W=W if W is not None else NT*1.0
  LC=collections.Counter()
  for t,c in sf.items(): LC[key[t]]+=c
  def pen(): return -W*sum((LC[c]/NT)*math.log10(max(LC[c],0.5)/NT/UF[c]) for c in ALPH if LC[c]>0)
  cur=full()+pen(); best=(cur,key[:]); free=[s for s in range(nsym) if not(fixed and s in fixed) and s in occ]
  for it in range(iters):
    T=T0*(1-it/iters)+0.01
    s=rnd.choice(free); old=key[s]; new=rnd.choice(ALPH)
    if new==old: continue
    js=occ[s]; p0=pen(); before=sum(q(j) for j in js); key[s]=new; LC[old]-=sf[s]; LC[new]+=sf[s]; d=sum(q(j) for j in js)-before+pen()-p0
    if d>=0 or rnd.random()<math.exp(d/T): cur+=d
    else: key[s]=old; LC[new]-=sf[s]; LC[old]+=sf[s]
    if cur>best[0]: best=(cur,key[:])
  key=best[1]; return full(),key
