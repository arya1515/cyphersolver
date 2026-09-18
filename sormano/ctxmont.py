# -*- coding: utf-8 -*-
"""Show members of a cluster inside their line context, glyph boxed.

python ctxmont.py SPDIR CLUSTER OUT.png [n] [half]
"""
import sys, os, json
from PIL import Image, ImageDraw

def build(SP, cid, out, n=10, half=230, cap=1520):
    D = json.load(open(os.path.join(SP, 'clustered.json')))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
    rs = [r for r in D['recs'] if r['c'] == cid]
    rs = sorted(rs, key=lambda r: r['d'])[:n]
    tiles = []
    for r in rs:
        im = ims[r['page']]
        x0 = max(0, r['x0']-half); x1 = min(im.size[0], r['x1']+half)
        g = im.crop((x0, r['cy']-80, x1, r['cy']+82)).convert('L').copy()
        d = ImageDraw.Draw(g)
        d.rectangle([r['x0']-x0-2, 4, r['x1']-x0+2, g.size[1]-5], outline=0, width=3)
        tiles.append((r, g))
    cw = max(t.size[0] for _, t in tiles); ch = tiles[0][1].size[1]
    canvas = Image.new('L', (cw, len(tiles)*(ch+8)), 235)
    dd = ImageDraw.Draw(canvas)
    for i, (r, t) in enumerate(tiles):
        canvas.paste(t, (0, i*(ch+8)))
        dd.text((3, i*(ch+8)+3), '%s L%d' % (r['page'][:8], r['line']), fill=0)
    s = min(cap/float(canvas.size[0]), cap/float(canvas.size[1]))
    canvas = canvas.resize((int(canvas.size[0]*s), int(canvas.size[1]*s)), Image.LANCZOS)
    canvas.save(out); print(out, canvas.size, 'n=%d' % len(tiles))

if __name__ == '__main__':
    a = sys.argv
    build(a[1], int(a[2]), a[3], int(a[4]) if len(a) > 4 else 10,
          int(a[5]) if len(a) > 5 else 230)
