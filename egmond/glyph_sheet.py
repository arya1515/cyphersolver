"""Index connected ink components for visual transcription, not automatic OCR."""
from PIL import Image,ImageDraw
import numpy as np,json,pathlib
root=pathlib.Path(__file__).resolve().parent
im=Image.open(root/'images/f27_hi.jpg').convert('RGB')
region=(695,490,2760,655)
crop=im.crop(region)
ink=np.array(crop.convert('L'))<105
seen=np.zeros_like(ink)
boxes=[]
h,w=ink.shape
for y,x in zip(*np.where(ink)):
    if seen[y,x]:continue
    stack=[(int(y),int(x))];seen[y,x]=True;pts=[]
    while stack:
        yy,xx=stack.pop();pts.append((yy,xx))
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
            ny,nx=yy+dy,xx+dx
            if 0<=ny<h and 0<=nx<w and ink[ny,nx] and not seen[ny,nx]:
                seen[ny,nx]=True;stack.append((ny,nx))
    if len(pts)<45:continue
    ys,xs=zip(*pts)
    boxes.append([min(xs),min(ys),max(xs)+1,max(ys)+1,len(pts)])
boxes.sort(key=lambda b:b[0])
sheet=Image.new('RGB',(1200,((len(boxes)+11)//12)*160),'white')
d=ImageDraw.Draw(sheet)
for i,(x0,y0,x1,y1,n) in enumerate(boxes):
    c=crop.crop((max(0,x0-3),max(0,y0-3),min(w,x1+3),min(h,y1+3)))
    c.thumbnail((94,130))
    px=(i%12)*100;py=(i//12)*160
    sheet.paste(c,(px,py+20));d.text((px+3,py+2),str(i+1),fill='black')
sheet.save(root/'images/line1_components.png')
(root/'line1_components.json').write_text(json.dumps({'source':'images/f27_hi.jpg','region':region,'threshold':105,'boxes':boxes,'caution':'Connected components may split or join cipher tokens.'},indent=2))
print('Components:',len(boxes))
