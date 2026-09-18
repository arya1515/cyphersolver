import sys,glob,re
from PIL import Image,ImageDraw
d,out=sys.argv[1],sys.argv[2]
fs=sorted(glob.glob(d+'/*_300.jpg'))
ims=[Image.open(f) for f in fs]; w=300; h=max(i.height for i in ims)
cols=8; rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*(h+20)),'white'); D=ImageDraw.Draw(S)
for k,(f,i) in enumerate(zip(fs,ims)):
    x,y=(k%cols)*w,(k//cols)*(h+20); S.paste(i,(x,y+20)); D.text((x+5,y+3),re.search(r'c(\d+)',f).group(1),fill='red')
S.save(out,quality=80)
