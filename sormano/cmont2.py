# -*- coding: utf-8 -*-
import sys, os, json
from collections import defaultdict
from PIL import Image, ImageDraw

def main(jsonf, outdir, tag, per=11, cell=148, chunk=13):
    D = json.load(open(jsonf))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    ims = {t: Image.open(p).convert('L') for t, p in pagemap.items()}
    byc = defaultdict(list)
    for r in D['recs']:
        if r['c'] >= 0: byc[r['c']].append(r)
    keys = sorted(byc, key=lambda k: -len(byc[k]))
    cols = per + 1
    for ci in range(0, len(keys), chunk):
        part = keys[ci:ci+chunk]
        canvas = Image.new('L', (cols*cell, len(part)*cell), 245)
        d = ImageDraw.Draw(canvas)
        for ri, k in enumerate(part):
            sel = sorted(byc[k], key=lambda r: r['d'])[:per]
            d.text((6, ri*cell+cell//2-6), '%d/%d' % (k, len(byc[k])), fill=0)
            for j, r in enumerate(sel):
                g = ims[r['page']].crop((r['x0'], r['y0'], r['x1'], r['y1']))
                w, h = g.size
                s = min((cell-14)/float(w), (cell-14)/float(h))
                g = g.resize((max(1,int(w*s)), max(1,int(h*s))), Image.LANCZOS)
                canvas.paste(g, ((j+1)*cell + (cell-g.size[0])//2,
                                 ri*cell + (cell-g.size[1])//2))
            d.line([0, ri*cell, cols*cell, ri*cell], fill=170)
        p = os.path.join(outdir, '%s_%02d.png' % (tag, ci//chunk))
        canvas.save(p)
    print('chunks', (len(keys)+chunk-1)//chunk, 'clusters', len(keys))

if __name__ == '__main__':
    main(*sys.argv[1:4])
