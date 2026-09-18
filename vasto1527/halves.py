import sys
from PIL import Image
c=sys.argv[1]; y0,y1,step=int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
x0,x1=int(sys.argv[5]),int(sys.argv[6])
im=Image.open(f'hi/c{c}.jpg'); w,h=im.size; s=w/1000
xm=(x0+x1)//2
for k,y in enumerate(range(y0,y1,step)):
    for j,(a,b) in enumerate([(x0,xm+30),(xm-30,x1)]):
        cr=im.crop((int(a*s),int(y*s),int(b*s),int((y+step+20)*s)))
        cr=cr.resize((cr.width*7//10,cr.height*7//10))
        cr.save(f'strips/{c}_{k:02d}{"ab"[j]}.jpg')
