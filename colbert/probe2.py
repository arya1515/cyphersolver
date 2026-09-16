"""Corner-crop montage over a canvas list: python probe2.py <ark> <start> <stop> <step> <out.jpg> [cols]"""
import sys, io, urllib.request, time
from PIL import Image, ImageDraw
ark=sys.argv[1]; a,b,s=int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]); out=sys.argv[5]; cols=int(sys.argv[6]) if len(sys.argv)>6 else 4
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0'}
tiles=[]
for c in range(a,b+1,s):
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{c}/pct:50,0,50,16/450,/0/native.jpg'
    for attempt in range(3):
        try:
            im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=120).read())).convert('L'); break
        except Exception as e:
            im=Image.new('L',(450,140),128); time.sleep(5)
    im=im.resize((450,int(450*im.height/im.width)))
    d=ImageDraw.Draw(im); d.rectangle([0,0,70,18],fill=0); d.text((3,3),f'c{c}',fill=255)
    tiles.append(im); time.sleep(0.4)
w=450; h=max(t.height for t in tiles); rows=(len(tiles)+cols-1)//cols
M=Image.new('L',(w*cols,h*rows),255)
for i,t in enumerate(tiles): M.paste(t,((i%cols)*w,(i//cols)*h))
M.save(out,quality=80); print('saved',out,M.size,len(tiles))
