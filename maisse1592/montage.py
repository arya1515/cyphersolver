"""Montage the folio-number corner (top-right of the right-hand page) of several canvases."""
import sys, glob, os
from PIL import Image, ImageDraw
idxs=[int(a) for a in sys.argv[2:]]
out=sys.argv[1]
tiles=[]
for i in idxs:
    g=sorted(glob.glob(f'img/c{i:03d}_w*.jpg'))
    if not g: print('miss',i); continue
    im=Image.open(g[-1]); W,H=im.size
    # right-hand page top strip, right 40% of the full opening
    c=im.crop((int(W*0.62),0,W,int(H*0.14))).convert('L')
    c=c.resize((520,int(520*c.size[1]/c.size[0])))
    tiles.append((i,c))
if not tiles: sys.exit('no tiles')
tw=520; th=max(t[1].size[1] for t in tiles)+18
cols=2; rows=(len(tiles)+cols-1)//cols
sheet=Image.new('L',(tw*cols,th*rows),255)
d=ImageDraw.Draw(sheet)
for n,(i,c) in enumerate(tiles):
    x=(n%cols)*tw; y=(n//cols)*th
    sheet.paste(c,(x,y+18)); d.text((x+4,y+4),f'canvas {i}',fill=0)
sheet.save(out); print(out, sheet.size)
