"""Find the skew angle that maximises row-profile contrast, rotate, re-strip."""
import numpy as np, os, sys
from PIL import Image, ImageOps
src=sys.argv[1]; outdir=sys.argv[2]
im=Image.open(src).convert('L')
a0=np.asarray(im,dtype=np.float32)
thr=a0.mean()-0.5*a0.std()
best=(None,-1)
for ang in np.arange(-3.0,3.01,0.25):
    r=im.rotate(ang,resample=Image.BILINEAR,fillcolor=255)
    a=np.asarray(r,dtype=np.float32)
    rows=(a<thr).sum(1).astype(float)
    score=float(np.var(rows))
    if score>best[1]: best=(ang,score)
ang=best[0]; print('skew angle',ang)
r=im.rotate(ang,resample=Image.BILINEAR,fillcolor=255)
a=np.asarray(r,dtype=np.float32); ink=(a<thr); H,W=ink.shape
rows=ink.sum(1).astype(float)
sm=np.convolve(rows,np.ones(15)/15,mode='same'); mx=sm.max()
peaks=[]
for i in range(1,H-1):
    if sm[i]>=sm[i-1] and sm[i]>sm[i+1] and sm[i]>mx*0.20:
        if not peaks or i-peaks[-1]>=70: peaks.append(i)
        elif sm[i]>sm[peaks[-1]]: peaks[-1]=i
print('lines',len(peaks))
os.makedirs(outdir,exist_ok=True)
for n,c in enumerate(peaks,1):
    lo=max(0,c-58); hi=min(H,c+58)
    ImageOps.autocontrast(r.crop((0,lo,W,hi)),cutoff=1).save(f'{outdir}/D{n:02d}.png')
print('written',len(peaks))
