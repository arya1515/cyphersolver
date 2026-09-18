import sys
from PIL import Image
f,x0,y0,x1,y1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
w=int(sys.argv[7]) if len(sys.argv)>7 else 1900
im=Image.open(f).crop((x0,y0,x1,y1))
r=w/im.width; im=im.resize((w,int(im.height*r)),Image.LANCZOS); im.save(out,quality=90)
