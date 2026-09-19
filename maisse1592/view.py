"""Stack line strips as left/right halves at readable scale for hand transcription."""
import sys, os
from PIL import Image, ImageDraw
outp=sys.argv[1]; d=sys.argv[2]; nums=[int(x) for x in sys.argv[3:]]
SC=float(os.environ.get('SC','1.15')); OV=int(os.environ.get('OV','120'))
parts=[]
for n in nums:
    im=Image.open(f'{d}/L{n:02d}.png').convert('L'); W,H=im.size
    mid=W//2
    for tag,box in (('a',(0,0,mid+OV,H)),('b',(mid-OV,0,W,H))):
        c=im.crop(box)
        c=c.resize((int(c.size[0]*SC),int(c.size[1]*SC)),Image.LANCZOS)
        parts.append((f'L{n}{tag}',c))
w=max(p.size[0] for _,p in parts); h=sum(p.size[1]+20 for _,p in parts)
s=Image.new('L',(w,h),255); dr=ImageDraw.Draw(s); y=0
for t,p in parts:
    dr.text((3,y+4),t,fill=0); s.paste(p,(0,y+20)); y+=p.size[1]+20
s.save(outp); print(outp,s.size)
