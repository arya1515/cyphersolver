import os, sys
from PIL import Image, ImageOps, ImageDraw
from glob import glob
files=sorted(glob('sweep/c*.jpg'))
n=len(files); made=0
for i in range(0,n,2):
    pair=files[i:i+2]
    ids=[os.path.basename(f)[1:4] for f in pair]
    out=f'sheets/s{ids[0]}.png'
    if os.path.exists(out): continue
    ims=[]
    for f in pair:
        im=Image.open(f).convert('L'); im=im.resize((900,int(im.height*900/im.width)),Image.LANCZOS)
        im=ImageOps.autocontrast(im,cutoff=1); ims.append(im)
    h=max(im.height for im in ims)
    sheet=Image.new('L',(900*len(ims),h+30),255); d=ImageDraw.Draw(sheet)
    for k,im in enumerate(ims):
        sheet.paste(im,(900*k,30)); d.text((900*k+10,5),'canvas '+ids[k],fill=0)
    sheet.save(out); made+=1
print('sheets made',made,'of',n//2)
