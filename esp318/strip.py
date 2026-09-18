import sys
from PIL import Image, ImageOps
# strip.py page line0 nlines [x0f x1f] ; uses TOP0/PITCH constants passed
f=sys.argv[1]; top0=float(sys.argv[2]); pitch=float(sys.argv[3]); k0=int(sys.argv[4]); n=int(sys.argv[5])
x0f=float(sys.argv[6]); x1f=float(sys.argv[7]); sc=float(sys.argv[8]); out=sys.argv[9]
im=Image.open(f); W,H=im.size
y0=int(top0+(k0-1)*pitch)-18; y1=int(top0+(k0-1+n)*pitch)+10
c=im.crop((int(W*x0f),max(0,y0),int(W*x1f),min(H,y1)))
w,h=c.size
c=c.resize((int(w*sc),int(h*sc)),Image.LANCZOS)
c=ImageOps.autocontrast(c.convert('L'))
c.save(out); print(out,c.size,y0,y1)
