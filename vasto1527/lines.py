import sys,numpy as np
from PIL import Image
c=sys.argv[1]; y0,y1=int(sys.argv[2]),int(sys.argv[3]); x0,x1=int(sys.argv[4]),int(sys.argv[5]); nseg=int(sys.argv[6]) if len(sys.argv)>6 else 3
im=Image.open(f'hi/c{c}.jpg').convert('L'); w,h=im.size; s=w/1000
a=np.array(im.crop((int(x0*s),int(y0*s),int(x1*s),int(y1*s))),dtype=float)
ink=(a<110).sum(1)
k=int(12*s); sm=np.convolve(ink,np.ones(k)/k,'same')
# find peaks spaced >= 20 units
pk=[]
for i in range(len(sm)):
    lo=max(0,i-int(13*s)); hi=min(len(sm),i+int(13*s))
    if sm[i]==sm[lo:hi].max() and sm[i]>sm.max()*0.25: 
        if not pk or i-pk[-1]>int(15*s): pk.append(i)
ys=[y0+p/s for p in pk]
print(len(ys),[round(y) for y in ys])
xs=np.linspace(x0,x1,nseg+1)
for li,y in enumerate(ys):
    for j in range(nseg):
        a_,b_=xs[j]-15,xs[j+1]+15
        cr=im.crop((int(a_*s),int((y-24)*s),int(b_*s),int((y+22)*s)))
        cr.save(f'strips/{c}_L{li:02d}{"abcd"[j]}.jpg')
