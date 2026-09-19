import math,collections,glob,sys
from parse import segs
S=[s for f in sorted(glob.glob('decode/DOC*.txt')) for s in segs(f)]
MAXL=int(sys.argv[1]) if len(sys.argv)>1 else 4
# init uniform-ish over all substrings
P=collections.Counter()
for s in S:
  for i in range(len(s)):
    for L in range(1,MAXL+1):
      if i+L<=len(s): P[s[i:i+L]]+=1
def norm(P):
  z=sum(P.values());return {k:math.log(v/z) for k,v in P.items() if v>0}
for it in range(40):
  lp=norm(P); C=collections.Counter()
  # forward-backward expected counts
  for s in S:
    n=len(s);a=[-1e18]*(n+1);a[0]=0
    for j in range(1,n+1):
      xs=[a[j-L]+lp[s[j-L:j]] for L in range(1,MAXL+1) if j-L>=0 and s[j-L:j] in lp]
      m=max(xs);a[j]=m+math.log(sum(math.exp(x-m) for x in xs))
    b=[-1e18]*(n+1);b[n]=0
    for i in range(n-1,-1,-1):
      xs=[b[i+L]+lp[s[i:i+L]] for L in range(1,MAXL+1) if i+L<=n and s[i:i+L] in lp]
      m=max(xs);b[i]=m+math.log(sum(math.exp(x-m) for x in xs))
    for i in range(n):
      for L in range(1,MAXL+1):
        w=s[i:i+L]
        if i+L<=n and w in lp: C[w]+=math.exp(a[i]+lp[w]+b[i+L]-a[n])
  # sparsity prior
  P=collections.Counter({k:max(v-0.5,0) for k,v in C.items()})
tot=sum(P.values())
print(len([k for k,v in P.items() if v>1]))
for k,v in P.most_common(90): print(k,round(v,1),end='  ')
