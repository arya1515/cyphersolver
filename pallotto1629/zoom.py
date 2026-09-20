import sys
from PIL import Image, ImageOps, ImageFilter
f,x0,y0,x1,y1,sc,out = sys.argv[1],*map(float,sys.argv[2:6]),float(sys.argv[6]),sys.argv[7]
im=Image.open(f).convert('L'); W,H=im.size
c=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
c=c.resize((int(c.width*sc),int(c.height*sc)),Image.LANCZOS)
c=c.filter(ImageFilter.UnsharpMask(radius=3,percent=160,threshold=2))
c=ImageOps.autocontrast(c)
c.save(out,quality=96); print(out,c.size)
