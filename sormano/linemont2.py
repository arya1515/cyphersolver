# -*- coding: utf-8 -*-
"""Montage of one line's glyphs with index and predicted letter (any recs json)."""
import sys, json
from PIL import Image, ImageDraw
def main(jsonf, page_img, tag, line, out, field='let', cols=12, cell=150):
    D = json.load(open(jsonf))
    im = Image.open(page_img).convert('L')
    rs = sorted([r for r in D['recs'] if r['page'] == tag and r['line'] == int(line)], key=lambda r: r['x0'])
    rows = (len(rs)+cols-1)//cols
    canvas = Image.new('L', (cols*cell, rows*cell), 245); d = ImageDraw.Draw(canvas)
    for i, r in enumerate(rs):
        g = im.crop((r['x0'], r['y0'], r['x1'], r['y1'])); w, h = g.size
        s = min((cell-30)/float(w), (cell-30)/float(h))
        g = g.resize((max(1, int(w*s)), max(1, int(h*s))), Image.LANCZOS)
        rr, cc = i//cols, i % cols
        canvas.paste(g, (cc*cell+(cell-g.size[0])//2, rr*cell+24+(cell-24-g.size[1])//2))
        d.text((cc*cell+4, rr*cell+5), '%d:%s' % (i, r.get(field, '?')), fill=0)
        d.rectangle([cc*cell, rr*cell, cc*cell+cell-1, rr*cell+cell-1], outline=200)
    canvas.save(out); print(out, len(rs))
if __name__ == '__main__':
    main(*sys.argv[1:6], **({'field': sys.argv[6]} if len(sys.argv) > 6 else {}))
