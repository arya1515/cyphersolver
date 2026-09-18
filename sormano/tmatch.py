# -*- coding: utf-8 -*-
"""Find glyphs most similar to a template record, show them in line context.

python tmatch.py SPDIR TAG LINE IDX OUT.png [n]
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter
from pipeline import otsu
import classify

def norm(im, r, y0, y1, thr):
    g = np.asarray(im.crop((r['x0'], y0, r['x1'], y1)), dtype=np.uint8)
    m = (g < thr).astype(np.float32)
    m = gaussian_filter(m, 1.2)
    v = Image.fromarray((np.clip(m, 0, 1)*255).astype(np.uint8)).resize((18, 26), Image.BILINEAR)
    return np.asarray(v, dtype=np.float32).ravel()/255.0

def main():
    SP, tag, line, idx, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    n = int(sys.argv[6]) if len(sys.argv) > 6 else 12
    recs, X, win = classify.features(SP)
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
    sel = sorted([i for i, r in enumerate(recs) if r['page'] == tag and r['line'] == line],
                 key=lambda i: recs[i]['x0'])
    t = X[sel[idx]]
    d = ((X - t[None, :])**2).sum(axis=1)
    order = np.argsort(d)[:n]
    tiles = []
    for i in order:
        r = recs[i]; im = ims[r['page']]
        x0 = max(0, r['x0']-235); x1 = min(im.size[0], r['x1']+235)
        g = im.crop((x0, r['cy']-82, x1, r['cy']+84)).copy()
        dr = ImageDraw.Draw(g)
        dr.rectangle([r['x0']-x0-2, 3, r['x1']-x0+2, g.size[1]-4], outline=0, width=3)
        tiles.append((r, g))
    cw = max(t.size[0] for _, t in tiles); ch = tiles[0][1].size[1]
    canvas = Image.new('L', (cw, len(tiles)*(ch+7)), 235)
    dd = ImageDraw.Draw(canvas)
    for i, (r, t) in enumerate(tiles):
        canvas.paste(t, (0, i*(ch+7)))
        dd.text((3, i*(ch+7)+3), '%s L%d' % (r['page'][4:], r['line']), fill=0)
    s = min(1500.0/canvas.size[0], 1500.0/canvas.size[1])
    canvas = canvas.resize((int(canvas.size[0]*s), int(canvas.size[1]*s)), Image.LANCZOS)
    canvas.save(out); print(out, canvas.size)

if __name__ == '__main__':
    main()
