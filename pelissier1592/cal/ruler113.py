# usage: python cal/ruler113.py img y0 y1 x0 x1 out.jpg : crop with x ticks every 25 px (labels every 100) and y ticks
import sys
from PIL import Image, ImageDraw
im,y0,y1,x0,x1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
c=Image.open(f'img/{im}.jpg').convert('RGB').crop((x0,y0,x1,y1)); sc=1800/c.width
c=c.resize((1800,int(c.height*sc))); W,H=c.size
o=Image.new('RGB',(W+60,H+30),'white'); o.paste(c,(60,0)); d=ImageDraw.Draw(o)
for x in range((x0//25+1)*25,x1,25):
    X=60+int((x-x0)*sc); d.line((X,H,X,H+(12 if x%100==0 else 5)),fill='red')
    if x%100==0: d.text((X+2,H+12),str(x),fill='red')
for y in range((y0//25+1)*25,y1,25):
    Y=int((y-y0)*sc); d.line((50,Y,60,Y),fill='blue'); d.text((0,Y-5),str(y),fill='blue')
o.save('cal/crops/'+out,quality=92)
