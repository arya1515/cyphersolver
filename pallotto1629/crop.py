import sys
from PIL import Image, ImageOps
f, x0,y0,x1,y1, scale, out = sys.argv[1], *map(float,sys.argv[2:6]), float(sys.argv[6]), sys.argv[7]
im = Image.open(f); W,H = im.size
c = im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
c = c.resize((int(c.width*scale), int(c.height*scale)), Image.LANCZOS)
c = ImageOps.autocontrast(c.convert('L'))
c.save(out, quality=95); print(out, c.size)
