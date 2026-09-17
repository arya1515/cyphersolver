import sys
from PIL import Image, ImageOps, ImageDraw
Image.MAX_IMAGE_PIXELS=None
c=sys.argv[1]; pref=sys.argv[2]; cores=[tuple(map(int,x.split('-'))) for x in sys.argv[3].split(',')]
x0,x1=int(sys.argv[4]),int(sys.argv[5])
im=Image.open('../full16127/%s.jpg'%c).convert('L'); im=ImageOps.autocontrast(im,cutoff=1)
w=(x1-x0)/3
for k,(s,e) in enumerate(cores):
    y0,y1=s-125,e+90
    for p in range(3):
        a=int(x0+p*w)-(40 if p else 0); b=int(x0+(p+1)*w)+(40 if p<2 else 0)
        cr=im.crop((a,y0,b,y1)).resize((int((b-a)*3),int((y1-y0)*3)),Image.LANCZOS).convert('RGB')
        d=ImageDraw.Draw(cr)
        for x in range((a//50+1)*50,b,50):
            X=int((x-a)*3); col=(255,0,0) if x%100==0 else (0,160,255)
            d.line([(X,0),(X,cr.height)],fill=col,width=1)
            if x%100==0: d.text((X+2,2),str(x),fill=(255,0,0))
        cr.save('hand/pieces/%s%02d_%d.png'%(pref,k+1,p))
print('done',pref,len(cores))
