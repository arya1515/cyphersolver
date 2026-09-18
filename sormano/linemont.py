# -*- coding: utf-8 -*-
"""Montage of one line's glyphs labelled with cluster id and decoded letter."""
import sys, os, json
from PIL import Image, ImageDraw
import labels

def main(jsonf, page, line, out, cols=11, cell=165):
    D = json.load(open(jsonf))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    im = Image.open(pagemap[page]).convert('L')
    rs = sorted([r for r in D['recs'] if r['page'] == page and r['line'] == int(line)],
                key=lambda r: r['x0'])
    rows = (len(rs)+cols-1)//cols
    canvas = Image.new('L', (cols*cell, rows*cell), 245)
    d = ImageDraw.Draw(canvas)
    for i, r in enumerate(rs):
        g = im.crop((r['x0'], r['y0'], r['x1'], r['y1']))
        w, h = g.size
        s = min((cell-34)/float(w), (cell-34)/float(h))
        g = g.resize((max(1,int(w*s)), max(1,int(h*s))), Image.LANCZOS)
        rr, cc = i//cols, i%cols
        canvas.paste(g, (cc*cell+(cell-g.size[0])//2, rr*cell+26+(cell-26-g.size[1])//2))
        ch = labels.L.get(r['c'], '~')
        d.text((cc*cell+5, rr*cell+6), '%d:%s:%s' % (i, r['c'], ch), fill=0)
        d.rectangle([cc*cell, rr*cell, cc*cell+cell-1, rr*cell+cell-1], outline=200)
    canvas.save(out); print(out, canvas.size, len(rs))

if __name__ == '__main__':
    main(*sys.argv[1:6])
