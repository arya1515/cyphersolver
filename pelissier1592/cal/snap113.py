# re-center atlas crops on the nearest glyph's ink centroid (x only, band +-45 px around given y), rewrite pngs + index
import numpy as np
from PIL import Image
W,H=150,190
ims={}
rows=[l.rstrip('\n').split('\t') for l in open('cal/atlas/index_113.txt',encoding='utf-8')]
out=[]
for name,imf,box in rows:
    x0,y0,x1,y1=map(int,box.split(',')); cx=(x0+x1)//2; cy=y0+H//2+10
    im=ims.setdefault(imf,Image.open('img/'+imf).convert('L')); a=np.array(im.crop((cx-120,cy-45,cx+120,cy+45)))<110
    x=120
    for _ in range(4):
        sl=a[:,max(0,x-40):x+40]; ys,xs=np.nonzero(sl)
        if len(xs)==0: break
        x=int(max(0,x-40)+xs.mean())
    nx=cx-120+x
    b=(nx-W//2,cy-H//2-10,nx+W//2,cy+H//2-10)
    im.crop(b).save('cal/atlas/'+name)
    out.append(f'{name}\t{imf}\t{b[0]},{b[1]},{b[2]},{b[3]}\t(centre {nx},{cy})\n')
open('cal/atlas/index_113.txt','w',encoding='utf-8').writelines(out)
