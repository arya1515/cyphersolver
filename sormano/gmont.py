# -*- coding: utf-8 -*-
"""Numbered montage of glyph boxes for a line range, in reading order.

python gmont.py SPDIR TAG L0 L1 OUT.png [cols] [cell]
Each line starts a fresh row and is tagged with its line number.
"""
import sys, os, json
from PIL import Image, ImageDraw

def build(SP, tag, l0, l1, out, cols=12, cell=124, up=76, dn=76):
    D = json.load(open(os.path.join(SP, 'inv.json')))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    im = Image.open(pagemap[tag]).convert('L')
    cells = []          # (label, image) ; None image = row break marker
    for ln in range(l0, l1+1):
        rs = sorted([r for r in D['recs'] if r['page'] == tag and r['line'] == ln],
                    key=lambda r: r['x0'])
        if not rs: continue
        while len(cells) % cols: cells.append(None)
        for i, r in enumerate(rs):
            cells.append(('%d.%d' % (ln, i),
                          im.crop((r['x0']-7, r['cy']-up, r['x1']+7, r['cy']+dn))))
    rows = (len(cells)+cols-1)//cols
    canvas = Image.new('L', (cols*cell, rows*cell), 245)
    d = ImageDraw.Draw(canvas)
    for i, c in enumerate(cells):
        rr, cc = i//cols, i % cols
        if c is None: continue
        lab, g = c
        w, h = g.size
        s = min((cell-20)/float(w), (cell-20)/float(h))
        g = g.resize((max(1,int(w*s)), max(1,int(h*s))), Image.LANCZOS)
        canvas.paste(g, (cc*cell+(cell-g.size[0])//2, rr*cell+18+(cell-18-g.size[1])//2))
        d.text((cc*cell+3, rr*cell+3), lab, fill=0)
        d.rectangle([cc*cell, rr*cell, cc*cell+cell-1, rr*cell+cell-1], outline=195)
    canvas.save(out)
    print('%s  %s L%d-%d  %d cells  %dx%d' % (out, tag, l0, l1, len(cells), canvas.size[0], canvas.size[1]))

if __name__ == '__main__':
    a = sys.argv
    build(a[1], a[2], int(a[3]), int(a[4]), a[5],
          int(a[6]) if len(a) > 6 else 12,
          int(a[7]) if len(a) > 7 else 124)
