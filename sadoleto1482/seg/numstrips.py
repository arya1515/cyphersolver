"""numbered glyph strips: python seg/numstrips.py glyphs.json outprefix [scale] [per]"""
import sys,json
from PIL import Image,ImageDraw,ImageFont
J=json.load(open(sys.argv[1])); out=sys.argv[2]; sc=float(sys.argv[3]) if len(sys.argv)>3 else 2.2; per=int(sys.argv[4]) if len(sys.argv)>4 else 16
im=Image.open(J['src']).convert('L'); ox,oy=J['offset']
from PIL import ImageOps
font=ImageFont.truetype('arial.ttf',18)
for li,L in enumerate(J['lines']):
    y0=min(b[1] for b in L)-8; y1=max(b[3] for b in L)+8
    for h in range(0,len(L),per):
        S=L[h:h+per]; x0=min(b[0] for b in S)-12; x1=max(b[2] for b in S)+12
        c=ImageOps.autocontrast(im.crop((x0+ox,y0+oy,x1+ox,y1+oy)),cutoff=1).convert('RGB')
        c=c.resize((int(c.size[0]*sc),int(c.size[1]*sc)),Image.LANCZOS)
        W,H=c.size; cv=Image.new('RGB',(W,H+26),(255,255,255)); cv.paste(c,(0,26)); d=ImageDraw.Draw(cv)
        for gi,b in enumerate(S,start=h):
            col=(255,0,0) if gi%2 else (0,0,255)
            d.rectangle(((b[0]-x0)*sc,(b[1]-y0)*sc+26,(b[2]-x0)*sc,(b[3]-y0)*sc+26),outline=col)
            d.text(((b[0]-x0)*sc,2),str(gi),fill=col,font=font)
        cv.save(f'{out}_L{li+1:02d}_{h//per+1}.png')
