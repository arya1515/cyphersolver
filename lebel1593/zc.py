import sys
from PIL import Image
c,x0,x1,y0,y1,step,tag=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(f'img3983/c{int(c):04d}_full_w2400.jpg'); xm=(x0+x1)//2
k=0
for a in range(y0,y1,step):
    b=a+step+30
    im.crop((x0,a,xm+60,b)).resize((2*(xm+60-x0),2*(b-a))).save(f'{tag}{k:02d}l.png')
    im.crop((xm-60,a,x1,b)).resize((2*(x1-xm+60),2*(b-a))).save(f'{tag}{k:02d}r.png'); k+=1
print(k)
