"""Fetch top-right corner crops of Gallica canvases and montage them so folio stamps can be read in one image.
usage: python probe.py <ark> <canvas,canvas,...> <out.jpg>"""
import sys, io, urllib.request, time
from PIL import Image, ImageDraw
ark, cs, out = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], sys.argv[3]
H={'User-Agent':'Mozilla/5.0 (research script)'}
tiles=[]
for c in cs:
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{c}/pct:45,0,55,22/600,/0/native.jpg'
    try:
        im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=120).read())).convert('L')
    except Exception as e:
        im=Image.new('L',(600,200),128); print(c,'ERR',e)
    im=im.resize((600,int(600*im.height/im.width)))
    d=ImageDraw.Draw(im); d.rectangle([0,0,90,22],fill=0); d.text((4,4),f'c{c}',fill=255)
    tiles.append(im); time.sleep(0.5)
w=600; cols=3; rows=(len(tiles)+cols-1)//cols; h=max(t.height for t in tiles)
M=Image.new('L',(w*cols,h*rows),255)
for i,t in enumerate(tiles): M.paste(t,((i%cols)*w,(i//cols)*h))
M.save(out,quality=80); print('saved',out,M.size)
