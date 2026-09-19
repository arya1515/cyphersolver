"""Render numbered line strips: python seg/strips.py <glyphs.json> <outprefix> [scale]"""
import sys,json
from PIL import Image,ImageDraw,ImageFont
Image.MAX_IMAGE_PIXELS=None
J=json.load(open(sys.argv[1])); out=sys.argv[2]; sc=float(sys.argv[3]) if len(sys.argv)>3 else 2.0
im=Image.open(J['src']).convert('RGB'); ox,oy=J['offset']
try: font=ImageFont.truetype('arial.ttf',18)
except: font=None
for li,L in enumerate(J['lines']):
    if not L: continue
    per=22
    for h in range(0,len(L),per):
        S=L[h:h+per]
        x0=min(b[0] for b in S)-15; x1=max(b[2] for b in S)+15
        y0=min(b[1] for b in L)-10; y1=max(b[3] for b in L)+10
        crop=im.crop((x0+ox,y0+oy,x1+ox,y1+oy)).resize((int((x1-x0)*sc),int((y1-y0)*sc)),Image.LANCZOS)
        W,H=crop.size; canvas=Image.new('RGB',(W,H+30),(255,255,255)); canvas.paste(crop,(0,30)); d=ImageDraw.Draw(canvas)
        for gi,b in enumerate(S,start=h):
            bx0=(b[0]-x0)*sc; bx1=(b[2]-x0)*sc; by0=(b[1]-y0)*sc+30; by1=(b[3]-y0)*sc+30
            d.rectangle((bx0,by0,bx1,by1),outline=(255,0,0) if gi%2 else (0,0,255))
            d.text((bx0,2 if gi%2 else 14),str(gi),fill=(255,0,0) if gi%2 else (0,0,255),font=font)
        canvas.save(f'{out}_L{li+1:02d}_{h//per+1}.png')
print('strips',len(J['lines']))
