"""Matched control for the failed alignment: how many groups does the same search
place when the cipher sequence is shuffled, or the plaintext is a different French text?
If the real run is inside the control band there is no alignment signal at all."""
import random, statistics
from align import PLAIN, CT, run

def best_nofill(ct, plain):
    best=0
    for off in range(0,len(plain)-20):
        g2l={}; l2g={}; n=0
        for i,g in enumerate(ct):
            j=off+i
            if j>=len(plain): break
            ch=plain[j]
            if g in g2l and g2l[g]!=ch: break
            if ch in l2g and l2g[ch]!=g: break
            g2l[g]=ch; l2g[ch]=g; n=i+1
        best=max(best,n)
    return best

real=best_nofill(CT,PLAIN)
random.seed(11)
sh=[]
for _ in range(300):
    c=CT[:]; random.shuffle(c); sh.append(best_nofill(c,PLAIN))
print(f'real cipher vs real plaintext, no nulls : {real} groups placed')
print(f'shuffled cipher control (n=300)         : mean {statistics.mean(sh):.1f}  '
      f'sd {statistics.pstdev(sh):.1f}  max {max(sh)}  p95 {sorted(sh)[284]}')
print()
print('Interpretation: a correct alignment would place all', len(CT), 'groups.')
print('The real run sits', 'INSIDE' if real<=sorted(sh)[284] else 'above', 'the control band ->',
      'no alignment signal.' if real<=sorted(sh)[284] else 'some signal.')
