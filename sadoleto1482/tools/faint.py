import sys,numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
src,pre=sys.argv[1],sys.argv[2]; x0,x1,yf,pitch,nl,pc=map(int,sys.argv[3:9]); up=float(sys.argv[9]); hh=int(sys.argv[10])
a=np.asarray(Image.open(src).convert('RGB')).astype(float)
b=a[...,2]*0.7+a[...,1]*0.3
for l in range(nl):
    yc=yf+l*pitch
    reg=b[yc-hh:yc+hh,x0:x1]
    bg=ndi.uniform_filter(reg,61); d=ndi.gaussian_filter(bg-reg,1.2)
    d=np.clip((d-4)/ (np.percentile(d,99.5)-4+1e-6),0,1)
    img=Image.fromarray((255*(1-d)).astype(np.uint8))
    w=(x1-x0)/pc
    for k in range(pc):
        c=img.crop((int(max(0,k*w-40)),0,int(min(x1-x0,(k+1)*w+40)),2*hh))
        c.resize((int(c.size[0]*up),int(c.size[1]*up)),Image.LANCZOS).save(f'{pre}_L{l+1:02d}_{k}.png')
