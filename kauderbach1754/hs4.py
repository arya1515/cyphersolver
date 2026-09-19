# coordinate ascent; symbol values may be letters or short syllables; score = quadgram over expanded text + unigram penalty
import math,random,collections
import solve as B
LQ,FL=B.LQ,B.FL
ALPH=list('abcdefghijlmnopqrstuvxyz')
bg=collections.Counter(B.corp[i:i+2] for i in range(len(B.corp)-1))
SYL=[b for b,_ in bg.most_common(40)]+['que','les','des','ent','qui','par','pour','ment','roi','tion','ons','ait']
VALS=ALPH+[s for s in SYL if s not in ALPH]
UF=collections.Counter(B.corp); _n=sum(UF.values()); UF={c:UF.get(c,1)/_n for c in ALPH}
def score_text(segs,key):
  s=0.0;LC=collections.Counter()
  for sg in segs:
    t=''.join(key[i] for i in sg); LC.update(t)
    s+=sum(LQ.get(t[j:j+4],FL) for j in range(len(t)-3))
  NT=sum(LC.values())
  return s, LC, NT
def run(segsI,nsym,rounds=15,seed=0,W=10,restarts=4,log=False,sylcost=0.5):
  rnd=random.Random(seed)
  occseg=collections.defaultdict(set)
  for k,sg in enumerate(segsI):
    for i in sg: occseg[i].add(k)
  segsc={}
  def segscore(k,key):
    t=''.join(key[i] for i in segsI[k]); return sum(LQ.get(t[j:j+4],FL) for j in range(len(t)-3)), t
  best=(-1e18,None)
  for r in range(restarts):
    key=[rnd.choice('esaitnrulodc') for _ in range(nsym)] if not best[1] else best[1][:]
    if best[1]:
      for s in rnd.sample(range(nsym),nsym//4): key[s]=rnd.choice('esaitnrulodc')
    for rd in range(rounds):
      ch=0
      for s in rnd.sample(range(nsym),nsym):
        ks=sorted(occseg[s]); bv,bc=None,key[s]
        for v in VALS:
          key[s]=v
          tot=0.0; LC=collections.Counter(); 
          for k in ks: sc,t=segscore(k,key); tot+=sc
          # penalty computed approximately on whole text only for chosen later; use per-length cost for syllables
          tot-=sylcost*(len(v)-1)*len(ks)
          if bv is None or tot>bv: bv,bc=tot,v
        if bc!=key[s]: ch+=1
        key[s]=bc
      if not ch: break
    s,LC,NT=score_text(segsI,key)
    pen=-W*NT*sum((LC[c]/NT)*math.log10(LC[c]/NT/UF[c]) for c in ALPH if LC[c]>0)
    tot=(s+pen)/NT
    if log: print(r,tot)
    if tot>best[0]: best=(tot,key[:])
  return best
