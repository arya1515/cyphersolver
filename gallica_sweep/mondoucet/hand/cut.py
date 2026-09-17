# cut.py canvas x0 x1 y0 y1 npieces scale name  -> hand/pieces/name_pN.png ; coordinates in full-res pixels
import sys, os
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS=None
c,x0,x1,y0,y1,n,sc,name=sys.argv[1],*map(int,sys.argv[2:6]),int(sys.argv[6]),float(sys.argv[7]),sys.argv[8]
im=Image.open('../full16127/%s.jpg'%c).convert('L'); im=ImageOps.autocontrast(im,cutoff=1)
os.makedirs('hand/pieces',exist_ok=True)
w=(x1-x0)/n; ov=int(0.04*(x1-x0))
for i in range(n):
    a=int(x0+i*w)-(ov if i else 0); b=int(x0+(i+1)*w)+(ov if i<n-1 else 0)
    cr=im.crop((a,y0,b,y1)); cr=cr.resize((int(cr.width*sc),int(cr.height*sc)),Image.LANCZOS)
    cr.save('hand/pieces/%s_p%d.png'%(name,i)); print('hand/pieces/%s_p%d.png'%(name,i),cr.size,'x',a,b)
