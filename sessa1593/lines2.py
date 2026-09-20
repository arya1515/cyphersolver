"""Centred line strips for f.98: one line per strip, peak-centred."""
import numpy as np, os
from PIL import Image, ImageOps
im=Image.open('img3983/r0178_pct17_33_62_42_w3200.jpg').convert('L')
a=np.asarray(im,dtype=np.float32); ink=(a < a.mean()-0.5*a.std()); H,W=ink.shape
rows=ink.sum(1).astype(float)
sm=np.convolve(rows,np.ones(21)/21,mode='same'); mx=sm.max()
peaks=[]
for i in range(1,H-1):
    if sm[i]>=sm[i-1] and sm[i]>sm[i+1] and sm[i]>mx*0.20:
        if not peaks or i-peaks[-1]>=70: peaks.append(i)
        elif sm[i]>sm[peaks[-1]]: peaks[-1]=i
print('lines',len(peaks))
os.makedirs('C98',exist_ok=True)
for n,c in enumerate(peaks,1):
    lo=max(0,c-52); hi=min(H,c+52)
    ImageOps.autocontrast(im.crop((0,lo,W,hi)),cutoff=1).save(f'C98/C{n:02d}.png')
print('written')
