import sys
from PIL import Image, ImageOps
# seg4.py src prefix x0 x1 y0 h n [up]: n horizontal pieces of one band
src,pre=sys.argv[1],sys.argv[2]; x0,x1,y0,h,n=map(int,sys.argv[3:8]); up=float(sys.argv[8]) if len(sys.argv)>8 else 3
im=Image.open(src).convert('L'); w=(x1-x0)//n
for i in range(n):
    a=x0+i*w-40 if i else x0; b=min(x1,x0+(i+1)*w+40)
    c=ImageOps.autocontrast(im.crop((a,y0,b,y0+h)),cutoff=1)
    c.resize((int(c.size[0]*up),int(h*up)),Image.LANCZOS).save(f'{pre}_{i}.png')
