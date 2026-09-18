# -*- coding: utf-8 -*-
"""Magnified stacked strips for a range of lines.

python mstrip.py SPDIR TAG L0 L1 OUT.png [nseg] [up] [dn] [cap]
Each line is cut into nseg overlapping segments stacked top to bottom;
a darker rule separates one line from the next.
"""
import sys, os, json
from PIL import Image, ImageDraw

def build(SP, tag, l0, l1, out, nseg=3, up=74, dn=74, cap=1560, over=45):
    D = json.load(open(os.path.join(SP, 'inv.json')))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    im = Image.open(pagemap[tag]).convert('L')
    rows = []
    marks = []
    for ln in range(l0, l1+1):
        rs = sorted([r for r in D['recs'] if r['page'] == tag and r['line'] == ln],
                    key=lambda r: r['x0'])
        if not rs: continue
        cy = sorted(r['cy'] for r in rs)[len(rs)//2]
        x0 = min(r['x0'] for r in rs) - 18; x1 = max(r['x1'] for r in rs) + 18
        band = im.crop((x0, cy-up, x1, cy+dn))
        W, H = band.size
        seg = (W + nseg - 1)//nseg
        marks.append(len(rows))
        for i in range(nseg):
            rows.append((ln, i, band.crop((i*seg, 0, min(W, i*seg+seg+over), H))))
    if not rows: print('no lines'); return
    cw = max(t.size[0] for _, _, t in rows)
    ch = max(t.size[1] for _, _, t in rows)
    gap = 8
    canvas = Image.new('L', (cw+46, len(rows)*(ch+gap)), 235)
    d = ImageDraw.Draw(canvas)
    for i, (ln, si, t) in enumerate(rows):
        y = i*(ch+gap)
        canvas.paste(t, (46, y))
        d.text((4, y+ch//2-4), '%d%s' % (ln, 'abcdef'[si]), fill=0)
        if i in marks:
            d.line([0, y-gap//2, canvas.size[0], y-gap//2], fill=90, width=3)
    s = min(cap/float(canvas.size[0]), cap/float(canvas.size[1]))
    canvas = canvas.resize((int(canvas.size[0]*s), int(canvas.size[1]*s)), Image.LANCZOS)
    canvas.save(out)
    print('%s  %s L%d-%d  %dx%d  scale=%.2f' % (out, tag, l0, l1, canvas.size[0], canvas.size[1], s))

if __name__ == '__main__':
    a = sys.argv
    build(a[1], a[2], int(a[3]), int(a[4]), a[5],
          int(a[6]) if len(a) > 6 else 3,
          int(a[7]) if len(a) > 7 else 74,
          int(a[8]) if len(a) > 8 else 74,
          int(a[9]) if len(a) > 9 else 1560)
