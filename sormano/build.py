# -*- coding: utf-8 -*-
"""Build glyph inventory + clusters for one page side."""
import sys, os, json, pickle
import numpy as np
from PIL import Image, ImageDraw
from pipeline import line_bands, line_glyphs, feat, FW, FH
from scipy.cluster.hierarchy import linkage, fcluster

def run(page, tag, x0, x1, y0, y1, nclust, outdir, pitch=122):
    im = Image.open(page).convert('L')
    bands = line_bands(page, x0, x1, y0, y1, pitch=pitch)
    recs = []; feats = []
    for li, (by0, by1) in enumerate(bands):
        bw, boxes = line_glyphs(im, x0, x1, by0, by1)
        for gi, (u, v, srcw) in enumerate(boxes):
            f, w = feat(bw, u, v)
            feats.append(f)
            recs.append(dict(line=li, idx=gi, x0=x0+u, x1=x0+v,
                             y0=by0-10, y1=by1+10, w=w, srcw=srcw))
    X = np.array(feats)
    print('glyphs', X.shape, 'lines', len(bands))
    Z = linkage(X, method='ward')
    lab = fcluster(Z, t=nclust, criterion='maxclust')
    for r, l in zip(recs, lab): r['c'] = int(l)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, tag + '.json'), 'w') as fh:
        json.dump(dict(bands=bands, recs=recs), fh)
    return im, bands, recs

def cluster_montage(im, recs, outdir, tag, per=22, cell=150, cols=23):
    from collections import defaultdict
    byc = defaultdict(list)
    for r in recs: byc[r['c']].append(r)
    keys = sorted(byc, key=lambda k: -len(byc[k]))
    rows = len(keys)
    canvas = Image.new('L', (cols*cell, rows*cell), 245)
    d = ImageDraw.Draw(canvas)
    order = []
    for ri, k in enumerate(keys):
        order.append((k, len(byc[k])))
        d.text((4, ri*cell+4), 'c%d n=%d' % (k, len(byc[k])), fill=0)
        sel = byc[k][:per]
        for ci, r in enumerate(sel):
            g = im.crop((r['x0'], r['y0'], r['x1'], r['y1']))
            w, h = g.size
            s = min((cell-16)/float(w), (cell-16)/float(h))
            g = g.resize((max(1,int(w*s)), max(1,int(h*s))), Image.LANCZOS)
            px = (ci+1)*cell + (cell-g.size[0])//2
            py = ri*cell + (cell-g.size[1])//2
            if px + g.size[0] < canvas.size[0]:
                canvas.paste(g, (px, py))
        d.line([0, ri*cell, cols*cell, ri*cell], fill=180)
    canvas.save(os.path.join(outdir, tag+'_clusters.png'))
    print('clusters', len(keys), [c for c,_ in order][:10])
    return keys

if __name__ == '__main__':
    page, tag, x0, x1, y0, y1, nclust, outdir = (sys.argv[1], sys.argv[2],
        int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]),
        int(sys.argv[7]), sys.argv[8])
    im, bands, recs = run(page, tag, x0, x1, y0, y1, nclust, outdir)
    cluster_montage(im, recs, outdir, tag)
