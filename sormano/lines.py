# -*- coding: utf-8 -*-
"""Find text line bands in a Gallica page crop by horizontal ink profile."""
import sys, numpy as np
from PIL import Image

def profile(path, x0, x1, y0, y1, thresh=None):
    im = Image.open(path).convert('L')
    a = np.asarray(im.crop((x0, y0, x1, y1)), dtype=np.float32)
    # local background: per-row median of a heavily blurred version
    bg = np.median(a)
    if thresh is None:
        thresh = bg - 35
    ink = (a < thresh).sum(axis=1)
    return ink

if __name__ == '__main__':
    p, x0, x1, y0, y1 = sys.argv[1], *map(int, sys.argv[2:6])
    ink = profile(p, x0, x1, y0, y1)
    # smooth
    k = np.ones(9)/9.0
    s = np.convolve(ink, k, mode='same')
    m = s.max()
    on = s > m*0.12
    bands = []
    i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]:
                j += 1
            if j-i > 15:
                bands.append((y0+i, y0+j))
            i = j
        else:
            i += 1
    for n,(a,b) in enumerate(bands):
        print(n, a, b, b-a)
