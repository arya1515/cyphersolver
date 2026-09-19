# usage: python cal/atlas113.py strip.png  img:x:y:label ...   -> strip in cal/crops (for viewing)
#        python cal/atlas113.py --save img:x:y:letter_token_n ... -> cal/atlas/<name>.png + index line
import sys
from PIL import Image, ImageDraw
W,H=150,190
args=sys.argv[1:]; save=args[0]=='--save'
if save: args=args[1:]
else: out=args.pop(0)
ims={}; tiles=[]
for a in args:
    im,x,y,lab=a.split(':'); x=int(x); y=int(y)
    if im not in ims: ims[im]=Image.open(f'img/{im}.jpg').convert('L')
    box=(x-W//2,y-H//2-10,x+W//2,y+H//2-10)
    t=ims[im].crop(box)
    if save:
        t.save(f'cal/atlas/{lab}.png')
        with open('cal/atlas/index_113.txt','a',encoding='utf-8') as f: f.write(f'{lab}.png\t{im}.jpg\t{box[0]},{box[1]},{box[2]},{box[3]}\n')
    tiles.append((t,lab))
if not save:
    s=Image.new('L',(W*len(tiles),H+20),255); d=ImageDraw.Draw(s)
    for i,(t,lab) in enumerate(tiles): s.paste(t,(i*W,0)); d.text((i*W+4,H+4),lab,fill=0)
    s=s.resize((s.width*2,s.height*2),Image.LANCZOS); s.save('cal/crops/'+out)
