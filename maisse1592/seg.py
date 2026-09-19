"""Segment a cipher block into line strips and then into groups by horizontal ink gaps."""
import sys, os, json
from PIL import Image
import numpy as np

src=sys.argv[1]; out=sys.argv[2]
im=Image.open(src).convert('L')
a=np.asarray(im,dtype=np.float32)
# local threshold: ink is well below the page mean
thr=a.mean()-0.45*a.std()
ink=(a<thr)
H,W=ink.shape
rows=ink.sum(1).astype(float)
# smooth
k=9; ker=np.ones(2*k+1)/(2*k+1)
sm=np.convolve(rows,ker,mode='same')
mx=sm.max()
peaks=[]
for i in range(1,H-1):
    if sm[i]>=sm[i-1] and sm[i]>sm[i+1] and sm[i]>mx*0.22:
        if not peaks or i-peaks[-1]>=40: peaks.append(i)
        elif sm[i]>sm[peaks[-1]]: peaks[-1]=i
cuts=[0]+[int((a_+b_)/2) if False else int(np.argmin(sm[a_:b_])+a_) for a_,b_ in zip(peaks,peaks[1:])]+[H]
lines=[(cuts[i],cuts[i+1]) for i in range(len(cuts)-1) if cuts[i+1]-cuts[i]>25]
print('lines',len(lines))
res=[]
for li,(y0,y1) in enumerate(lines,1):
    band=ink[y0:y1]
    col=band.sum(0)
    on=col>0
    # merge gaps shorter than GAP
    GAP=int(os.environ.get('GAP','11'))
    runs=[];s=None
    for x in range(W):
        if on[x] and s is None: s=x
        elif not on[x] and s is not None:
            runs.append([s,x]); s=None
    if s is not None: runs.append([s,W])
    merged=[]
    for r in runs:
        if merged and r[0]-merged[-1][1]<GAP: merged[-1][1]=r[1]
        else: merged.append(r)
    merged=[r for r in merged if r[1]-r[0]>=6 and band[:,r[0]:r[1]].sum()>=18]
    res.append({'line':li,'y0':int(y0),'y1':int(y1),'groups':[[int(x0),int(x1)] for x0,x1 in merged]})
    print(f'  line {li:2d} y{y0}-{y1}: {len(merged)} groups')
json.dump(res,open(out,'w'))
print('total groups',sum(len(r['groups']) for r in res))
