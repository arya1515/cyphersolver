import sys
from PIL import Image
c=sys.argv[1]; ys=[float(v) for v in sys.argv[2].split(',')]; x0,x1=float(sys.argv[3]),float(sys.argv[4]); h=float(sys.argv[5]); sc=float(sys.argv[6]); n=int(sys.argv[7])
im=Image.open(f'hi/c{c}.jpg').convert('L'); s=im.width/1000
w=(x1-x0)/n
for k,y in enumerate(ys):
    for j in range(n):
        a=x0+j*w-12; b=x0+(j+1)*w+12
        cr=im.crop((int(a*s),int((y-h*0.62)*s),int(b*s),int((y+h*0.38)*s)))
        cr=cr.resize((int(cr.width*sc),int(cr.height*sc)),Image.LANCZOS); cr.save(f'strips/n20_{c}_{k:02d}{"abcd"[j]}.jpg')
