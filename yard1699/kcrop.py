"""kcrop.py x0 y0 x1 y1 -- coords in 1/5 thumb of key_r; saves img/k/k_x0_y0.jpg"""
import sys, os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
x0,y0,x1,y1=[int(v)*5 for v in sys.argv[1:5]]
os.makedirs('img/k',exist_ok=True)
im=Image.open('img/key_r.jpg').convert('L').crop((x0,y0,x1,y1))
s=min(1.0, 1900/max(im.size)); im=im.resize((int(im.size[0]*s),int(im.size[1]*s)))
out=f'img/k/k_{x0//5}_{y0//5}.jpg'; im.save(out); print(out, im.size)
