"""Split the f.98 cipher block into line strips by ink profile."""
import numpy as np, os
from PIL import Image, ImageOps
src='img3983/r0178_pct17_33_62_42_w3200.jpg'
im=Image.open(src).convert('L')
a=np.asarray(im,dtype=np.float32)
ink=(a < a.mean()-0.5*a.std())
H,W=ink.shape
rows=ink.sum(1).astype(float)
k=13; sm=np.convolve(rows,np.ones(2*k+1)/(2*k+1),mode='same')
mx=sm.max()
peaks=[]
for i in range(1,H-1):
    if sm[i]>=sm[i-1] and sm[i]>sm[i+1] and sm[i]>mx*0.20:
        if not peaks or i-peaks[-1]>=70: peaks.append(i)
        elif sm[i]>sm[peaks[-1]]: peaks[-1]=i
print('lines',len(peaks))
os.makedirs('L98',exist_ok=True)
bounds=[]
for j,c in enumerate(peaks):
    lo=0 if j==0 else int((peaks[j-1]+c)/2)
    hi=H if j==len(peaks)-1 else int((c+peaks[j+1])/2)
    bounds.append((lo,hi))
for n,(lo,hi) in enumerate(bounds,1):
    c=im.crop((0,max(0,lo-6),W,min(H,hi+6)))
    c=ImageOps.autocontrast(c,cutoff=1)
    c.save(f'L98/L{n:02d}.png')
print('strips written', len(bounds))
