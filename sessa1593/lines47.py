import numpy as np, os
from PIL import Image, ImageOps
src='img3984/r0198_pct9_6_44_24_w3600.jpg'
im=Image.open(src).convert('L'); a=np.asarray(im,dtype=np.float32)
ink=(a < a.mean()-0.55*a.std()); H,W=ink.shape
rows=ink.sum(1).astype(float)
sm=np.convolve(rows,np.ones(11)/11,mode='same'); mx=sm.max()
peaks=[]
for i in range(1,H-1):
    if sm[i]>=sm[i-1] and sm[i]>sm[i+1] and sm[i]>mx*0.16:
        if not peaks or i-peaks[-1]>=26: peaks.append(i)
        elif sm[i]>sm[peaks[-1]]: peaks[-1]=i
print('bands',len(peaks),'image',im.size)
os.makedirs('L108',exist_ok=True)
for j,c in enumerate(peaks,1):
    lo=max(0,c-38); hi=min(H,c+38)
    ImageOps.autocontrast(im.crop((0,lo,W,hi)),cutoff=1).save(f'L108/B{j:02d}.png')
