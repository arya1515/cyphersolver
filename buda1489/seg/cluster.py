"""Cluster segmented glyphs by shape. usage: python seg/cluster.py <thresh> <outprefix> <glyphs.json>..."""
import sys,json,os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.cluster.hierarchy import linkage,fcluster
from scipy.spatial.distance import squareform
Image.MAX_IMAGE_PIXELS=None
thresh=float(sys.argv[1]); out=sys.argv[2]; files=sys.argv[3:]
S=36
items=[]; feats=[]
cache={}
for f in files:
    J=json.load(open(f)); src=J['src']; ox,oy=J['offset']
    if src not in cache:
        im=Image.open(src).convert('L'); cache[src]=np.asarray(im).astype(float)
    g=cache[src]
    tag=os.path.basename(f).replace('_glyphs.json','')
    for li,L in enumerate(J['lines']):
        if len(L)<4: continue
        for gi,b in enumerate(L):
            x0,y0,x1,y1=b[0]+ox,b[1]+oy,b[2]+ox,b[3]+oy
            pad=3
            crop=g[max(0,y0-pad):y1+pad,max(0,x0-pad):x1+pad]
            bg=np.percentile(crop,90)
            ink=np.clip((bg-crop)/max(1,bg-crop.min()),0,1)
            h,w=ink.shape; s=(S-4)/max(h,w)
            r=np.asarray(Image.fromarray((ink*255).astype(np.uint8)).resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS)).astype(float)/255
            canvas=np.zeros((S,S)); yy=(S-r.shape[0])//2; xx=(S-r.shape[1])//2
            canvas[yy:yy+r.shape[0],xx:xx+r.shape[1]]=r
            canvas=ndi.gaussian_filter(canvas,1.0)
            v=canvas.flatten(); v=v-v.mean(); v/= (np.linalg.norm(v)+1e-9)
            # aspect + size features appended (weighted) so tall vs short glyphs separate
            asp=np.array([ (h/(w+1e-9))*0.5, (h/60.0)*1.0 ])
            feats.append(np.concatenate([v,asp]))
            items.append((tag,li,gi,x0,y0,x1,y1,src))
X=np.array(feats)
n=len(X); print('glyphs',n)
Z=linkage(X,method='average',metric='euclidean')
cl=fcluster(Z,t=thresh,criterion='distance')
ids,counts=np.unique(cl,return_counts=True)
order=np.argsort(-counts)
print('clusters',len(ids)); print('sizes',counts[order][:60].tolist())
# save assignment
json.dump({'items':items,'cluster':cl.tolist()},open(out+'_clusters.json','w'))
# montage: each cluster a row of up to 24 samples at 40px
rows=[]
for k in order:
    cid=ids[k]; idx=np.where(cl==cid)[0][:24]
    rows.append((int(cid),int(counts[k]),idx))
CH=44; CW=44; per=24
H=len(rows)*CH; W=90+per*CW
mont=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(mont)
for r,(cid,cnt,idx) in enumerate(rows):
    d.text((2,r*CH+14),f'{cid}:{cnt}',fill=(200,0,0))
    for j,i in enumerate(idx):
        tag,li,gi,x0,y0,x1,y1,src=items[i]
        crop=Image.fromarray(cache[src][y0-3:y1+3,x0-3:x1+3].astype(np.uint8))
        h,w=crop.size[1],crop.size[0]; s=min(40/h,40/w); crop=crop.resize((max(1,int(w*s)),max(1,int(h*s))))
        mont.paste(crop,(90+j*CW+(40-crop.size[0])//2,r*CH+2+(40-crop.size[1])//2))
mont.save(out+'_montage.png'); print('montage',mont.size)
