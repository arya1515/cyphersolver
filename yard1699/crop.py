"""crop.py oid page x0 y0 x1 y1 [scale]  -- coords in 1/4-thumbnail units; writes img/c/<oid>_p<page>_<y0>.jpg"""
import sys, os
from PIL import Image
oid,page=sys.argv[1],sys.argv[2]
x0,y0,x1,y1=[int(v)*4 for v in sys.argv[3:7]]
sc=float(sys.argv[7]) if len(sys.argv)>7 else 0.6
os.makedirs('img/c',exist_ok=True)
im=Image.open(f'img/{oid}_p{page}.jpg').convert('L').crop((x0,y0,x1,y1))
im=im.resize((int(im.size[0]*sc),int(im.size[1]*sc)))
out=f'img/c/{oid}_p{page}_{y0//4}.jpg'; im.save(out); print(out, im.size)
