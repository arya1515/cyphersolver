import math,random,collections,glob,sys,unicodedata,re
from parse import segs
def clean(t):
  t=unicodedata.normalize('NFD',t.lower()); return re.sub('[^a-z]','',t)
import os
corp=clean(open(os.environ['CORP'],encoding='utf8').read()) if os.environ.get('CORP') else clean(open('../affry1757/corpus_fr.txt',encoding='utf8').read()+open('../hellen1752/corpus_fr.txt',encoding='utf8').read())
Q=collections.Counter(corp[i:i+4] for i in range(len(corp)-3)); N=sum(Q.values())
LQ={k:math.log10(v/N) for k,v in Q.items()}; FL=math.log10(0.01/N)
def sc(p): return sum(LQ.get(p[i:i+4],FL) for i in range(len(p)-3))
S=[s for f in sorted(glob.glob('decode/DOC*.txt')) for s in segs(f)]
def tokens(rule):
  out=[]
  for s in S:
    i=0;seg=[]
    while i<len(s):
      L=rule[int(s[i])]; seg.append(s[i:i+L]); i+=L
    out.append(seg)
  return out
def solve(rule,iters=40000,restarts=4,seed=0):
  segsT=tokens(rule); syms=sorted({t for sg in segsT for t in sg})
  idx={t:i for i,t in enumerate(syms)}; segsI=[[idx[t] for t in sg] for sg in segsT if len(sg)>=4]
  letters='esaitnrulodcmpvqfbghjxyz'
  rnd=random.Random(seed);best=(-1e9,None)
  for r in range(restarts):
    key=[rnd.choice(letters[:12]) for _ in syms]
    dec=lambda k:[''.join(k[i] for i in sg) for sg in segsI]
    cur=sum(sc(p) for p in dec(key))
    T=5.0
    for it in range(iters):
      k2=key[:]; k2[rnd.randrange(len(syms))]=rnd.choice(letters)
      s2=sum(sc(p) for p in dec(k2))
      if s2>cur or rnd.random()<math.exp((s2-cur)/T): key,cur=k2,s2
      T=max(0.2,5.0*(1-it/iters))
    if cur>best[0]: best=(cur,key)
  cur,key=best; nt=sum(len(s) for s in segsI)
  txt=''.join(''.join(key[i] for i in sg)+'|' for sg in segsI)
  return cur/nt,dict(zip(syms,key)),txt
if __name__=='__main__':
  rule=tuple(int(c) for c in sys.argv[1])
  s,k,t=solve(rule,int(sys.argv[2]) if len(sys.argv)>2 else 20000,2)
  print(rule,round(s,3));print(k);print(t[:1500])
