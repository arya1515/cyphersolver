import sys
from PIL import Image, ImageOps
c=int(sys.argv[1]); tag=sys.argv[3]; y=int(sys.argv[2]); half=int(sys.argv[4]) if len(sys.argv)>4 else 80
im=Image.open(f'img/c{c:03d}.jpg').convert('L'); w,h=im.size
x0=int(w*0.07); n=3; step=(w-x0)//n
parts=[]
for i in range(n):
    a=x0+i*step-60; b=min(w,x0+(i+1)*step+60)
    cr=ImageOps.autocontrast(im.crop((a,y-half,b,y+half)),cutoff=1)
    parts.append(cr.resize((int(cr.size[0]*1.5),int(cr.size[1]*1.5)),Image.LANCZOS))
W=max(p.size[0] for p in parts); H=sum(p.size[1] for p in parts)+20
s=Image.new('L',(W,H),255); yy=0
for p in parts: s.paste(p,(0,yy)); yy+=p.size[1]+10
s.save(f'ln/{tag}.png')
