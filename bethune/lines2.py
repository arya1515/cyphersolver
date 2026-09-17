"""lines2.py <canvas> <x0> <y0> <x1> <y1> [--thumb out.jpg]
Detect text lines in a fractional box of full/cNNN.jpg and print their index and y-range (fractions of
the page), optionally writing a numbered thumbnail so the cipher lines can be picked out by eye."""
import sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw
sys.path.insert(0, 'bethune')
from seg import find_lines

c = int(sys.argv[1]); x0f, y0f, x1f, y1f = [float(v) for v in sys.argv[2:6]]
im = Image.open('bethune/full/c%03d.jpg' % c).convert('L')
W, H = im.size
box = (int(W*x0f), int(H*y0f), int(W*x1f), int(H*y1f))
reg = ImageOps.autocontrast(im.crop(box), cutoff=1)
arr = np.asarray(reg, dtype=np.uint8)
peaks, period = find_lines(arr)
print('period', period, 'lines', len(peaks))
for n, pk in enumerate(peaks, 1):
    ya, yb = pk-int(period*0.62), pk+int(period*0.62)
    print('%2d  centre %5d  y %.4f - %.4f' % (n, pk, (box[1]+ya)/H, (box[1]+yb)/H))
if '--thumb' in sys.argv:
    out = sys.argv[sys.argv.index('--thumb')+1]
    th = reg.convert('RGB')
    d = ImageDraw.Draw(th)
    for n, pk in enumerate(peaks, 1):
        d.line([(0, pk), (th.width, pk)], fill=(255, 0, 0), width=3)
        d.text((5, pk-30), str(n), fill=(0, 0, 255))
    sc = 1400.0/max(th.size)
    th = th.resize((int(th.width*sc), int(th.height*sc)), Image.LANCZOS)
    th.save(out, quality=92); print('thumb', out, th.size)
