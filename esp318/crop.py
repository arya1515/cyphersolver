import sys
from PIL import Image, ImageOps
f,x0,y0,x1,y1,sc,out=sys.argv[1:8]
im=Image.open(f)
c=im.crop((int(x0),int(y0),int(x1),int(y1)))
w,h=c.size; s=float(sc)
c=c.resize((int(w*s),int(h*s)),Image.LANCZOS)
c=ImageOps.autocontrast(c.convert('L'))
c.save(out); print(out,c.size)
