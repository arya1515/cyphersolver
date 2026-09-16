import numpy as np,collections,re
import qg, ng5
from solve2 import load_ct,anneal,AL
tab=qg.load(); tab5=ng5.load()
ct0=load_ct('elizabeth_moray.txt')
def fam(s): return re.sub(r'[0-9b]+$','',s) if s not in ('10','11','12','13','14','15','16','17','18','19','4') else s
def transform(ct,drop=(),merge=()):
    out=[]
    for s in ct:
        f=fam(s)
        if f in drop: continue
        out.append(f if f in merge else s)
    return out
def best(ct,restarts=8):
    syms=sorted(set(ct)); si={s:i for i,s in enumerate(syms)}; ctidx=np.array([si[s] for s in ct])
    b=max((anneal(ctidx,len(syms),iters=120000,seed=r) for r in range(restarts)),key=lambda t:t[0])
    dec=''.join(AL[x] for x in b[1][ctidx])
    p=np.frombuffer(dec.encode(),dtype=np.uint8).astype(np.int64)-97
    return b[0]/(len(ct)-3), ng5.score(tab5,p)/(len(ct)-4), len(syms), dec
for name,drop,merge in [('base',(),()),('merge x',(),('x',)),('merge z',(),('z',)),('merge x,z,o,4',(),('x','z','o','4')),
                        ('drop z',('z',),()),('drop x',('x',),()),('drop z merge x',('z',),('x',)),('drop x merge z',('x',),('z',)),
                        ('drop z merge x,o,4',('z',),('x','o','4'))]:
    ct=transform(ct0,drop,merge)
    q4,q5,ns,dec=best(ct)
    print(f'{name:22s} n={len(ct)} syms={ns} q4/char={q4:.3f} q5/char={q5:.3f} {dec}',flush=True)
