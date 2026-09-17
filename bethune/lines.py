"""Detect text lines on a page image by ink projection and cut each into overlapping half-line crops.
usage: python lines.py full/c075.jpg f34 [x0frac x1frac] -> writes f34_L01a.jpg ... and prints line centres."""
import sys, numpy as np
from PIL import Image, ImageFilter
src, prefix = sys.argv[1], sys.argv[2]
x0f = float(sys.argv[3]) if len(sys.argv)>3 else 0.22
x1f = float(sys.argv[4]) if len(sys.argv)>4 else 0.96
im = Image.open(src).convert('L'); W,H = im.size
x0,x1 = int(W*x0f), int(W*x1f)
a = np.asarray(im.crop((x0,0,x1,H)), dtype=np.float32)
ink = (a < 140).mean(axis=1)                      # fraction of dark pixels per row
k = 9; sm = np.convolve(ink, np.ones(k)/k, mode='same')
thr = 0.012
rows = sm > thr
# segments of consecutive text rows
segs=[]; i=0
while i<H:
    if rows[i]:
        j=i
        while j<H and rows[j]: j+=1
        if j-i > 25: segs.append((i,j))
        i=j
    else: i+=1
# merge segments closer than 18 px (ascenders/descenders)
merged=[]
for s in segs:
    if merged and s[0]-merged[-1][1] < 18: merged[-1]=(merged[-1][0], s[1])
    else: merged.append(s)
# typical line height
hs=[b-a for a,b in merged]; med=np.median(hs) if hs else 60
out=[]
for a_,b_ in merged:
    if b_-a_ > 1.7*med:   # split tall blocks
        n=int(round((b_-a_)/med))
        for q in range(n): out.append((a_+q*(b_-a_)/n, a_+(q+1)*(b_-a_)/n))
    else: out.append((a_,b_))
pad=int(0.35*med)
imc=Image.open(src)
for n,(a_,b_) in enumerate(out,1):
    y0=max(0,int(a_-pad)); y1=min(H,int(b_+pad))
    xm=(x0+x1)//2; ov=int(0.02*W)
    for k_,(l,r) in enumerate([(x0-ov,xm+ov),(xm-ov,x1+ov)]):
        s=imc.crop((max(0,l),y0,min(W,r),y1)); s=s.resize((int(s.width*1.5),int(s.height*1.5)),Image.LANCZOS)
        s.save(f'bethune/{prefix}_L{n:02d}{"ab"[k_]}.jpg',quality=92)
print(prefix, len(out), 'lines; centres:', [int((a_+b_)/2) for a_,b_ in out])
