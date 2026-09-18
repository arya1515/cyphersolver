import sys,numpy as np
from PIL import Image
c=sys.argv[1]; y0=float(sys.argv[2]); step=float(sys.argv[3]); n=int(sys.argv[4]); x0,x1=int(sys.argv[5]),int(sys.argv[6]); nseg=int(sys.argv[7]); sc=float(sys.argv[8]) if len(sys.argv)>8 else 0.8
im=Image.open(f'hi/c{c}.jpg').convert('L'); w,h=im.size; s=w/1000
xs=np.linspace(x0,x1,nseg+1)
for li in range(n):
    y=y0+li*step
    for j in range(nseg):
        cr=im.crop((int((xs[j]-10)*s),int((y-step*0.7)*s),int((xs[j+1]+10)*s),int((y+step*0.55)*s)))
        cr=cr.resize((int(cr.width*sc),int(cr.height*sc)),Image.LANCZOS)
        cr.save(f'strips/{c}_M{li:02d}{"abcd"[j]}.jpg')
