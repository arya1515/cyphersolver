import sys,numpy as np
from PIL import Image
c=sys.argv[1]; y0=float(sys.argv[2]); step=float(sys.argv[3]); n=int(sys.argv[4]); x0,x1=int(sys.argv[5]),int(sys.argv[6]); nseg=int(sys.argv[7])
im=Image.open(f'hi/c{c}.jpg').convert('L'); w,h=im.size; s=w/1000
xs=np.linspace(x0,x1,nseg+1)
for li in range(n):
    y=y0+li*step
    for j in range(nseg):
        cr=im.crop((int((xs[j]-12)*s),int((y-step*0.75)*s),int((xs[j+1]+12)*s),int((y+step*0.6)*s)))
        cr.save(f'strips/{c}_L{li:02d}{"abcd"[j]}.jpg')
