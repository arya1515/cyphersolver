# usage: python cal/strip113.py out.jpg x,y x,y ...  (centres, 130x170 boxes) -> horizontal strip, 3x
import sys
from PIL import Image
im=Image.open('img/c234.jpg') if not sys.argv[1].startswith('v') else Image.open('img/c235.jpg')
out=sys.argv[1][1:] if sys.argv[1].startswith('v') else sys.argv[1]
pts=[tuple(map(int,a.split(','))) for a in sys.argv[2:]]
W,H=150,190
strip=Image.new('L',(W*len(pts),H),255)
for i,(x,y) in enumerate(pts):
    strip.paste(im.crop((x-W//2,y-H//2-20,x+W//2,y+H//2-20)).convert('L'),(i*W,0))
strip=strip.resize((strip.width*3,strip.height*3),Image.LANCZOS)
strip.save('cal/crops/'+out,quality=92)
