# lines.py canvas qx0 qx1 [qy0 qy1] -> line centre y (preview units) by ink projection
import sys, numpy as np
from PIL import Image
c=sys.argv[1]; x0,x1=float(sys.argv[2]),float(sys.argv[3])
qy0=float(sys.argv[4]) if len(sys.argv)>4 else 0; qy1=float(sys.argv[5]) if len(sys.argv)>5 else 1e9
im=Image.open(f'full16127/c{c}.jpg').convert('L'); s=im.width/1240
a=np.asarray(im.resize((1240,int(im.height/s))),dtype=float)
ink=(a<110)[:,int(x0):int(x1)].sum(1).astype(float)
k=np.ones(9)/9; sm=np.convolve(ink,k,'same')
pk=[y for y in range(10,len(sm)-10) if qy0<=y<=qy1 and sm[y]==sm[y-9:y+10].max() and sm[y]>0.12*np.percentile(sm,99)]
out=[]
for y in pk:
    if out and y-out[-1]<20: 
        if sm[y]>sm[out[-1]]: out[-1]=y
        continue
    out.append(y)
print(len(out)); print(' '.join(map(str,out)))
