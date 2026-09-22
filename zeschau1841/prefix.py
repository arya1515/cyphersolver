from collections import Counter
from itertools import product
import math
s=''.join(l.split()[1] for l in open('ct_R5005.txt'))
def ent(c):
    N=sum(c.values());return -sum(v/N*math.log2(v/N) for v in c.values())
res=[]
for lens in ((1,2),(2,3),(1,2,3)):
  for assign in product(range(len(lens)),repeat=10):
    L=[lens[a] for a in assign]; i=0;tok=[]
    while i<len(s):
        n=L[int(s[i])];tok.append(s[i:i+n]);i+=n
    c=Counter(tok);N=len(tok)
    # bits per digit of unigram model - lower is more structure; penalize types
    h=ent(c)*N/len(s)
    res.append((round(h,3),lens,''.join(map(str,L)),len(c),N))
for r in sorted(res)[:15]:print(r)
