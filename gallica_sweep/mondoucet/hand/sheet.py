# Contact sheet: for glyph type T, crop windows around each occurrence in f.62r/v grouped by the letter it aligned to.
import re,sys
from PIL import Image, ImageOps, ImageDraw
Image.MAX_IMAGE_PIXELS=None
cores={'18':(2906,2967),'19':(3067,3126),'20':(3223,3281),'21':(3380,3436),'22':(3538,3598),'23':(3710,3762),'24':(3866,3919),'25':(4025,4082),'26':(4184,4236),'27':(4345,4413),'28':(4517,4582),'29':(4699,4763),'30':(4861,4927),'31':(5039,5115),'32':(5243,5300),'33':(5399,5434),'34':(5612,5652),
'V1':(792,821),'V2':(950,978),'V3':(1097,1127),'V4':(1253,1284),'V5':(1410,1445)}
X0,X1=1450,4700
ims={}
def img(c):
    if c not in ims:
        im=Image.open('../full16127/%s.jpg'%c).convert('L'); ims[c]=ImageOps.autocontrast(im,cutoff=1)
    return ims[c]
txt=open('hand/align2_out.txt',encoding='utf-8').read().split('\n')
occ={}  # letter -> list of (line,k,N)
i=0
T=sys.argv[1]
while i<len(txt)-1:
    if re.match(r'^ *\w+: ',txt[i]) and txt[i+1].startswith('     '):
        lab=txt[i].split(':')[0].strip(); g=txt[i].split(':',1)[1].split(); d=txt[i+1].split()
        for k,(a,b) in enumerate(zip(g,d)):
            if a==T: occ.setdefault(b[-1] if b!='_' else '_',[]).append((lab,k,len(g)))
        i+=2
    else: i+=1
W=260; rows=[]
for letter,lst in sorted(occ.items(),key=lambda kv:-len(kv[1])):
    for (lab,k,N) in lst[:int(sys.argv[2]) if len(sys.argv)>2 else 6]:
        c='c130' if lab.startswith('V') else 'c129'
        s,e=cores[lab]; xw=X1-X0 if c=='c129' else 3200
        xc=X0+ (k+0.5)/N*xw
        cr=img(c).crop((int(xc-W/2),s-90,int(xc+W/2),e+60)).resize((W*2,(e-s+150)*2),Image.LANCZOS).convert('RGB')
        ImageDraw.Draw(cr).text((4,4),'%s=%s L%s#%d'%(T,letter,lab,k),fill=(255,0,0))
        ImageDraw.Draw(cr).line([(W,0),(W,cr.height)],fill=(0,160,255))
        rows.append((letter,cr))
# stack in rows of 5
per=5; Hs=[]; y=0
sheet_rows=[rows[i:i+per] for i in range(0,len(rows),per)]
H=sum(max(c.height for _,c in r) for r in sheet_rows); S=Image.new('RGB',(W*2*per,H),(255,255,255))
for r in sheet_rows:
    x=0
    for _,c in r: S.paste(c,(x,y)); x+=W*2
    y+=max(c.height for _,c in r)
S.save('hand/pieces/sheet_%s.png'%T.replace('/','sl').replace('*','star').replace('#','hash').replace('@','at').replace('^','lam').replace('+','dag')); print('ok',len(rows))
