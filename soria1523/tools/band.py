import sys, numpy as np
from PIL import Image, ImageFilter
img,x0,x1,y0,y1,out=sys.argv[1],*map(float,sys.argv[2:6]),sys.argv[6]
im=Image.open(img).convert('L'); W,H=im.size
r=im.crop((int(W*x0),int(H*y0),int(W*x1),int(H*y1)))
a=np.asarray(r).astype(float); bg=np.asarray(r.filter(ImageFilter.GaussianBlur(20))).astype(float)
d=Image.fromarray(np.clip((a-bg)*3+255,0,255).astype('uint8'))
w=d.size[0]
for j,(u,v) in enumerate([(0,w//2+40),(w//2-40,w)]):
  p=d.crop((u,0,v,d.size[1])); p=p.resize((p.size[0]*2,p.size[1]*2)); p.save(f'{out}{"ab"[j]}.jpg')
