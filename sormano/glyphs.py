# -*- coding: utf-8 -*-
"""Segment manuscript lines into glyph images and build labelled montages."""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw

def otsu(arr):
    hist, _ = np.histogram(arr, bins=256, range=(0,256))
    tot = arr.size; sum_all = np.dot(np.arange(256), hist)
    sumB = 0.0; wB = 0.0; best = -1.0; thr = 128
    for t in range(256):
        wB += hist[t]
        if wB == 0: continue
        wF = tot - wB
        if wF == 0: break
        sumB += t*hist[t]
        mB = sumB/wB; mF = (sum_all - sumB)/wF
        v = wB*wF*(mB-mF)**2
        if v > best: best = v; thr = t
    return thr

def split_wide(col, a, b, target=44, lo=58):
    """Recursively split box [a,b) at low-ink minima."""
    w = b-a
    if w <= lo: return [(a,b)]
    k = max(1, int(round(w/float(target))))
    if k <= 1: return [(a,b)]
    # candidate cut points: interior minima
    out = []
    seglen = w/float(k)
    cuts = []
    for i in range(1, k):
        c = a + int(round(i*seglen))
        lo_i = max(a+12, c-14); hi_i = min(b-12, c+14)
        if hi_i <= lo_i: cuts.append(c); continue
        cuts.append(lo_i + int(np.argmin(col[lo_i:hi_i])))
    pts = [a]+sorted(set(cuts))+[b]
    for i in range(len(pts)-1):
        if pts[i+1]-pts[i] >= 10: out.append((pts[i], pts[i+1]))
    return out

def line_glyphs(im, x0, x1, y0, y1, pad=8, gapmax=3, target=44):
    a = np.asarray(im.crop((x0, y0-pad, x1, y1+pad)), dtype=np.uint8)
    thr = otsu(a)
    bw = a < thr
    col = bw.sum(axis=0)
    on = col > 0
    boxes = []; i = 0; n = len(on)
    while i < n:
        if on[i]:
            j = i; gap = 0
            while j < n:
                if on[j]: gap = 0; j += 1
                else:
                    gap += 1
                    if gap > gapmax: break
                    j += 1
            end = j-gap
            if end-i >= 8: boxes.append((i, end))
            i = j
        else: i += 1
    out = []
    for (u,v) in boxes:
        out.extend(split_wide(col, u, v, target))
    return a, bw, out

def montage(im, page, spans, out, cols=10, cell=190, label=True):
    """spans: list of (x0,y0,x1,y1) in page coords."""
    rows = (len(spans)+cols-1)//cols
    canvas = Image.new('L', (cols*cell, rows*cell), 245)
    d = ImageDraw.Draw(canvas)
    for idx, (bx0,by0,bx1,by1) in enumerate(spans):
        g = im.crop((bx0,by0,bx1,by1))
        w,h = g.size
        s = min((cell-26)/float(w), (cell-26)/float(h))
        g = g.resize((max(1,int(w*s)), max(1,int(h*s))), Image.LANCZOS)
        r, c = idx//cols, idx%cols
        px = c*cell + (cell-g.size[0])//2
        py = r*cell + 20 + (cell-20-g.size[1])//2
        canvas.paste(g, (px,py))
        if label: d.text((c*cell+4, r*cell+4), str(idx), fill=0)
        d.rectangle([c*cell, r*cell, c*cell+cell-1, r*cell+cell-1], outline=200)
    canvas.save(out)
    print(out, canvas.size, len(spans))
