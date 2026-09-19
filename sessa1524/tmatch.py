import cv2, numpy as np, glob, os, sys
from PIL import Image
def load_tpl(path, xfrac=(0,1)):
    t=cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    w=t.shape[1]; t=t[:,int(w*xfrac[0]):int(w*xfrac[1])]
    return t
# tiles were resized to height 150 from original ~crop; get original scale: tokens.py crops original then resizes to H=150.
# we instead cut templates straight from the source image for true scale:
src=cv2.imread('img/IMG_R9877_I46030_P1.jpg',cv2.IMREAD_GRAYSCALE)
T={}
import json
boxes=json.load(open('tpl_boxes.json'))
for name,(x0,y0,x1,y1) in boxes.items(): T[name]=src[y0:y1,x0:x1]
pages=sorted(glob.glob('img/IMG_R96*.jpg')+glob.glob('img/IMG_R97*.jpg')+glob.glob('img/IMG_R98[3-4]*.jpg')+glob.glob('img/IMG_R9873*.jpg')+glob.glob('img/IMG_R989[0-8]*.jpg'))
res={n:[] for n in T}
for p in pages:
    g=cv2.imread(p,cv2.IMREAD_GRAYSCALE)
    for n,t in T.items():
        best=[]
        for s in (0.85,0.93,1.0,1.08,1.16):
            tt=cv2.resize(t,None,fx=s,fy=s)
            r=cv2.matchTemplate(g,tt,cv2.TM_CCOEFF_NORMED)
            ys,xs=np.where(r>0.55)
            for y,x in zip(ys,xs): best.append((float(r[y,x]),int(x),int(y),tt.shape[1],tt.shape[0]))
        best.sort(reverse=True); kept=[]
        for b in best:
            if all(abs(b[1]-k[1])>b[3]*0.6 or abs(b[2]-k[2])>b[4]*0.6 for k in kept): kept.append(b)
            if len(kept)>=8: break
        for b in kept: res[n].append((b[0],p)+b[1:])
for n in res:
    res[n].sort(reverse=True)
    print(n,[(round(r[0],2),os.path.basename(r[1])[4:18]) for r in res[n][:12]])
json.dump(res,open('tmatch_res.json','w'))
