"""Like bands3.py but each token is boxed and numbered, so a hand reading can be written
as one letter per token index (alignment-free ground truth for training)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
Z=2.0
d=json.load(open('raince_tokens.json'))
os.makedirs('img/idx',exist_ok=True)
font=ImageFont.truetype('arialbd.ttf',22); big=ImageFont.truetype('arialbd.ttf',30)
page,ln=sys.argv[1],int(sys.argv[2])
r=d['regions'][page]; toks=[t for t in d['tokens'] if t['page']==page]
x0=r['x0']+min(t['x0'] for t in toks)-25; x1=r['x0']+max(t['x1'] for t in toks)+25; W=x1-x0
pitch=r['pitch']; y=int(r['y0']+r['lines'][ln-1])
im=Image.open(r['img']).convert('L')
top=int(y-pitch*0.72); bot=int(y+pitch*0.62)
band=im.crop((x0,top,x1,bot)).convert('RGB')
dr=ImageDraw.Draw(band)
row=sorted([t for t in toks if t['line']==ln-1],key=lambda t:t['x0'])
for i,t in enumerate(row,1):
    a=r['x0']+t['x0']-x0; b=r['x0']+t['x1']-x0
    dr.rectangle([a-2,0,b+2,band.height-1],outline=(255,0,0))
    dr.text(((a+b)//2-8,band.height-26),str(i),fill=(0,0,200),font=font)
ov=85; n=4
cuts=[(max(0,i*W//n-ov),min(W,(i+1)*W//n+ov)) for i in range(n)]
parts=[band.crop((a,0,b,band.height)).resize((int((b-a)*Z),int(band.height*Z)),Image.LANCZOS) for a,b in cuts]
w=max(p.width for p in parts); h=parts[0].height
out=Image.new('RGB',(w+46,n*(h+12)),(255,255,255)); d2=ImageDraw.Draw(out)
for i,p in enumerate(parts):
    out.paste(p,(46,i*(h+12))); d2.text((6,i*(h+12)+h//2-16),'abcd'[i],fill=(0,0,0),font=big)
    d2.line([(0,i*(h+12)-6),(out.width,i*(h+12)-6)],fill=(150,150,150))
out.save(f'img/idx/{page}_{ln:02d}.png')
print(f'{page} line {ln}: {len(row)} tokens ->', f'img/idx/{page}_{ln:02d}.png', out.size)
