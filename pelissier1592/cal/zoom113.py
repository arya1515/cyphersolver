# python cal/zoom113.py out.png name1 name2 ...   (atlas names without .png) -> tight 110x130 zoom strip
import sys,re
from PIL import Image, ImageDraw
idx={l.split('\t')[0]:l for l in open('cal/atlas/index_113.txt',encoding='utf-8')}
tiles=[]
for n in sys.argv[2:]:
    if ':' in n: im,x,y=n.split(':'); cx,cy=int(x),int(y); f=im+'.jpg'; lab=f'{x},{y}'
    else:
        l=idx[n+'.png'].split('\t'); cx,cy=map(int,re.findall(r'\d+',l[3])); f=l[1]; lab=n
    tiles.append((Image.open('img/'+f).convert('L').crop((cx-55,cy-75,cx+55,cy+55)),lab))
s=Image.new('L',(110*len(tiles),150),255); d=ImageDraw.Draw(s)
for i,(t,n) in enumerate(tiles): s.paste(t,(i*110,0)); d.text((i*110+2,135),n[:18],fill=0)
s.resize((s.width*2,s.height*2)).save('cal/crops/'+sys.argv[1])
