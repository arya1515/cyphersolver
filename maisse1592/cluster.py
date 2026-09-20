"""Cluster the connected components of f.370 by shape, then show representatives to label."""
import json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.cluster.vq import kmeans2

SRC='img/r419_pct49_23_50_40_w3500.jpg'
A=np.asarray(Image.open(SRC).convert('L'),dtype=np.float32)
INK=(A < A.mean()-0.42*A.std()).astype(np.float32)
comps=json.load(open('comps.json'))

S=24
def raster(c):
    sub=INK[c['y']:c['y1'], c['x']:c['x1']]
    h,w=sub.shape
    sc=float(S)/max(h,w)
    nh,nw=max(2,int(round(h*sc))),max(2,int(round(w*sc)))
    im=Image.fromarray((sub*255).astype(np.uint8)).resize((nw,nh),Image.BILINEAR)
    a=np.asarray(im,dtype=np.float32)/255.0
    out=np.zeros((S,S),dtype=np.float32)
    oy=(S-nh)//2; ox=(S-nw)//2
    out[oy:oy+nh, ox:ox+nw]=a
    return out

X=np.array([raster(c).ravel() for c in comps])
# add aspect ratio as a feature (weighted): 1 vs 0 are narrow/round
ar=np.array([[c['w']/float(c['h'])] for c in comps],dtype=np.float32)
F=np.hstack([X, np.clip(ar,0,3)*6.0])
np.random.seed(7)
K=28
cent,lab=kmeans2(F,K,minit='++',iter=60,seed=7)
cnt=np.bincount(lab,minlength=K)
print('cluster sizes:',sorted(cnt,reverse=True))
json.dump([int(v) for v in lab],open('labels.json','w'))

# montage: up to 8 examples per cluster, clusters ordered by size
order=np.argsort(-cnt)
TH=30
rows=[]
for k in order:
    if cnt[k]==0: continue
    idx=np.where(lab==k)[0][:8]
    tiles=[]
    for i in idx:
        c=comps[i]
        sub=INK[c['y']:c['y1'], c['x']:c['x1']]
        im=Image.fromarray(((1-sub)*255).astype(np.uint8))
        sc=TH/float(im.size[1]); im=im.resize((max(4,int(im.size[0]*sc)),TH),Image.LANCZOS)
        tiles.append(im)
    rows.append((k,int(cnt[k]),tiles))
wmax=max(60+sum(t.size[0]+6 for t in r[2]) for r in rows)
sheet=Image.new('L',(wmax, len(rows)*(TH+10)+6),255)
d=ImageDraw.Draw(sheet)
for j,(k,n,tiles) in enumerate(rows):
    y=j*(TH+10)+3
    d.text((2,y+8),f'{k:02d} n={n:3d}',fill=0)
    x=62
    for t in tiles:
        sheet.paste(t,(x,y)); x+=t.size[0]+6
sheet.save('clusters.png'); print('clusters.png',sheet.size)
