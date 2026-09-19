import json,sys,math,random,collections
import solve as B
LQ,FL=B.LQ,B.FL
V='a ai an au b be bi c ca ce ci co d da de di do du e em en er es et f fai fe g ga ge h hi i ia ie il ju k l la le ma me n na ne ni no nu o oi on ou p pour pr q que qui r ra re ri s sa se si son t te u vous x y z'.split()
D=json.load(open('pairs.json'))
segsT=[]
for f,tk in D:
  cur=[]
  for t in tk:
    if t.startswith('*'):
      if len(cur)>=3: segsT.append(cur)
      cur=[]
    else: cur.append(t)
  if len(cur)>=3: segsT.append(cur)
syms=sorted({t for sg in segsT for t in sg}); idx={t:i for i,t in enumerate(syms)}
segsI=[[idx[t] for t in sg] for sg in segsT]
n=len(syms); nv=len(V)
occ=collections.defaultdict(set)
for k,sg in enumerate(segsI):
  for i in sg: occ[i].add(k)
def segsc(key,k):
  t=''.join(V[key[i]] for i in segsI[k]); return sum(LQ.get(t[j:j+4],FL) for j in range(len(t)-3))
def run(seed,iters):
  rnd=random.Random(seed)
  # init by frequency: frequent codes -> frequent-looking values
  cnt=collections.Counter(i for sg in segsI for i in sg)
  order=[i for i,_ in cnt.most_common()]
  pref='e s a i t n r u l o d c p m de le v es en re que la q f b g h on et ou'.split()
  vals=[V.index(p) for p in pref if p in V]+[j for j in range(nv) if V[j] not in pref]
  key=[0]*n; used=set()
  for i,s in enumerate(order): key[s]=vals[i]
  for s in range(n):
    if s not in order: key[s]=vals[len(order)]
  inv={}
  for s in range(n): inv[key[s]]=s
  SS=[segsc(key,k) for k in range(len(segsI))]; cur=sum(SS); best=(cur,key[:])
  for it in range(iters):
    T=max(0.05, 8*(1-it/iters))
    a=rnd.randrange(n); v=rnd.randrange(nv)
    if key[a]==v: continue
    b=inv.get(v)
    ks=occ[a]|(occ[b] if b is not None else set())
    old={k:SS[k] for k in ks}
    va=key[a]; key[a]=v
    if b is not None: key[b]=va
    new={k:segsc(key,k) for k in ks}
    d=sum(new.values())-sum(old.values())
    if d>=0 or rnd.random()<math.exp(d/T):
      for k in ks: SS[k]=new[k]
      cur+=d; inv[v]=a
      if b is not None: inv[va]=b
      else: inv.pop(va,None)
      if cur>best[0]: best=(cur,key[:])
    else:
      key[a]=va
      if b is not None: key[b]=v
  return best
seed=int(sys.argv[1]); cur,key=run(seed,int(sys.argv[2]))
nt=sum(len(''.join(V[key[i]] for i in sg)) for sg in segsI)
print(cur/nt)
print(' '.join(f'{s}={V[k]}' for s,k in zip(syms,key)))
print('|'.join(''.join(V[key[i]] for i in sg) for sg in segsI)[:2500])
json.dump({s:V[k] for s,k in zip(syms,key)},open(f'permnom_{seed}.json','w'))
