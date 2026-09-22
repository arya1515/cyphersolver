import sys, numpy as np
from PIL import Image
f,x0,x1,yc,tag=sys.argv[1],*map(int,sys.argv[2:5]),sys.argv[5]
im=Image.open(f).convert('RGB').crop((x0,yc-190,x1,yc+70))
a=np.asarray(im).astype(float)
g=a[:,:,2]  # blue channel: pencil grey vs paper yellow
bg=np.percentile(g,85); d=np.clip((bg-g)/35,0,1)
out=(255*(1-d)).astype(np.uint8)
Image.fromarray(out).save(f'img/lines/{tag}.png')
