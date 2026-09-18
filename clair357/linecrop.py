import sys
from PIL import Image, ImageOps
c=int(sys.argv[1]); y=int(sys.argv[2]); tag=sys.argv[3]
im=Image.open(f'img/c{c:03d}.jpg').convert('L'); w,h=im.size
x0=int(w*0.07); n=3; step=(w-x0)//n
for i in range(n):
    a=x0+i*step-60; b=min(w,x0+(i+1)*step+60)
    cr=ImageOps.autocontrast(im.crop((a,y-75,b,y+85)),cutoff=1)
    cr=cr.resize((int(cr.size[0]*1.5),int(cr.size[1]*1.5)),Image.LANCZOS)
    cr.save(f'ln/{tag}_{i}.png')
