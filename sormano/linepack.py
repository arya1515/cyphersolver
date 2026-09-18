# -*- coding: utf-8 -*-
"""Per-line review sheet: magnified line strip on top, labelled glyph cells below."""
import sys, json, os
from PIL import Image, ImageDraw
from collections import defaultdict

def sheet(im, recs, band, x0, x1, out, field='let2', W=1800, cell=128, cols=14, nseg=3):
    y0, y1 = band
    strip = im.crop((x0, y0-14, x1, y1+14)); sw, sh = strip.size
    seg = (sw+nseg-1)//nseg; tiles = []
    for i in range(nseg):
        t = strip.crop((i*seg, 0, min(sw, i*seg+seg+30), sh))
        s = W/float(seg+30); tiles.append(t.resize((int(t.size[0]*s), int(sh*s)), Image.LANCZOS))
    th = sum(t.size[1] for t in tiles) + 6*nseg
    rs = sorted(recs, key=lambda r: r['x0'])
    rows = (len(rs)+cols-1)//cols
    canvas = Image.new('L', (W, th + rows*cell + 8), 242); d = ImageDraw.Draw(canvas)
    y = 0
    for t in tiles: canvas.paste(t, (0, y)); y += t.size[1]+6
    y += 4
    for i, r in enumerate(rs):
        g = im.crop((r['x0'], r['y0'], r['x1'], r['y1'])); w, h = g.size
        s = min((cell-28)/float(w), (cell-28)/float(h))
        g = g.resize((max(1, int(w*s)), max(1, int(h*s))), Image.LANCZOS)
        rr, cc = i//cols, i % cols
        px, py = cc*cell, y+rr*cell
        canvas.paste(g, (px+(cell-g.size[0])//2, py+22+(cell-22-g.size[1])//2))
        lab = r.get(field, '?'); lab = '.' if lab == '~' else lab
        d.text((px+4, py+4), '%d %s' % (i, lab), fill=0)
        d.rectangle([px, py, px+cell-1, py+cell-1], outline=190)
    canvas.save(out)

if __name__ == '__main__':
    sp, tag, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    lines = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else None
    D = json.load(open(sp+'/knn.json'))
    cfg = {c['tag']: c for c in json.load(open('pages.json'))}[tag]
    im = Image.open(cfg['page']).convert('L')
    byline = defaultdict(list)
    for r in D['recs']:
        if r['page'] == tag: byline[r['line']].append(r)
    bands = D['bands'][tag]
    os.makedirs(outdir, exist_ok=True)
    for li in sorted(byline):
        if lines and li not in lines: continue
        sheet(im, byline[li], bands[li], cfg['x0'], cfg['x1'], '%s/%s_L%02d.png' % (outdir, tag, li))
    print('done', tag)
