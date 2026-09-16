import numpy as np,collections
import qg
from solve2 import load_ct,anneal,AL
tab=qg.load()
ct=load_ct('elizabeth_moray.txt')
def best(ct,restarts=6):
    syms=sorted(set(ct)); si={s:i for i,s in enumerate(syms)}; ctidx=np.array([si[s] for s in ct])
    b=max((anneal(ctidx,len(syms),iters=100000,seed=r) for r in range(restarts)),key=lambda t:t[0])
    return b[0]/(len(ct)-3),''.join(AL[x] for x in b[1][ctidx])
base=best(ct); print('base',round(base[0],3),base[1],flush=True)
for s,cnt in collections.Counter(ct).most_common():
    if cnt<3: break
    ct2=[x for x in ct if x!=s]
    r=best(ct2); print(s,cnt,round(r[0],3),r[1],flush=True)
