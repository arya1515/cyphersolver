import sys
from PIL import Image, ImageOps
# rows.py src prefix x0 x1 yfirst pitch nlines pieces up [halfheight]
src,pre=sys.argv[1],sys.argv[2]; x0,x1,yf,pitch,nl,pc=map(int,sys.argv[3:9]); up=float(sys.argv[9]); hh=int(sys.argv[10]) if len(sys.argv)>10 else 40
im=Image.open(src).convert('L'); w=(x1-x0)/pc
for l in range(nl):
    yc=yf+l*pitch
    for k in range(pc):
        a=int(x0+k*w-40) if k else x0; b=int(min(x1,x0+(k+1)*w+40))
        c=ImageOps.autocontrast(im.crop((a,yc-hh,b,yc+hh)),cutoff=1)
        c.resize((int(c.size[0]*up),int(c.size[1]*up)),Image.LANCZOS).save(f'{pre}_L{l+1:02d}_{k}.png')
