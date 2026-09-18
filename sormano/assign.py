# -*- coding: utf-8 -*-
"""Classify glyphs of a new page side with the saved 700-cluster model."""
import sys, json, os
import numpy as np
from PIL import Image
from extract import do_page
from cluster import build_features

def main(sp, page, tag, x0, x1, y0, y1, out):
    recs = []
    bands = do_page(page, tag, x0, x1, y0, y1, 122, recs)
    X, thr, keep = build_features(recs, {tag: page})
    P = np.load(sp+'/P.npy'); mean = np.load(sp+'/mean.npy'); C = np.load(sp+'/C.npy')
    Z = ((X - mean) @ P).astype(np.float32)
    ks = set(keep.tolist())
    for i, r in enumerate(recs):
        if i not in ks: r['c'] = -1; r['d'] = 0.0; continue
        d = ((C - Z[i])**2).sum(axis=1)
        j = int(d.argmin()); r['c'] = j; r['d'] = float(np.sqrt(d[j]))
    json.dump(dict(recs=recs, bands={tag: bands}), open(out, 'w'))
    print(tag, 'lines', len(bands), 'glyphs', len(recs))

if __name__ == '__main__':
    a = sys.argv
    main(a[1], a[2], a[3], int(a[4]), int(a[5]), int(a[6]), int(a[7]), a[8])
