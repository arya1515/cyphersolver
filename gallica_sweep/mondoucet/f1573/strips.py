# strips.py canvas qx0 qx1 out_prefix y1 y2 ... : one strip per line centre (preview units), two halves each
import sys, os
from PIL import Image, ImageOps
SC=float(__import__("os").environ.get("SC","0.5")); c=sys.argv[1]; x0,x1=float(sys.argv[2]),float(sys.argv[3]); pre=sys.argv[4]; ys=[float(v) for v in sys.argv[5:]]
im=Image.open(f'full16127/c{c}.jpg').convert('L'); s=im.width/1240
os.makedirs(os.path.dirname(pre),exist_ok=True)
xm=(x0+x1)/2
for i,y in enumerate(ys):
    for h,(a,b) in enumerate([(x0,xm+25),(xm-25,x1)]):
        cr=im.crop((int(a*s),int((y-24)*s),int(b*s),int((y+22)*s)))
        cr=ImageOps.autocontrast(cr,cutoff=1); cr=cr.resize((int(cr.width*SC),int(cr.height*SC)),Image.LANCZOS)
        cr.save(f'{pre}{i+1:02d}{"ab"[h]}.png')
print('ok',len(ys))
