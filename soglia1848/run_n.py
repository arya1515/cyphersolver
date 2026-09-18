import sys
from drive import *
tag=sys.argv[1]; cand=sys.argv[2]
it,R,T0,T1,lam,n=sys.argv[3:9]
run_nsa(tag,cand,it,R,T0,T1,lam,int(n))
C=[l.strip() for l in open(cand) if l.strip()]
Rs=results(f'runs/{tag}_*.out')
for sc,m in Rs[:5]:
    print(f'{sc:.1f}',show_n(m,C)[:300])
sc,m=Rs[0]
print({t:C[m[i]] for i,t in enumerate(types)})
