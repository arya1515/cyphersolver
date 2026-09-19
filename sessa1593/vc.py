import sys, os
from PIL import Image, ImageDraw
out=sys.argv[1]; nums=[int(x) for x in sys.argv[2:]]
SC=float(os.environ.get('SC','0.78'))
parts=[]
for n in nums:
    im=Image.open(f'D162/D{n:02d}.png').convert('L')
    im=im.resize((int(im.size[0]*SC),int(im.size[1]*SC)),Image.LANCZOS)
    parts.append((f'line {n}',im))
w=max(p.size[0] for _,p in parts); h=sum(p.size[1]+18 for _,p in parts)
s=Image.new('L',(w,h),255); d=ImageDraw.Draw(s); y=0
for t,p in parts:
    d.text((3,y+3),t,fill=0); s.paste(p,(0,y+18)); y+=p.size[1]+18
s.save(out); print(out,s.size)
