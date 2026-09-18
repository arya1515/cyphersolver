"""Flatten parchment and sharpen a block once, so every later step works on a clean image."""
import sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter
src,out=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('L')
a=np.array(im).astype(np.float32)
bg=np.array(im.filter(ImageFilter.GaussianBlur(25))).astype(np.float32)
flat=np.clip(a/np.maximum(bg,1)*180,0,255).astype(np.uint8)
o=Image.fromarray(flat).filter(ImageFilter.UnsharpMask(radius=3.0,percent=220,threshold=2))
o=ImageOps.autocontrast(o,cutoff=2)
o.save(out); print(o.size)
