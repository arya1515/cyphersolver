# Segment glyphs in line images: connected components, merged by horizontal overlap. segglyphs.py prefix nlines thr
import sys, json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
pre=sys.argv[1]; n=int(sys.argv[2]); thr=int(sys.argv[3]) if len(sys.argv)>3 else 160
out={}
for k in range(1,n+1):
    im=Image.open(f'{pre}_l{k:02d}.png'); a=np.asarray(im)
    ink=a<thr
    # remove ruling noise: components with area<12
    lab,nl=ndimage.label(ink, structure=np.ones((3,3)))
    objs=ndimage.find_objects(lab)
    boxes=[]
    for i,sl in enumerate(objs):
        if sl is None: continue
        area=(lab[sl]==i+1).sum()
        y0,y1=sl[0].start,sl[0].stop; x0,x1=sl[1].start,sl[1].stop
        if area<14: continue
        if (y1-y0)>0.95*a.shape[0] and (x1-x0)>200: continue  # long rule
        boxes.append([x0,y0,x1,y1,int(area)])
    boxes.sort()
    # merge boxes overlapping in x by > 40% of the smaller width, or tiny boxes within a glyph span
    merged=[]
    for b in boxes:
        if merged:
            m=merged[-1]
            ov=min(m[2],b[2])-max(m[0],b[0]); wmin=min(m[2]-m[0],b[2]-b[0])
            if ov>0.4*wmin or (ov>-3 and (b[4]<60 or m[4]<60)):
                m[0]=min(m[0],b[0]); m[1]=min(m[1],b[1]); m[2]=max(m[2],b[2]); m[3]=max(m[3],b[3]); m[4]+=b[4]; continue
        merged.append(list(b))
    merged=[m for m in merged if m[4]>=30]
    # split over-wide boxes at thin columns
    widths=sorted(m[2]-m[0] for m in merged); med=widths[len(widths)//2] if widths else 30
    split=[]
    for m in merged:
        x0,y0,x1,y1,area=m
        if x1-x0<=1.6*med: split.append(m); continue
        col=ink[y0:y1,x0:x1].sum(0)
        cuts=[]; start=0
        # candidate cut columns: minimal ink, at least 0.6*med from last cut
        i=int(0.6*med)
        while i<len(col)-int(0.6*med):
            if col[i]<=2:
                j=i
                while j<len(col) and col[j]<=2: j+=1
                cuts.append((i+j)//2); i=j+int(0.6*med)
            else: i+=1
        if not cuts:
            # fall back: cut at the lowest columns spaced by med
            n=int(round((x1-x0)/med))
            for q in range(1,n):
                lo=int(q*med-0.3*med); hi=int(q*med+0.3*med)
                seg=col[lo:hi]; cuts.append(lo+int(seg.argmin()))
        prev=0
        for c in cuts+[x1-x0]:
            sub=ink[y0:y1,x0+prev:x0+c]
            if sub.sum()>=30:
                ys=np.where(sub.any(1))[0]; xs=np.where(sub.any(0))[0]
                split.append([x0+prev+int(xs[0]),y0+int(ys[0]),x0+prev+int(xs[-1])+1,y0+int(ys[-1])+1,int(sub.sum())])
            prev=c
    merged=split
    out[k]=merged
    d=im.convert('RGB'); dr=ImageDraw.Draw(d)
    for m in merged: dr.rectangle(m[:4],outline=(255,0,0))
    d.save(f'{pre}_l{k:02d}_box.png')
json.dump(out,open(f'{pre}_glyphs.json','w'))
print({k:len(v) for k,v in out.items()})
