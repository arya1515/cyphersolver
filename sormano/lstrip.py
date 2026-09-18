# -*- coding: utf-8 -*-
"""Magnified stacked strip of one manuscript line, by page tag + line index.

python lstrip.py SPDIR TAG LINE OUT.png [nseg] [up] [dn]
"""
import sys, os, json
from collections import defaultdict
from PIL import Image

def strip(SP, tag, line, out, nseg=4, up=72, dn=72, gap=14, cap=1900):
    D = json.load(open(os.path.join(SP, 'inv.json')))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    rs = sorted([r for r in D['recs'] if r['page'] == tag and r['line'] == line],
                key=lambda r: r['x0'])
    if not rs:
        print('no glyphs'); return
    cy = rs[len(rs)//2]['cy']
    x0 = min(r['x0'] for r in rs) - 20; x1 = max(r['x1'] for r in rs) + 20
    im = Image.open(pagemap[tag]).convert('L')
    band = im.crop((x0, cy-up, x1, cy+dn))
    W, H = band.size
    seg = (W + nseg - 1)//nseg
    tiles = [band.crop((i*seg, 0, min(W, i*seg+seg+40), H)) for i in range(nseg)]
    cw = max(t.size[0] for t in tiles)
    canvas = Image.new('L', (cw, nseg*H + (nseg-1)*gap), 235)
    for i, t in enumerate(tiles):
        canvas.paste(t, (0, i*(H+gap)))
    s = min(cap/float(canvas.size[0]), cap/float(canvas.size[1]))
    canvas = canvas.resize((int(canvas.size[0]*s), int(canvas.size[1]*s)), Image.LANCZOS)
    canvas.save(out)
    print('%s %s L%02d  cy=%d x=%d..%d  %dx%d scale=%.2f' %
          (out, tag, line, cy, x0, x1, canvas.size[0], canvas.size[1], s))

if __name__ == '__main__':
    a = sys.argv
    strip(a[1], a[2], int(a[3]), a[4],
          int(a[5]) if len(a) > 5 else 4,
          int(a[6]) if len(a) > 6 else 72,
          int(a[7]) if len(a) > 7 else 72)
