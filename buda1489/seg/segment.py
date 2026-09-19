"""Connected-component glyph segmentation for the Buda cipher pages.
usage: python seg/segment.py <image> <x0> <y0> <x1> <y1> <outprefix>
Writes <outprefix>_glyphs.json (boxes in reading order, per line) and <outprefix>_lines.png overview."""
import sys,json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
Image.MAX_IMAGE_PIXELS=None
src,x0,y0,x1,y1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
im=Image.open(src).convert('RGB').crop((x0,y0,x1,y1))
a=np.asarray(im).astype(float)
# ink = darker & browner than paper: use min channel vs local background
g=a.mean(axis=2)
bg=ndi.uniform_filter(g,151)
ink=(bg-g)>float(sys.argv[7]) if len(sys.argv)>7 else (bg-g)>28
ink=ndi.binary_opening(ink,iterations=1)
lab,n=ndi.label(ink)
objs=ndi.find_objects(lab)
boxes=[]
for i,sl in enumerate(objs):
    h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
    area=(lab[sl]==i+1).sum()
    if area<25 or (h<6 and w<6): continue
    boxes.append([sl[1].start,sl[0].start,sl[1].stop,sl[0].stop,int(area)])
# line centres = peaks of the smoothed horizontal ink projection, period from autocorrelation
from scipy.signal import find_peaks
prof=ink.sum(axis=1).astype(float)
p=ndi.gaussian_filter1d(prof,4)
pc=p-p.mean(); ac=np.correlate(pc,pc,'full')[len(pc)-1:]
lo=15; period=lo+int(np.argmax(ac[lo:min(len(ac),400)]))
peaks,_=find_peaks(p,distance=int(period*0.6),prominence=p.max()*0.08)
centres=list(peaks)
lines=[[] for _ in centres]
for i,b in enumerate(boxes):
    yc=(b[1]+b[3])/2
    k=int(np.argmin([abs(yc-c) for c in centres]))
    lines[k].append(i)
lines=[L for L in lines if L]
print('period',period,'lines',len(centres))
# merge components that overlap horizontally within a line (diacritics + base)
glyph_lines=[]
for L in lines:
    bs=sorted([boxes[i] for i in L],key=lambda b:b[0])
    merged=[]
    for b in bs:
        if merged:
            m=merged[-1]
            ov=min(m[2],b[2])-max(m[0],b[0])
            if ov> 0.4*min(m[2]-m[0],b[2]-b[0]):
                merged[-1]=[min(m[0],b[0]),min(m[1],b[1]),max(m[2],b[2]),max(m[3],b[3]),m[4]+b[4]]; continue
        merged.append(list(b))
    # second pass: attach small diacritics (superscript letters, bars, dots) sitting above/right of a base glyph,
    # and merge pairs of thin slashes into one sign
    lineh=np.median([b[3]-b[1] for b in merged]) if merged else 20
    out2=[]
    for b in merged:
        if out2:
            m=out2[-1]
            bw,bh=b[2]-b[0],b[3]-b[1]; mw,mh=m[2]-m[0],m[3]-m[1]
            gap=b[0]-m[2]
            small = b[4]<0.35*np.median([x[4] for x in merged]) and bh<0.7*lineh
            medarea=np.median([x[4] for x in merged])
            slashlike = lambda q:(q[3]-q[1])>=1.05*(q[2]-q[0]) and (q[2]-q[0])<0.8*lineh and q[4]<0.6*medarea and (q[3]-q[1])<1.1*lineh
            if slashlike(b) and slashlike(m) and gap<0.3*lineh and abs(b[1]-m[1])<0.4*lineh and not m[5:]:
                out2[-1]=[min(m[0],b[0]),min(m[1],b[1]),max(m[2],b[2]),max(m[3],b[3]),m[4]+b[4],'ss']; continue
            if small and gap<0.25*lineh and b[1]<m[1]+0.3*mh:
                out2[-1]=[min(m[0],b[0]),min(m[1],b[1]),max(m[2],b[2]),max(m[3],b[3]),m[4]+b[4]]; continue
        out2.append(b)
    glyph_lines.append(out2)
# fold tiny 'lines' (descenders etc.) into neighbours
final=[]
for L in glyph_lines:
    if len(L)<4 and final: final[-1]=sorted(final[-1]+L,key=lambda b:b[0])
    else: final.append(L)
glyph_lines=final
json.dump({'src':src,'offset':[x0,y0],'lines':glyph_lines},open(out+'_glyphs.json','w'))
d=ImageDraw.Draw(im)
for li,L in enumerate(glyph_lines):
    for b in L: d.rectangle(b[:4],outline=(255,0,0) if li%2 else (0,0,255))
im.save(out+'_lines.png')
print('lines',len(glyph_lines),'glyphs per line',[len(L) for L in glyph_lines])
