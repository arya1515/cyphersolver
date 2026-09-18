import sys, os
from PIL import Image, ImageDraw
c=int(sys.argv[1]); x0,x1,y0,y1=map(int,sys.argv[2:6]); step=int(sys.argv[6]) if len(sys.argv)>6 else 400
img=Image.open(f'img/c{c}.jpg').convert('RGB')
w=(x1-x0)/3; cuts=[int(x0+w),int(x0+2*w)]
d=ImageDraw.Draw(img)
for cx in cuts: d.line([(cx,y0),(cx,y1)],fill=(255,0,0),width=3)
os.makedirs(f'b3/{c}',exist_ok=True)
for f in os.listdir(f'b3/{c}'): os.remove(f'b3/{c}/{f}')
xs=[x0]+cuts+[x1]; n=0; y=y0
while y<y1:
    for h in range(3):
        cr=img.crop((xs[h]-60,y,xs[h+1]+60,y+step+60)); r=1900/cr.width
        cr.resize((1900,int(cr.height*r)),Image.LANCZOS).save(f'b3/{c}/{n:02d}{"abc"[h]}.jpg',quality=88)
    n+=1; y+=step
print(c,n)
