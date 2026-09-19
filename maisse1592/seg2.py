"""f.370: line split with a fixed pitch prior, then group split, then digit split."""
import sys, os, json
import numpy as np
from PIL import Image

src='img/r419_pct49_23_50_40_w3500.jpg'
im=Image.open(src).convert('L')
a=np.asarray(im,dtype=np.float32)
ink=(a < a.mean()-0.45*a.std())
H,W=ink.shape
rows=ink.sum(1).astype(float)
ker=np.ones(19)/19.0
sm=np.convolve(rows,ker,mode='same')

# line centres: greedy peaks with an enforced minimum pitch
PITCH=int(os.environ.get('PITCH','95'))
order=np.argsort(-sm)
cent=[]
for i in order:
    if sm[i] < sm.max()*0.18: break
    if all(abs(i-c)>=PITCH*0.75 for c in cent): cent.append(int(i))
cent.sort()
print('line centres',len(cent))
bounds=[]
for j,c in enumerate(cent):
    lo = 0 if j==0 else int((cent[j-1]+c)/2)
    hi = H if j==len(cent)-1 else int((c+cent[j+1])/2)
    bounds.append((lo,hi))

GAP=int(os.environ.get('GAP','12'))
out=[]
for li,(y0,y1) in enumerate(bounds,1):
    band=ink[y0:y1]
    col=band.sum(0); on=col>0
    runs=[];s=None
    for x in range(W):
        if on[x] and s is None: s=x
        elif not on[x] and s is not None: runs.append([s,x]); s=None
    if s is not None: runs.append([s,W])
    merged=[]
    for r in runs:
        if merged and r[0]-merged[-1][1]<GAP: merged[-1][1]=r[1]
        else: merged.append(r)
    merged=[r for r in merged if (r[1]-r[0])>=7 and band[:,r[0]:r[1]].sum()>=20]
    out.append({'line':li,'y0':y0,'y1':y1,'groups':merged})
    print(f'  line {li:2d} y{y0:4d}-{y1:4d} h{y1-y0:3d}: {len(merged):2d} groups')
json.dump(out,open('seg370.json','w'))
tot=sum(len(o['groups']) for o in out)
ws=[r[1]-r[0] for o in out for r in o['groups']]
print('total groups',tot,'median width',int(np.median(ws)),'p10',int(np.percentile(ws,10)),'p90',int(np.percentile(ws,90)))
