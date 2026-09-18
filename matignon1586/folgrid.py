import sys, os
from PIL import Image, ImageOps, ImageDraw
ids=[int(x) for x in sys.argv[1].split(',')] if ',' in sys.argv[1] else list(range(*[int(x) for x in sys.argv[1].split('-')]))
tiles=[]
for c in ids:
    fn=f'nav/c{c:03d}.jpg'
    if not os.path.exists(fn): continue
    im=Image.open(fn).convert('L')
    W,H=im.size
    t=im.crop((int(W*0.74),0,W,int(H*0.13)))
    t=ImageOps.autocontrast(t,1).resize((700,int(700*t.height/t.width)),Image.LANCZOS)
    tiles.append((c,t))
cols=3; rowh=max(t.height for _,t in tiles)+22
rows=(len(tiles)+cols-1)//cols
out=Image.new('L',(700*cols,rowh*rows),255); d=ImageDraw.Draw(out)
for k,(c,t) in enumerate(tiles):
    x=700*(k%cols); y=rowh*(k//cols)
    d.text((x+6,y+4),f'c{c}',fill=0); out.paste(t,(x,y+20))
out.save(sys.argv[2]); print(out.size)
