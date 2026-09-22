import sys, numpy as np
from PIL import Image, ImageFilter
f,x0,x1,y0,y1,tag=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
im=Image.open(f).convert('RGB').crop((x0,y0,x1,y1))
a=np.asarray(im).astype(float); g=a.mean(2)
bgim=Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.GaussianBlur(25))
d=np.asarray(bgim).astype(float)-g
out=np.clip(255-d*9,0,255).astype(np.uint8)
Image.fromarray(out).save(f'img/lines/{tag}.png')
