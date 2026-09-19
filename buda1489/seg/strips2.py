"""Annotated strips: boxes + agent token + decoded value. python seg/strips2.py <glyphs.json> <trans.csv> <key.json> <outprefix> [scale] [per]"""
import sys,json,csv,re
from PIL import Image,ImageDraw,ImageFont
Image.MAX_IMAGE_PIXELS=None
J=json.load(open(sys.argv[1])); key=json.load(open(sys.argv[3],encoding='utf-8')); out=sys.argv[4]
sc=float(sys.argv[5]) if len(sys.argv)>5 else 1.8; per=int(sys.argv[6]) if len(sys.argv)>6 else 20
tok={}
VAL=False
for r in csv.DictReader(open(sys.argv[2],encoding='utf-8')):
    if 'value' in r: VAL=True
    i=r['idx'].strip().split('-')[0]
    tok.setdefault((int(r['line']),i.rstrip('abc')),'')
    tok[(int(r['line']),i.rstrip('abc'))]+=(('+' if tok[(int(r['line']),i.rstrip('abc'))] else '')+(r['value'] if VAL else r['token']).strip())
im=Image.open(J['src']).convert('RGB'); ox,oy=J['offset']
font=ImageFont.truetype('arial.ttf',15); font2=ImageFont.truetype('arialbd.ttf',17)
for li,L in enumerate(J['lines']):
    ln=li+1
    for h in range(0,len(L),per):
        S=L[h:h+per]
        x0=min(b[0] for b in S)-15; x1=max(b[2] for b in S)+15
        y0=min(b[1] for b in L)-10; y1=max(b[3] for b in L)+10
        crop=im.crop((x0+ox,y0+oy,x1+ox,y1+oy)).resize((int((x1-x0)*sc),int((y1-y0)*sc)),Image.LANCZOS)
        W,H=crop.size; canvas=Image.new('RGB',(W,H+70),(255,255,255)); canvas.paste(crop,(0,25)); d=ImageDraw.Draw(canvas)
        for gi,b in enumerate(S,start=h):
            bx0=(b[0]-x0)*sc; bx1=(b[2]-x0)*sc; by0=(b[1]-y0)*sc+25; by1=(b[3]-y0)*sc+25
            col=(255,0,0) if gi%2 else (0,0,255)
            d.rectangle((bx0,by0,bx1,by1),outline=col)
            d.text((bx0,2),str(gi),fill=col,font=font)
            t=tok.get((ln,str(gi)),'')
            v=t if VAL else (key.get(re.sub(r'\?$','',t),'?') if t and not t.startswith('[') else ('[c]' if t else ''))
            d.text((bx0,H+28),t[:6],fill=(0,0,0),font=font)
            d.text((bx0,H+46),v[:7],fill=(0,120,0),font=font2)
        canvas.save(f'{out}_L{ln:02d}_{h//per+1}.png')
print('done')
