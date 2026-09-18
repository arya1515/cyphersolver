# render a line with numbered glyph boxes, split in N parts at zoom Z: render_idx.py prefix line N Z outprefix
import sys, json
from PIL import Image, ImageDraw
pre,k,N,Z,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
bx=json.load(open(f'{pre}_glyphs.json'))[str(k)]
im=Image.open(f'{pre}_l{k:02d}.png').convert('RGB'); w,h=im.size
big=im.resize((w*Z,h*Z),Image.LANCZOS); d=ImageDraw.Draw(big)
for i,(x0,y0,x1,y1,a) in enumerate(bx):
    d.rectangle((x0*Z,y0*Z,x1*Z,y1*Z),outline=(255,0,0),width=2); d.text((x0*Z+2,2),str(i),fill=(0,0,255))
s=w*Z//N
for j in range(N):
    x0=max(0,j*s-60); x1=min(w*Z,(j+1)*s+60)
    big.crop((x0,0,x1,h*Z)).save(f'{out}_{j}.png')
print(len(bx),'boxes')
