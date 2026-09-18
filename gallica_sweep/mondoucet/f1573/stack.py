# stack.py prefix n per -> prefix_Gkk.png stacking line halves a,b for `per` lines, with line labels
import sys, glob
from PIL import Image, ImageDraw
pre,n,per=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
for g in range(0,n,per):
    ims=[]
    for i in range(g+1,min(n,g+per)+1):
        for h in 'ab':
            im=Image.open(f'{pre}{i:02d}{h}.png').convert('RGB')
            d=ImageDraw.Draw(im); d.text((2,2),f'{i}{h}',fill=(255,0,0)); ims.append(im)
    W=max(i.width for i in ims); H=sum(i.height for i in ims)
    out=Image.new('RGB',(W,H),'white'); y=0
    for i in ims: out.paste(i,(0,y)); y+=i.height
    out.save(f'{pre}G{g+1:02d}.png')
