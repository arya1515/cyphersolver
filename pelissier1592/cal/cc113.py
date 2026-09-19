# usage: python cal/cc113.py img y0 y1 x0 x1 out.png  -> numbered connected components (ink) drawn on band; prints boxes
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
im,y0,y1,x0,x1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
g=np.array(Image.open(f'img/{im}.jpg').convert('L').crop((x0,y0,x1,y1)))
b=g<110
b=ndimage.binary_closing(b,iterations=2)
lab,n=ndimage.label(b)
objs=ndimage.find_objects(lab)
boxes=[]
for i,s in enumerate(objs):
    ys,xs=s; h=ys.stop-ys.start; w=xs.stop-xs.start
    if (lab[s]==i+1).sum()<150: continue
    boxes.append((xs.start+x0,ys.start+y0,xs.stop+x0,ys.stop+y0))
boxes.sort()
sc=2
img=Image.fromarray(g).convert('RGB').resize((g.shape[1]*sc,g.shape[0]*sc))
d=ImageDraw.Draw(img)
for k,(a,b_,c,e) in enumerate(boxes):
    d.rectangle(((a-x0)*sc,(b_-y0)*sc,(c-x0)*sc,(e-y0)*sc),outline=(255,0,0))
    d.text(((a-x0)*sc+2,(e-y0)*sc-12),str(k),fill=(0,0,255))
    print(k,a,b_,c,e)
img.save('cal/crops/'+out)
