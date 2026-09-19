"""Extract every cipher group of f.370 as a normalised raster, then cluster by shape.
No digit is ever read: the point is only to know which groups are the SAME group."""
import json, numpy as np
from PIL import Image

SRC='img/r419_pct49_23_50_40_w3500.jpg'
im=Image.open(SRC).convert('L')
A=np.asarray(im,dtype=np.float32)
INK=(A < A.mean()-0.45*A.std())
seg=json.load(open('seg370.json'))

H,W=INK.shape
recs=[]
for r in seg:
    if r['line']<3: continue                      # lines 1-2 are the clear preamble
    y0,y1=r['y0'],r['y1']
    for (x0,x1) in r['groups']:
        if x1-x0<8: continue
        sub=INK[y0:y1, x0:x1]
        if sub.sum()<25: continue
        # tighten to the ink bounding box
        ys=np.where(sub.any(1))[0]; xs=np.where(sub.any(0))[0]
        if len(ys)==0 or len(xs)==0: continue
        sub=sub[ys[0]:ys[-1]+1, xs[0]:xs[-1]+1]
        recs.append({'line':r['line'],'x0':int(x0),'x1':int(x1),
                     'y0':int(y0+ys[0]),'y1':int(y0+ys[-1]+1),
                     'w':int(sub.shape[1]),'h':int(sub.shape[0])})
print('groups extracted:',len(recs))
ws=np.array([r['w'] for r in recs]); hs=np.array([r['h'] for r in recs])
print('width  median',int(np.median(ws)),'p05',int(np.percentile(ws,5)),'p95',int(np.percentile(ws,95)))
print('height median',int(np.median(hs)),'p05',int(np.percentile(hs,5)),'p95',int(np.percentile(hs,95)))
json.dump(recs,open('glyphs.json','w'))

# rasterise: height normalised to 28, width scaled by the same factor, placed in a 44-wide field
def raster(r):
    sub=INK[r['y0']:r['y1'], r['x0']:r['x1']].astype(np.float32)
    ys=np.where(sub.any(1))[0]; xs=np.where(sub.any(0))[0]
    sub=sub[ys[0]:ys[-1]+1, xs[0]:xs[-1]+1]
    h,w=sub.shape
    sc=28.0/h
    nw=max(3,min(44,int(round(w*sc))))
    img=Image.fromarray((sub*255).astype(np.uint8)).resize((nw,28),Image.BILINEAR)
    a=np.asarray(img,dtype=np.float32)/255.0
    out=np.zeros((28,44),dtype=np.float32)
    out[:, :nw]=a
    return out, nw
R=[];Wd=[]
for r in recs:
    a,nw=raster(r); R.append(a.ravel()); Wd.append(nw)
R=np.array(R); Wd=np.array(Wd,dtype=np.float32)
np.save('rasters.npy',R); np.save('widths.npy',Wd)
print('raster matrix',R.shape)
