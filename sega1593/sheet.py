# contact sheet: sheet.py out.png width_per_page files...
import sys
from PIL import Image, ImageDraw
out=sys.argv[1]; w=int(sys.argv[2]); files=sys.argv[3:]
ims=[]
for f in files:
    im=Image.open(f).convert('L'); im=im.resize((w,int(im.height*w/im.width))); ims.append(im)
cols=min(4,len(ims)); rows=(len(ims)+cols-1)//cols; H=max(i.height for i in ims)
sheet=Image.new('L',(cols*w,rows*H),255)
for k,im in enumerate(ims):
    x=(k%cols)*w; y=(k//cols)*H; sheet.paste(im,(x,y)); ImageDraw.Draw(sheet).text((x+5,y+5),files[k].split('_')[-2],fill=0)
sheet.save(out); print(sheet.size)
