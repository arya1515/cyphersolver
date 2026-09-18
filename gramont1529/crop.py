import sys
from PIL import Image, ImageOps
f,x0,y0,x1,y1,out=sys.argv[1],*map(float,sys.argv[2:6]),sys.argv[6]
W=int(sys.argv[7]) if len(sys.argv)>7 else 1800
im=Image.open(f).convert('L'); w,h=im.size
c=im.crop((int(x0*w),int(y0*h),int(x1*w),int(y1*h)))
c=ImageOps.autocontrast(c,cutoff=1)
if c.width>W: c=c.resize((W,int(c.height*W/c.width)),Image.LANCZOS)
c.save(out,quality=88)
