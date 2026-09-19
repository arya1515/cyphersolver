import sys
from PIL import Image, ImageOps
# bands.py src prefix x0 x1 y0 y1 [h stride up]
src,pre=sys.argv[1],sys.argv[2]; x0,x1,y0,y1=map(int,sys.argv[3:7])
h=int(sys.argv[7]) if len(sys.argv)>7 else 170; st=int(sys.argv[8]) if len(sys.argv)>8 else 120; up=float(sys.argv[9]) if len(sys.argv)>9 else 1.5
im=Image.open(src).convert('L'); y=y0; i=0
while y<y1:
    c=ImageOps.autocontrast(im.crop((x0,y,x1,y+h)),cutoff=1); w=c.size[0]
    for k,(l,r) in enumerate([(0,w//2+70),(w//2-70,w)]):
        cc=c.crop((l,0,r,h)); cc.resize((int(cc.size[0]*up),int(h*up)),Image.LANCZOS).save(f'{pre}_{i:02d}{"ab"[k]}_y{y}.png')
    y+=st; i+=1
print(i)
