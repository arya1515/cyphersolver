import sys, numpy as np, os
from PIL import Image, ImageDraw
c=int(sys.argv[1]); x0,x1,y0,y1=map(int,sys.argv[2:6]); step=int(sys.argv[6]) if len(sys.argv)>6 else 400
img=Image.open(f'img/c{c}.jpg').convert('RGB')
mid=(x0+x1)//2; d=ImageDraw.Draw(img); d.line([(mid,y0),(mid,y1)],fill=(255,0,0),width=4)
os.makedirs(f'band/{c}',exist_ok=True)
for f in os.listdir(f'band/{c}'): os.remove(f'band/{c}/{f}')
n=0; y=y0
while y<y1:
    for h,(a,b) in enumerate([(x0,mid+80),(mid-80,x1)]):
        cr=img.crop((a,y,b,y+step+70)); r=1900/cr.width
        cr.resize((1900,int(cr.height*r)),Image.LANCZOS).save(f'band/{c}/{n:02d}{"LR"[h]}.jpg',quality=88)
    n+=1; y+=step
print(c,n)
