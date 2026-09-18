import sys
from PIL import Image
c=sys.argv[1]; y0,y1,step,hh=[float(v) for v in sys.argv[2:6]]; x0,x1=float(sys.argv[6]),float(sys.argv[7]); sc=float(sys.argv[8]); tag=sys.argv[9]
im=Image.open(f'hi/c{c}.jpg').convert('L'); s=im.width/1000
xm=(x0+x1)/2; k=0; y=y0
while y<y1:
    for j,(a,b) in enumerate([(x0,xm+12),(xm-12,x1)]):
        cr=im.crop((int(a*s),int(y*s),int(b*s),int((y+hh)*s)))
        cr=cr.resize((int(cr.width*sc),int(cr.height*sc)),Image.LANCZOS); cr.save(f'strips/{tag}_{c}_{k:02d}{"ab"[j]}.jpg')
    k+=1; y+=step
print(k)
