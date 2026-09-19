"""Contact sheet of glyph crops for given lines: python seg/sheet.py <glyphs.json> <out.png> <line numbers (1-based), e.g. 1 2>"""
import sys,json
from PIL import Image,ImageDraw,ImageFont
Image.MAX_IMAGE_PIXELS=None
J=json.load(open(sys.argv[1])); out=sys.argv[2]; lines=[int(x) for x in sys.argv[3:]]
im=Image.open(J['src']).convert('L'); ox,oy=J['offset']
font=ImageFont.truetype('arial.ttf',16)
H=96; PER=18; pad=6
cells=[]
for ln in lines:
    L=J['lines'][ln-1]
    for gi,b in enumerate(L):
        x0,y0,x1,y1=b[0]+ox-pad,b[1]+oy-pad,b[2]+ox+pad,b[3]+oy+pad
        c=im.crop((x0,y0,x1,y1)); s=H/c.size[1]; c=c.resize((max(8,int(c.size[0]*s)),H),Image.LANCZOS)
        cells.append((f'{ln}.{gi}',c))
CW=110
rows=(len(cells)+PER-1)//PER
sheet=Image.new('L',(PER*CW,rows*(H+22)),255); d=ImageDraw.Draw(sheet)
for k,(lab,c) in enumerate(cells):
    r,cc=divmod(k,PER); x=cc*CW; y=r*(H+22)
    d.text((x+2,y+2),lab,fill=0,font=font)
    w=min(c.size[0],CW-4); sheet.paste(c.crop((0,0,w,H)),(x+2,y+20))
sheet.save(out); print(out,sheet.size,len(cells),'glyphs')
