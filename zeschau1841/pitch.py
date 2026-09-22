import sys
from PIL import Image
f,x0,x1,ystart,pitch,n,tag=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(f).convert('L')
for k in range(n):
    c=ystart+k*pitch
    s=im.crop((x0,c-110,x1,c+110)); s.thumbnail((2400,400)); s.save(f'img/lines/{tag}_{k:02d}.png')
