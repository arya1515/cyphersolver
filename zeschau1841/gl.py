# enhanced gloss crops: page, x0, x1, baseline-y, tag -> 3 overlapping zoomed segments
import sys, numpy as np
from PIL import Image, ImageFilter
f,x0,x1,y,tag=sys.argv[1],*map(int,sys.argv[2:5]),sys.argv[5]
im=Image.open(f).convert('L')
w=(x1-x0)//3
for k in range(3):
    a0=x0+k*w-40; c=im.crop((a0,y-200,a0+w+80,y+60))
    g=np.asarray(c).astype(float); bg=np.asarray(c.filter(ImageFilter.GaussianBlur(25))).astype(float)
    out=np.clip(255-(bg-g)*9,0,255).astype(np.uint8)
    Image.fromarray(out).save(f'img/lines/g_{tag}_{k}.png')
