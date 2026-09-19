"""Magnify an x,y box of a block image for digit-level reading."""
import sys, os
from PIL import Image, ImageOps
src,out=sys.argv[1],sys.argv[2]
x0,y0,x1,y1=[int(v) for v in sys.argv[3:7]]
SC=float(os.environ.get('SC','3.0'))
im=Image.open(src).convert('L').crop((x0,y0,x1,y1))
im=im.resize((int(im.size[0]*SC),int(im.size[1]*SC)),Image.LANCZOS)
im=ImageOps.autocontrast(im,cutoff=1)
im.save(out); print(out,im.size)
