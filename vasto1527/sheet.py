import sys,glob
from PIL import Image,ImageDraw
a,b,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
fs=[f'btv1b90601558/c{i:03d}.jpg' for i in range(a,b+1)]
W,H=300,420; cols=6; rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(W*cols,H*rows),'white'); d=ImageDraw.Draw(S)
for k,f in enumerate(fs):
    try: im=Image.open(f).convert('RGB')
    except: continue
    im.thumbnail((W,H-20)); S.paste(im,((k%cols)*W,(k//cols)*H+20)); d.text(((k%cols)*W+5,(k//cols)*H+3),f[-8:-4],fill='red')
S.save(out,quality=80)
