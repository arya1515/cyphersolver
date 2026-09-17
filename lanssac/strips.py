"""Deskew a text block of a Gallica page image and cut one 100-px strip per line, in two overlapping halves.
usage: python strips.py <canvas> <x0> <y0> <x1> <y1> <prefix>   (coords in 885x1300 preview units)"""
import sys, numpy as np
from PIL import Image, ImageOps
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
n=int(sys.argv[1]); x0,y0,x1,y1=map(float,sys.argv[2:6]); pre=sys.argv[6]
im=Image.open(f'img/c{n:03d}.jpg'); w,h=im.size; sx=w/885; sy=h/1300
blk=ImageOps.autocontrast(im.crop((int(x0*sx),int(y0*sy),int(x1*sx),int(y1*sy))).convert('L'),cutoff=1)
best=None
for ang in np.arange(-3,3.01,0.125):
    r=blk.rotate(ang,resample=Image.BILINEAR,fillcolor=255)
    a=255-np.asarray(r).astype(float); v=gaussian_filter1d(a[:,200:-200].mean(1),2).var()
    if best is None or v>best[0]: best=(v,ang)
rot=blk.rotate(best[1],resample=Image.BICUBIC,fillcolor=255); rot.save(f'img/{pre}_deskew.png')
a=255-np.asarray(rot).astype(float); prof=gaussian_filter1d(a[:,200:-200].mean(1),3)
pk,_=find_peaks(prof,distance=int(sys.argv[7]) if len(sys.argv)>7 else 55,prominence=2)
print('angle',best[1],'lines',len(pk),list(map(int,pk)),list(map(int,np.diff(pk))))
W=rot.width
for i,c in enumerate(pk):
    for k,(xa,xb) in enumerate(((0,W//2+60),(W//2-60,W))):
        rot.crop((xa,max(0,c-52),xb,min(rot.height,c+48))).save(f'img/{pre}{i+1:02d}{"ab"[k]}.png')
