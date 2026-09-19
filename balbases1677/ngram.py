import sys,collections,glob
sys.stdout.reconfigure(encoding='utf-8')
from align2 import read_tx,ctok,cplain
D={}
for f in sorted(glob.glob('tx/R*.txt')):
    t,p=read_tx(f);t=[ctok(x) for x in t];s=cplain(p)
    if len(t)>20 and len(s)>40: D[f[3:-4]]=(t,s)
C=collections.defaultdict(list)
for r,(t,s) in D.items():
    for n in (3,4,5):
        for i in range(len(t)-n+1): C[(n,' '.join(t[i:i+n]))].append((r,i))
out=[]
for (n,g),occ in C.items():
    if len(occ)>=2 and len({r for r,i in occ})>=2 and n>=3:
        out.append((n*len(occ),g,occ))
for sc,g,occ in sorted(out,reverse=True)[:60]:
    print('==',g)
    for r,i in occ:
        t,s=D[r];j=int(i/len(t)*len(s)); print('  ',r,i,s[max(0,j-35):j+35])
