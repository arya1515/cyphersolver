import sys
from PIL import Image
c,y0,y1=map(int,sys.argv[1:4]); im=Image.open(f'img3983/c{c:04d}_full_w2400.jpg'); w=im.width
im.crop((450,y0,1450,y1)).resize((2000,2*(y1-y0))).save('zl.png'); im.crop((1350,y0,2400,y1)).resize((2100,2*(y1-y0))).save('zr.png')
