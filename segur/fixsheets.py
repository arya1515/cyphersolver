# rebuild any solo sheet whose partner canvas has since been downloaded (fixed odd/even pairing)
import os
from PIL import Image, ImageOps, ImageDraw
rebuilt=[]
for n in range(1,441,2):
    out=f'sheets/s{n:03d}.png'
    a=f'sweep/c{n:03d}.jpg'; b=f'sweep/c{n+1:03d}.jpg'
    if not (os.path.exists(a) and os.path.exists(b)): continue
    if os.path.exists(out) and Image.open(out).width>=1800: continue
    ims=[]
    for f in (a,b):
        im=Image.open(f).convert('L'); im=im.resize((900,int(im.height*900/im.width)),Image.LANCZOS); ims.append(ImageOps.autocontrast(im,cutoff=1))
    h=max(i.height for i in ims); sheet=Image.new('L',(1800,h+30),255); d=ImageDraw.Draw(sheet)
    for k,im in enumerate(ims): sheet.paste(im,(900*k,30)); d.text((900*k+10,5),f'canvas {n+k}',fill=0)
    sheet.save(out); rebuilt.append(n)
print('rebuilt',rebuilt)
