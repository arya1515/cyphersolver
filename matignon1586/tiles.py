import sys
from PIL import Image, ImageOps
src=sys.argv[1]; out=sys.argv[2]
ys=[int(v) for v in sys.argv[3].split(',')]
half=int(sys.argv[4]) if len(sys.argv)>4 else 50
ntile=int(sys.argv[5]) if len(sys.argv)>5 else 2
im=Image.open(src).convert('L'); im=ImageOps.autocontrast(im,1)
W=im.width
for i,y in enumerate(ys):
    band=im.crop((0,max(0,y-half),W,y+half))
    for j in range(ntile):
        x0=W*j//ntile; x1=min(W,W*(j+1)//ntile+60)
        t=band.crop((x0,0,x1,band.height))
        t=t.resize((int(t.width*1.6),int(t.height*1.6)),Image.LANCZOS)
        t.save(f'{out}_{i+1:02d}_{j}.png')
print('tiles',len(ys)*ntile)
