"""Cut a block into line strips: smooth the ink profile, take peaks as line centres, cut at minima."""
import sys, os
from PIL import Image
src=sys.argv[1]; outdir=sys.argv[2]
im=Image.open(src).convert('L'); W,H=im.size; px=im.load()
os.makedirs(outdir,exist_ok=True)
prof=[sum(1 for x in range(0,W,3) if px[x,y]<150) for y in range(H)]
def smooth(p,k):
    out=[]
    for i in range(len(p)):
        a=max(0,i-k); b=min(len(p),i+k+1)
        out.append(sum(p[a:b])/(b-a))
    return out
s=smooth(prof,9)
mx=max(s)
# peaks: local maxima above 25% of max, separated by >=30px
peaks=[]
for i in range(1,len(s)-1):
    if s[i]>=s[i-1] and s[i]>s[i+1] and s[i]>mx*0.25:
        if not peaks or i-peaks[-1]>=30: peaks.append(i)
        elif s[i]>s[peaks[-1]]: peaks[-1]=i
print('peaks',len(peaks))
cuts=[0]
for a,b in zip(peaks,peaks[1:]):
    lo=min(range(a,b),key=lambda y:s[y]); cuts.append(lo)
cuts.append(H)
n=0
for a,b in zip(cuts,cuts[1:]):
    if b-a<18: continue
    n+=1
    pad=6
    im.crop((0,max(0,a-pad),W,min(H,b+pad))).save(f'{outdir}/L{n:02d}.png')
print('strips',n)
