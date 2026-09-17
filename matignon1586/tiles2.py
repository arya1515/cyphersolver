import sys
from PIL import Image, ImageOps
src, out = sys.argv[1], sys.argv[2]
ys=[int(v) for v in sys.argv[3].split(',')]
half=int(sys.argv[4]); ntile=int(sys.argv[5]); slope=float(sys.argv[6]) if len(sys.argv)>6 else 0.0
im=ImageOps.autocontrast(Image.open(src).convert('L'),1)
W=im.width
for i,y in enumerate(ys):
    for j in range(ntile):
        x0=W*j//ntile; x1=min(W,W*(j+1)//ntile+70)
        dy=int(slope*(x0+x1)/2)
        t=im.crop((x0,max(0,y+dy-half),x1,y+dy+half))
        sc=1900/t.width
        t=t.resize((int(t.width*sc),int(t.height*sc)),Image.LANCZOS)
        t.save(f'{out}_{i+1:02d}_{j}.png')
print('ok')
