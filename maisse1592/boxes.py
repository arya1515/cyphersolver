"""Draw the segmentation boxes on one line so the split can be checked by eye."""
import sys, json
from PIL import Image, ImageDraw
li=int(sys.argv[1]); out=sys.argv[2]
seg=json.load(open('seg370.json'))
rec=[r for r in seg if r['line']==li][0]
im=Image.open('img/r419_pct49_23_50_40_w3500.jpg').convert('RGB')
band=im.crop((0,rec['y0'],im.size[0],rec['y1']))
d=ImageDraw.Draw(band)
for i,(x0,x1) in enumerate(rec['groups']):
    d.rectangle([x0,0,x1,band.size[1]-1],outline=(220,0,0),width=3)
half=band.size[0]//2
parts=[band.crop((0,0,half,band.size[1])),band.crop((half,0,band.size[0],band.size[1]))]
SC=1.6
parts=[p.resize((int(p.size[0]*SC),int(p.size[1]*SC)),Image.LANCZOS) for p in parts]
s=Image.new('RGB',(parts[0].size[0],sum(p.size[1]+8 for p in parts)),(255,255,255))
y=0
for p in parts: s.paste(p,(0,y)); y+=p.size[1]+8
s.save(out); print(out,s.size,len(rec['groups']),'groups')
