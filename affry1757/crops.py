import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
f,rot,tag=sys.argv[1],int(sys.argv[2]),sys.argv[3]
n=int(sys.argv[4]) if len(sys.argv)>4 else 4
im=Image.open(f).convert('L').rotate(rot,expand=True)
w,h=im.size
for k in range(n):
    y0=max(0,k*h//n-60);y1=min(h,(k+1)*h//n+20)
    im.crop((0,y0,w,y1)).resize((w//2,(y1-y0)//2)).save(f'sm/{tag}_{k}.jpg',quality=85)
print(w,h)
