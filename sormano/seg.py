# -*- coding: utf-8 -*-
"""Segment a manuscript line into glyph boxes by column-ink valleys."""
import sys, numpy as np
from PIL import Image

def binarize(arr):
    # Otsu on the crop
    hist, _ = np.histogram(arr, bins=256, range=(0,256))
    tot = arr.size
    sum_all = np.dot(np.arange(256), hist)
    sumB = 0.0; wB = 0.0; best = 0.0; thr = 128
    for t in range(256):
        wB += hist[t]
        if wB == 0: continue
        wF = tot - wB
        if wF == 0: break
        sumB += t*hist[t]
        mB = sumB/wB; mF = (sum_all - sumB)/wF
        v = wB*wF*(mB-mF)**2
        if v > best: best = v; thr = t
    return arr < thr, thr

def line_boxes(path, x0, x1, y0, y1, pad=6, minw=8, gapmax=3):
    im = Image.open(path).convert('L')
    a = np.asarray(im.crop((x0, y0-pad, x1, y1+pad)), dtype=np.uint8)
    bw, thr = binarize(a)
    col = bw.sum(axis=0)
    on = col > 0
    boxes = []
    i = 0; n = len(on)
    while i < n:
        if on[i]:
            j = i
            gap = 0
            while j < n:
                if on[j]:
                    gap = 0; j += 1
                else:
                    gap += 1
                    if gap > gapmax: break
                    j += 1
            end = j-gap
            boxes.append((i, end))
            i = j
        else:
            i += 1
    return a, bw, boxes, thr

if __name__ == '__main__':
    p = sys.argv[1]; x0,x1,y0,y1 = map(int, sys.argv[2:6])
    a, bw, boxes, thr = line_boxes(p,x0,x1,y0,y1)
    print('thr',thr,'nboxes',len(boxes))
    print([ (b-aa) for aa,b in boxes ])
