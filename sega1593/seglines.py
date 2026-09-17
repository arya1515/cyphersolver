# Segment a cipher page into text lines: deskew, ink profile, separators at profile minima spaced by the line pitch.
# usage: seglines.py img x0 y0 x1 y1 out_prefix [thr]
import sys, numpy as np
from PIL import Image, ImageDraw
f=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); pre=sys.argv[6]; thr=int(sys.argv[7]) if len(sys.argv)>7 else 160
im=Image.open(f).convert('L').crop((x0,y0,x1,y1))
def profile(img):
    a=np.asarray(img); ink=(a<thr).astype(float); return ink.sum(1)
best=None
for ang in np.arange(-2.0,2.01,0.25):
    r=im.rotate(ang,resample=Image.BILINEAR,fillcolor=255)
    p=profile(r); v=p.var()
    if best is None or v>best[0]: best=(v,ang,r,p)
v,ang,rot,prof=best
sm=np.convolve(prof,np.ones(9)/9,mode='same')
# pitch by autocorrelation
z=sm-sm.mean(); ac=np.correlate(z,z,mode='full')[len(z)-1:]
lo,hi=40,200; pitch=lo+int(np.argmax(ac[lo:hi]))
print('skew',ang,'pitch',pitch)
# separators: minima of sm within windows
seps=[]; i=0
thresh=0.35*np.percentile(sm,90)
# find runs of low profile
low=sm<thresh
runs=[];i=0
while i<len(low):
    if low[i]:
        j=i
        while j<len(low) and low[j]: j+=1
        runs.append((i,j)); i=j
    else: i+=1
cuts=[ (a+b)//2 for a,b in runs if b-a>=4]
# merge cuts closer than 0.5 pitch
m=[]
for c in cuts:
    if m and c-m[-1]<0.5*pitch: m[-1]=(m[-1]+c)//2
    else: m.append(c)
lines=[(m[k],m[k+1]) for k in range(len(m)-1) if m[k+1]-m[k]>0.5*pitch]
print(len(lines),'lines')
d=rot.convert('RGB'); dr=ImageDraw.Draw(d)
for c in m: dr.line((0,c,rot.width,c),fill=(255,0,0),width=3)
d.resize((d.width//4,d.height//4)).save(pre+'_lines.png')
rot.save(pre+'_rot.png')
with open(pre+'_lines.txt','w') as fo:
    for k,(a,b) in enumerate(lines):
        fo.write(f'{k+1} {a} {b}\n')
        rot.crop((0,a,rot.width,b)).save(f'{pre}_l{k+1:02d}.png')
