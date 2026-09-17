# ruler.py canvas x0 x1 y0 y1 scale name : crop at scale with vertical ruler lines every 50 full-res px, labelled
import sys, os
from PIL import Image, ImageOps, ImageDraw
Image.MAX_IMAGE_PIXELS=None
c,x0,x1,y0,y1=sys.argv[1],*map(int,sys.argv[2:6]); sc=float(sys.argv[6]); name=sys.argv[7]
im=Image.open('../full16127/%s.jpg'%c).convert('L'); im=ImageOps.autocontrast(im,cutoff=1)
cr=im.crop((x0,y0,x1,y1)).resize((int((x1-x0)*sc),int((y1-y0)*sc)),Image.LANCZOS).convert('RGB')
d=ImageDraw.Draw(cr)
for x in range((x0//50+1)*50,x1,50):
    X=int((x-x0)*sc); col=(255,0,0) if x%100==0 else (0,160,255)
    d.line([(X,0),(X,cr.height)],fill=col,width=1)
    if x%100==0: d.text((X+2,2),str(x),fill=(255,0,0)); d.text((X+2,cr.height-12),str(x),fill=(255,0,0))
cr.save('hand/pieces/%s.png'%name); print(name,cr.size)
