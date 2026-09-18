# -*- coding: utf-8 -*-
"""Extract glyph boxes from every target page side into one inventory."""
import sys, os, json
import numpy as np
from PIL import Image
from pipeline import otsu, line_bands, split_wide

BAND_UP, BAND_DN = 48, 52          # fixed crop height around line centre

def line_boxes(im, x0, x1, by0, by1, gapmax=3, target=44):
    pad = 12
    a = np.asarray(im.crop((x0, by0-pad, x1, by1+pad)), dtype=np.uint8)
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
            end = j-gap
            if end-i >= 8: raw.append((i, end))
            i = j
        else: i += 1
    out = []
    for (u, v) in raw:
        for (p, q) in split_wide(col, u, v, target):
            out.append((p, q, v-u))
    return out

def line_centre(im, x0, x1, b0, b1):
    """Row of maximum ink density = middle of the x-height band."""
    a = np.asarray(im.crop((x0, b0, x1, b1)), dtype=np.uint8)
    thr = otsu(a); bw = a < thr
    rows = bw.sum(axis=1).astype(float)
    k = np.ones(11)/11.0
    s = np.convolve(rows, k, mode='same')
    return b0 + int(np.argmax(s))

def do_page(page, tag, x0, x1, y0, y1, pitch, recs):
    im = Image.open(page).convert('L')
    bands = line_bands(page, x0, x1, y0, y1, pitch=pitch)
    for li, (b0, b1) in enumerate(bands):
        cy = line_centre(im, x0, x1, b0, b1)
        for gi, (u, v, srcw) in enumerate(line_boxes(im, x0, x1, b0, b1)):
            recs.append(dict(page=tag, line=li, idx=gi,
                             x0=x0+u, x1=x0+v, cy=cy,
                             y0=cy-BAND_UP, y1=cy+BAND_DN,
                             w=v-u, srcw=srcw))
    return bands

if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    recs = []; allb = {}
    for c in cfg:
        b = do_page(c['page'], c['tag'], c['x0'], c['x1'], c['y0'], c['y1'],
                    c.get('pitch', 122), recs)
        allb[c['tag']] = b
        print(c['tag'], 'lines', len(b), 'glyphs so far', len(recs))
    json.dump(dict(recs=recs, bands=allb), open(out, 'w'))
    print('total', len(recs))
