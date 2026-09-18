"""Render line tiles with unsharp masking and local contrast, for the lines the eye cannot settle."""
import sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter
src,out=sys.argv[1],sys.argv[2]
ys=[int(v) for v in sys.argv[3].split(',')]
half=int(sys.argv[4]); ntile=int(sys.argv[5])
im=Image.open(src).convert('L')
a=np.array(im).astype(np.float32)
# local background estimate, then divide out (flattens parchment)
bg=np.array(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(25))).astype(np.float32)
flat=np.clip(a/np.maximum(bg,1)*180,0,255).astype(np.uint8)
im2=Image.fromarray(flat)
im2=im2.filter(ImageFilter.UnsharpMask(radius=3.0,percent=220,threshold=2))
im2=ImageOps.autocontrast(im2,cutoff=2)
W=im2.width
for i,y in enumerate(ys):
    for j in range(ntile):
        x0=W*j//ntile; x1=min(W,W*(j+1)//ntile+70)
        t=im2.crop((x0,max(0,y-half),x1,y+half))
        sc=1900/t.width
        t=t.resize((int(t.width*sc),int(t.height*sc)),Image.LANCZOS)
        t.save(f'{out}_{i+1:02d}_{j}.png')
print('ok')
