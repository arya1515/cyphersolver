# -*- coding: utf-8 -*-
"""Segment a page into glyphs, cluster them, and emit montages for labelling."""
import sys, os, json, math
import numpy as np
from PIL import Image, ImageDraw

# ---------- binarisation ----------
def otsu(arr):
    hist, _ = np.histogram(arr, bins=256, range=(0, 256))
    tot = arr.size; sum_all = np.dot(np.arange(256), hist)
    sumB = 0.0; wB = 0.0; best = -1.0; thr = 128
    for t in range(256):
        wB += hist[t]
        if wB == 0: continue
        wF = tot - wB
        if wF == 0: break
        sumB += t * hist[t]
        mB = sumB / wB; mF = (sum_all - sumB) / wF
        v = wB * wF * (mB - mF) ** 2
        if v > best: best = v; thr = t
    return thr

# ---------- line bands ----------
def line_bands(page, x0, x1, y0, y1, pitch=122, frac=0.10):
    im = Image.open(page).convert('L')
    a = np.asarray(im.crop((x0, y0, x1, y1)), dtype=np.uint8)
    thr = otsu(a)
    bw = a < thr
    ink = bw.sum(axis=1).astype(float)
    k = np.ones(9) / 9.0
    s = np.convolve(ink, k, mode='same')
    on = s > s.max() * frac
    bands = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            if j - i > 18: bands.append([y0 + i, y0 + j])
            i = j
        else: i += 1
    # split bands that clearly hold more than one line
    out = []
    for a_, b_ in bands:
        h = b_ - a_
        n = max(1, int(round(h / float(pitch))))
        if n == 1: out.append((a_, b_))
        else:
            step = h / float(n)
            for q in range(n):
                out.append((int(a_ + q * step), int(a_ + (q + 1) * step)))
    return out

# ---------- glyph boxes ----------
def split_wide(col, a, b, target=44, lo=60):
    w = b - a
    if w <= lo: return [(a, b)]
    k = max(1, int(round(w / float(target))))
    if k <= 1: return [(a, b)]
    seglen = w / float(k); cuts = []
    for i in range(1, k):
        c = a + int(round(i * seglen))
        lo_i = max(a + 12, c - 15); hi_i = min(b - 12, c + 15)
        if hi_i <= lo_i: cuts.append(c)
        else: cuts.append(lo_i + int(np.argmin(col[lo_i:hi_i])))
    pts = [a] + sorted(set(cuts)) + [b]
    return [(pts[i], pts[i + 1]) for i in range(len(pts) - 1) if pts[i + 1] - pts[i] >= 10]

def line_glyphs(im, x0, x1, y0, y1, pad=10, gapmax=3, target=44):
    a = np.asarray(im.crop((x0, y0 - pad, x1, y1 + pad)), dtype=np.uint8)
    thr = otsu(a); bw = a < thr
    col = bw.sum(axis=0); on = col > 0
    raw = []; i = 0; n = len(on)
    while i < n:
        if on[i]:
            j = i; gap = 0
            while j < n:
                if on[j]: gap = 0; j += 1
                else:
                    gap += 1
                    if gap > gapmax: break
                    j += 1
            end = j - gap
            if end - i >= 8: raw.append((i, end))
            i = j
        else: i += 1
    out = []
    for (u, v) in raw:
        srcw = v - u
        for (p, q) in split_wide(col, u, v, target):
            out.append((p, q, srcw))
    return bw, out

# ---------- features ----------
FW, FH = 20, 28
def feat(bw, u, v):
    g = bw[:, u:v]
    H, W = g.size and g.shape
    img = Image.fromarray((g * 255).astype(np.uint8))
    img = img.resize((FW, FH), Image.BILINEAR)
    f = np.asarray(img, dtype=np.float32) / 255.0
    return f.ravel(), float(v - u)

if __name__ == '__main__':
    pass
