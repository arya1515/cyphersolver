import sys,os,numpy as np
from PIL import Image, ImageOps
from scipy.ndimage import gaussian_filter1d
# lines.py src prefix x0 x1 y0 y1 (full-res px) ; writes prefix_LNN_a/b.png (two halves, upscaled)
src,pre=sys.argv[1],sys.argv[2]; x0,x1,y0,y1=map(int,sys.argv[3:7])
im=Image.open(src).convert('L'); a=np.asarray(im,dtype=float)
reg=a[y0:y1,x0:x1]; bg=np.percentile(reg,90); ink=np.clip(bg-reg-25,0,None)
prof=gaussian_filter1d(ink.sum(1),12)
from scipy.signal import find_peaks
pk,_=find_peaks(prof,distance=int(sys.argv[7]) if len(sys.argv)>7 else 90,prominence=prof.max()*0.08)
print('peaks',[p+y0 for p in pk])
for i,p in enumerate(pk):
    yc=p+y0; top=yc-55; bot=yc+45
    c=ImageOps.autocontrast(im.crop((x0,top,x1,bot)),cutoff=1)
    w=c.size[0]; 
    for h,(l,r) in enumerate([(0,w//2+80),(w//2-80,w)]):
        cc=c.crop((l,0,r,c.size[1])); cc=cc.resize((int(cc.size[0]*1.6),int(cc.size[1]*1.6)),Image.LANCZOS)
        cc.save(f'{pre}_L{i+1:02d}{"ab"[h]}.png')
