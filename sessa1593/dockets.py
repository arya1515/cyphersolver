"""Montage the top-right docket corner (piece number) for a range of canvases."""
import sys, glob, os
from PIL import Image, ImageDraw
vol=os.environ.get('VOL','3983'); out=sys.argv[1]; idxs=[int(a) for a in sys.argv[2:]]
ims=[]
for i in idxs:
    p=sorted(glob.glob(f'img{vol}/c{i:04d}_full_w*.jpg'))
    if not p: continue
    im=Image.open(p[-1]).convert('L'); W,H=im.size
    c=im.crop((int(W*0.52),0,W,int(H*0.11)))
    c=c.resize((470,int(470*c.size[1]/c.size[0])),Image.LANCZOS)
    ims.append((f'c{i}',c))
cols=2; rows=(len(ims)+cols-1)//cols
tw=470; th=max(i.size[1] for _,i in ims)+16
s=Image.new('L',(tw*cols,th*rows),255); d=ImageDraw.Draw(s)
for n,(t,i) in enumerate(ims):
    x=(n%cols)*tw; y=(n//cols)*th
    d.text((x+3,y+2),t,fill=0); s.paste(i,(x,y+16))
s.save(out); print(out,s.size,len(ims))
