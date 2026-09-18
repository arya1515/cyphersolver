from PIL import Image
import numpy as np
im=Image.open('soglia-cryptogram.png').convert('L')
a=np.array(im)
x0,x1=150,1100
prof=(a[:,x0:x1]<120).sum(1)
# find text line bands
on=prof>15
bands=[];s=None
for y in range(950,2000):
    if on[y] and s is None: s=y
    if not on[y] and s is not None:
        if y-s>6: bands.append((s,y))
        s=None
print(bands)
cols=(a[1000:1960]<120).sum(0)
xs=np.where(cols>5)[0]; print(xs.min(),xs.max())
