"""kNN glyph classifier. python seg/knn.py <train: glyphs.json,aligned.json>[,...] <test glyphs.json> <out.json>"""
import sys,json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
Image.MAX_IMAGE_PIXELS=None
S=36; cache={}
def feat(src,b):
    if src not in cache: cache[src]=np.asarray(Image.open(src).convert('L')).astype(float)
    g=cache[src]; x0,y0,x1,y1=b; pad=3
    crop=g[max(0,y0-pad):y1+pad,max(0,x0-pad):x1+pad]
    bg=np.percentile(crop,90); ink=np.clip((bg-crop)/max(1,bg-crop.min()),0,1)
    h,w=ink.shape; s=(S-4)/max(h,w)
    r=np.asarray(Image.fromarray((ink*255).astype(np.uint8)).resize((max(1,int(w*s)),max(1,int(h*s))),Image.LANCZOS)).astype(float)/255
    c=np.zeros((S,S)); yy=(S-r.shape[0])//2; xx=(S-r.shape[1])//2; c[yy:yy+r.shape[0],xx:xx+r.shape[1]]=r
    c=ndi.gaussian_filter(c,1.0); v=c.flatten(); v=v-v.mean(); v/=(np.linalg.norm(v)+1e-9)
    return np.concatenate([v,[0.6*h/(w+1e-9),1.2*h/60.0]])
X=[];Y=[];T=[]
for spec in sys.argv[1].split(';'):
    gj,aj=spec.split(',')
    G=json.load(open(gj)); ox,oy=G['offset']
    for ln,idx,tok,val in json.load(open(aj)):
        if not idx.isdigit(): continue
        L=G['lines'][ln-1]; i=int(idx)
        if i>=len(L): continue
        b=L[i]; X.append(feat(G['src'],(b[0]+ox,b[1]+oy,b[2]+ox,b[3]+oy))); Y.append(val); T.append(tok)
X=np.array(X); print('train',len(X))
G=json.load(open(sys.argv[2])); ox,oy=G['offset']; res=[]
for li,L in enumerate(G['lines']):
    row=[]
    for gi,b in enumerate(L):
        f=feat(G['src'],(b[0]+ox,b[1]+oy,b[2]+ox,b[3]+oy))
        d=np.linalg.norm(X-f,axis=1); o=np.argsort(d)[:5]
        votes={}
        for k in o: votes[Y[k]]=votes.get(Y[k],0)+1/(d[k]+0.05)
        best=max(votes,key=votes.get); conf=votes[best]/sum(votes.values())
        row.append({'idx':gi,'val':best,'conf':round(float(conf),2),'d':round(float(d[o[0]]),3),'tok':T[o[0]]})
    res.append(row)
json.dump(res,open(sys.argv[3],'w'))
for li,row in enumerate(res):
    print(f'L{li+1:02d}: '+''.join((r['val'] if r['conf']>0.6 and r['d']<0.9 else '['+r['val']+']') for r in row))
