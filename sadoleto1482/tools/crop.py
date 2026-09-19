import sys
from PIL import Image, ImageOps
# usage: crop.py src out x0 y0 x1 y1 (thumb coords at width 1600) [scale]
src,out=sys.argv[1],sys.argv[2]; x0,y0,x1,y1=map(float,sys.argv[3:7]); up=float(sys.argv[7]) if len(sys.argv)>7 else 2
im=Image.open(src).convert('L'); s=im.size[0]/float(__import__("os").environ.get("TW","1600"))
c=im.crop((int(x0*s),int(y0*s),int(x1*s),int(y1*s))); c=ImageOps.autocontrast(c,cutoff=1)
c=c.resize((int(c.size[0]*up),int(c.size[1]*up)),Image.LANCZOS); c.save(out); print(c.size)
