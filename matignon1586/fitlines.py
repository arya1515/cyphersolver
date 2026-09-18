"""Fit line centres to a block: comb periodicity, then a DP that refines each line locally while
keeping the spacing plausible. Manuscript lines are not evenly spaced and a uniform grid drifts."""
import numpy as np, sys
from PIL import Image, ImageOps
src=sys.argv[1]; lo=float(sys.argv[2]); hi=float(sys.argv[3]); out=sys.argv[4]
im=ImageOps.autocontrast(Image.open(src).convert('L'),1)
a=np.array(im); ink=(a<150).sum(axis=1).astype(float)
prof=np.convolve(ink,np.ones(9)/9,'same')
best=None
for sp in np.arange(lo,hi,0.2):
    n=int(len(prof)/sp)
    for ph in np.arange(0,sp,1.0):
        ys=[ph+sp*i for i in range(n)]
        if ys[-1]>=len(prof): continue
        s=sum(prof[int(y)] for y in ys)/n
        if best is None or s>best[0]: best=(s,sp,ph,n)
s0,sp,ph,n=best
# DP: state = chosen y for line i, allowed within +-0.22*sp of the grid, spacing within +-0.25*sp
W=int(0.16*sp)
cands=[[int(ph+sp*i)+d for d in range(-W,W+1) if 0<=int(ph+sp*i)+d<len(prof)] for i in range(n)]
INF=-1e18
score=[[prof[y] for y in cands[0]]]
back=[[-1]*len(cands[0])]
for i in range(1,n):
    row=[];brow=[]
    for y in cands[i]:
        bestv=INF;bj=-1
        for j,yp in enumerate(cands[i-1]):
            d=y-yp
            if d < 0.90*sp or d > 1.12*sp: continue
            v=score[i-1][j]
            if v>bestv: bestv=v;bj=j
        row.append((bestv if bj>=0 else INF)+prof[y]); brow.append(bj)
    score.append(row); back.append(brow)
j=int(np.argmax(score[-1])); ys=[]
for i in range(n-1,-1,-1):
    ys.append(cands[i][j]); j=back[i][j]
    if j<0 and i>0: break
ys=list(reversed(ys))
print('sp',round(sp,1),'lines',len(ys))
print('diffs',[ys[i+1]-ys[i] for i in range(len(ys)-1)])
open(out,'w').write(','.join(map(str,ys)))
