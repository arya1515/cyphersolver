"""View a horizontal band of a block image, split into left/right halves at readable scale."""
import sys, os
from PIL import Image, ImageDraw
src=sys.argv[1]; out=sys.argv[2]; y0=int(sys.argv[3]); y1=int(sys.argv[4])
SC=float(os.environ.get('SC','1.25')); OV=int(os.environ.get('OV','140')); NH=int(os.environ.get('NH','2'))
im=Image.open(src).convert('L'); W,H=im.size
y0=max(0,y0); y1=min(H,y1)
b=im.crop((0,y0,W,y1))
step=W//NH
parts=[]
for i in range(NH):
    a=max(0,i*step-OV); z=min(W,(i+1)*step+OV)
    c=b.crop((a,0,z,b.size[1]))
    c=c.resize((int(c.size[0]*SC),int(c.size[1]*SC)),Image.LANCZOS)
    parts.append((f'y{y0}-{y1} part{i+1}',c))
w=max(p.size[0] for _,p in parts); h=sum(p.size[1]+20 for _,p in parts)
s=Image.new('L',(w,h),255); d=ImageDraw.Draw(s); yy=0
for t,p in parts:
    d.text((3,yy+4),t,fill=0); s.paste(p,(0,yy+20)); yy+=p.size[1]+20
s.save(out); print(out,s.size)
