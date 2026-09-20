"""Connected-component digit extraction from the f.370 cipher block."""
import json, numpy as np
from PIL import Image
from scipy import ndimage

SRC='img/r419_pct49_23_50_40_w3500.jpg'
A=np.asarray(Image.open(SRC).convert('L'),dtype=np.float32)
INK=(A < A.mean()-0.42*A.std())
seg=json.load(open('seg370.json'))
lines=[r for r in seg if r['line']>=3]
print('cipher lines',len(lines))

comps=[]
for r in lines:
    y0,y1=r['y0'],r['y1']
    band=INK[y0:y1]
    lab,n=ndimage.label(band, structure=np.array([[1,1,1],[1,1,1],[1,1,1]]))
    objs=ndimage.find_objects(lab)
    for k,sl in enumerate(objs,1):
        ys,xs=sl
        h=ys.stop-ys.start; w=xs.stop-xs.start
        area=int((lab[sl]==k).sum())
        if area<28 or h<9 or w<4: continue           # specks
        if h>0.92*(y1-y0): continue                  # tall strokes from the line above/below
        comps.append({'line':r['line'],'x':int(xs.start),'x1':int(xs.stop),
                      'y':int(y0+ys.start),'y1':int(y0+ys.stop),
                      'w':int(w),'h':int(h),'area':area})
print('components:',len(comps))
w=np.array([c['w'] for c in comps]); h=np.array([c['h'] for c in comps])
print('cc width  median',int(np.median(w)),'p05',int(np.percentile(w,5)),'p95',int(np.percentile(w,95)))
print('cc height median',int(np.median(h)),'p05',int(np.percentile(h,5)),'p95',int(np.percentile(h,95)))
per_line={}
for c in comps: per_line[c['line']]=per_line.get(c['line'],0)+1
print('components per line:', [per_line.get(l['line'],0) for l in lines])
json.dump(comps,open('comps.json','w'))
