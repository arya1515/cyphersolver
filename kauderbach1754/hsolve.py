import math,random,collections,sys
import solve as B
LQ,FL=B.LQ,B.FL
T0=3
L='abcdefghijlmnopqrstuvxyz'
def run(segsI,nsym,iters=300000,seed=0,fixed=None):
  rnd=random.Random(seed)
  text=[t for sg in segsI for t in sg+[-1]]
  occ=collections.defaultdict(list)
  for i,t in enumerate(text):
    if t>=0: occ[t].append(i)
  key=[rnd.choice('esaitnrulodc') for _ in range(nsym)]
  if fixed:
    for s,c in fixed.items(): key[s]=c
  def ch(i): t=text[i]; return '|' if t<0 else key[t]
  def q(i):
    g=''.join(ch(j) for j in range(i,i+4)) if i+4<=len(text) else '|'
    return 0 if '|' in g else LQ.get(g,FL)
  cur=sum(q(i) for i in range(len(text)))
  best=(cur,key[:])
  for it in range(iters):
    T=T0*(1-it/iters)+0.02
    s=rnd.randrange(nsym)
    if fixed and s in fixed: continue
    old=key[s]; new=rnd.choice(L)
    if new==old: continue
    starts=sorted({j for i in occ[s] for j in range(i-3,i+1) if j>=0})
    before=sum(q(j) for j in starts); key[s]=new; after=sum(q(j) for j in starts)
    d=after-before
    if d>=0 or rnd.random()<math.exp(d/T): cur+=d
    else: key[s]=old
    if cur>best[0]: best=(cur,key[:])
  return best
if __name__=='__main__':
  rule=tuple(int(c) for c in sys.argv[1])
  segsT=B.tokens(rule); syms=sorted({t for sg in segsT for t in sg}); idx={t:i for i,t in enumerate(syms)}
  segsI=[[idx[t] for t in sg] for sg in segsT if len(sg)>=4]
  nt=sum(map(len,segsI))
  sc,key=run(segsI,len(syms),int(sys.argv[2]),int(sys.argv[3]) if len(sys.argv)>3 else 0)
  print(rule,round(sc/nt,3),len(syms))
  print(' '.join(f'{s}={k}' for s,k in zip(syms,key)))
  print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:1200])
