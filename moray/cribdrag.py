import sys,json,numpy as np
import ng5 as qg
from solve3 import load_ct,anneal,AL
tab=qg.load()
ct=load_ct('elizabeth_moray.txt'); syms=sorted(set(ct)); si={s:i for i,s in enumerate(syms)}
ctidx=np.array([si[s] for s in ct])
cribs=sys.argv[1].split(',')
def consistent(word,i):
    m={}
    for k,ch in enumerate(word):
        s=ct[i+k]
        if s in m and m[s]!=ch: return None
        m[s]=ch
    # distinct letters must have distinct symbols: already implied (same symbol->one letter)
    return m
out=[]
for w in cribs:
    for i in range(len(ct)-len(w)+1):
        m=consistent(w,i)
        if m is None: continue
        fx={si[s]:AL.index(l) for s,l in m.items()}
        best=None
        for r in range(4):
            b,k=anneal(ctidx,len(syms),iters=80000,seed=r,fixed=fx)
            if best is None or b>best[0]: best=(b,k)
        dec=''.join(AL[x] for x in best[1][ctidx])
        out.append((best[0],w,i,dec))
        print(f'{best[0]:.1f} {w} @{i} {dec}',flush=True)
out.sort(key=lambda x:-x[0])
print('TOP'); [print(f'{b:.1f} {w} @{i} {d}') for b,w,i,d in out[:25]]
