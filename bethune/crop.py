"""crop.py <canvas> <x0> <y0> <x1> <y1> <zoom> <out>  — fractional box of full/cNNN.jpg, contrast-boosted."""
import sys, os
from PIL import Image, ImageOps
c, x0, y0, x1, y1, z, out = sys.argv[1], *[float(v) for v in sys.argv[2:7]], sys.argv[7]
im = Image.open(f'bethune/full/c{int(c):03d}.jpg')
W, H = im.size
box = (int(W*x0), int(H*y0), int(W*x1), int(H*y1))
s = im.crop(box).convert('L')
s = ImageOps.autocontrast(s, cutoff=1)
s = s.resize((int(s.width*z), int(s.height*z)), Image.LANCZOS)
s.save(out, quality=94)
print(out, s.size, 'from', box)
