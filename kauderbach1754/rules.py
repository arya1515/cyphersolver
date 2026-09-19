import itertools,math,collections,glob
from parse import segs
S=[s for f in sorted(glob.glob('decode/DOC*.txt')) for s in segs(f)]
res=[]
for rule in itertools.product((1,2,3),repeat=10):
  C=collections.Counter();n=0;digits=0
  for s in S:
    i=0
    while i<len(s):
      L=rule[int(s[i])]; t=s[i:i+L]; C[t]+=1; i+=L
  N=sum(C.values()); H=-sum(v/N*math.log2(v/N) for v in C.values())
  # bits per digit incl. vocabulary cost
  bpd=(H*N+len(C)*10)/6096
  res.append((bpd,rule,len(C),N))
res.sort()
for r in res[:15]: print(r)
