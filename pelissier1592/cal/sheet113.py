from PIL import Image, ImageDraw
import glob, os, sys
fs=sorted(glob.glob('cal/atlas/*_113*.png'))
a,b=int(sys.argv[1]),int(sys.argv[2]); fs=fs[a:b]
W,H=150,210; cols=8; rows=(len(fs)+cols-1)//cols
s=Image.new('L',(W*cols,H*rows),255); d=ImageDraw.Draw(s)
for i,f in enumerate(fs):
    s.paste(Image.open(f),((i%cols)*W,(i//cols)*H)); d.text(((i%cols)*W+3,(i//cols)*H+192),str(a+i)+' '+os.path.basename(f)[:-8],fill=0)
s.save(f'cal/crops/sheet_{a}.png')
