import sys
from PIL import Image, ImageOps
# usage: crop.py img out x0 y0 x1 y1 [scale]  (fractions of width/height)
im=Image.open(sys.argv[1]); W,H=im.size
x0,y0,x1,y1=[float(v) for v in sys.argv[3:7]]
sc=float(sys.argv[7]) if len(sys.argv)>7 else 1.0
c=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
if sc!=1.0: c=c.resize((int(c.width*sc),int(c.height*sc)),Image.LANCZOS)
c=ImageOps.autocontrast(c.convert('L'),cutoff=1)
c.save(sys.argv[2]); print(sys.argv[2],c.size)
