# -*- coding: utf-8 -*-
"""Stacked, magnified composite of a manuscript line (or half-line).

python strip.py PAGE.jpg X0 X1 Y0 Y1 OUT.png [pad] [nseg]
Chooses nseg to make the composite square, maximising magnification.
"""
import sys, math
from PIL import Image

def build(path, x0, x1, y0, y1, out, pad=8, nseg=None, gap=12, cap=1950):
    im = Image.open(path).convert('L')
    strip = im.crop((x0, max(0, y0-pad), x1, y1+pad))
    W, H = strip.size
    if nseg is None:
        nseg = max(1, int(round(math.sqrt(W/float(H+gap)))))
    seg = (W + nseg - 1)//nseg
    tiles = [strip.crop((i*seg, 0, min(W, i*seg+seg+28), H)) for i in range(nseg)]
    cw = max(t.size[0] for t in tiles)
    canvas = Image.new('L', (cw, nseg*H + (nseg-1)*gap), 240)
    for i, t in enumerate(tiles):
        canvas.paste(t, (0, i*(H+gap)))
    s = min(cap/float(canvas.size[0]), cap/float(canvas.size[1]))
    canvas = canvas.resize((int(canvas.size[0]*s), int(canvas.size[1]*s)), Image.LANCZOS)
    canvas.save(out)
    print('%s  %dx%d  nseg=%d  scale=%.2f' % (out, canvas.size[0], canvas.size[1], nseg, s))

if __name__ == '__main__':
    a = sys.argv
    build(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6],
          int(a[7]) if len(a) > 7 else 8, int(a[8]) if len(a) > 8 else None)
