import sys
from PIL import Image
f,out,x0,y0,x1,y1=sys.argv[1],sys.argv[2],*map(float,sys.argv[3:7])
im=Image.open(f); W,H=im.size
c=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
c.thumbnail((1800,1800)); c.save(out,quality=88)
