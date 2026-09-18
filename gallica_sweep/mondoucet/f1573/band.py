# band.py canvas qx0 qx1 qy0 qy1 scale out   (coords in 1240-wide preview units)
import sys
from PIL import Image, ImageOps
c,x0,x1,y0,y1,sc,out=sys.argv[1],*map(float,sys.argv[2:7]),sys.argv[7]
im=Image.open(f'full16127/c{c}.jpg').convert('L'); s=im.width/1240
cr=im.crop((int(x0*s),int(y0*s),int(x1*s),int(y1*s)))
cr=ImageOps.autocontrast(cr,cutoff=1)
cr=cr.resize((int(cr.width*sc),int(cr.height*sc)),Image.LANCZOS); cr.save(out); print(out,cr.size)
