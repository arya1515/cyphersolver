# -*- coding: utf-8 -*-
"""Two-line review sheets: for each line, a 2-segment strip then labelled glyph cells."""
import sys, json, os
from PIL import Image, ImageDraw
from collections import defaultdict

def line_block(im, recs, band, x0, x1, field, W=1900, cell=118, cols=16, nseg=2):
    y0, y1 = band
    strip = im.crop((x0, y0-12, x1, y1+12)); sw, sh = strip.size
    seg = (sw+nseg-1)//nseg; tiles = []
    for i in range(nseg):
        t = strip.crop((i*seg, 0, min(sw, i*seg+seg+30), sh))
        s = W/float(seg+30); tiles.append(t.resize((int(t.size[0]*s), int(sh*s)), Image.LANCZOS))
    rs = sorted(recs, key=lambda r: r['x0'])
    rows = (len(rs)+cols-1)//cols
    th = sum(t.size[1] for t in tiles) + 4*nseg
    blk = Image.new('L', (W, th + rows*cell + 6), 242); d = ImageDraw.Draw(blk)
    y = 0
    for t in tiles: blk.paste(t, (0, y)); y += t.size[1]+4
    for i, r in enumerate(rs):
        g = im.crop((r['x0'], r['y0'], r['x1'], r['y1'])); w, h = g.size
        s = min((cell-26)/float(w), (cell-26)/float(h))
        g = g.resize((max(1, int(w*s)), max(1, int(h*s))), Image.LANCZOS)
        rr, cc = i//cols, i % cols; px, py = cc*cell, y+rr*cell
        blk.paste(g, (px+(cell-g.size[0])//2, py+20+(cell-20-g.size[1])//2))
        lab = r.get(field, '?'); lab = '.' if lab == '~' else lab
        d.text((px+3, py+3), '%d %s' % (i, lab), fill=0)
        d.rectangle([px, py, px+cell-1, py+cell-1], outline=190)
    return blk

if __name__ == '__main__':
    sp, tag, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    field = sys.argv[4] if len(sys.argv) > 4 else 'let2'
    D = json.load(open(sp+'/knn.json'))
    cfg = {c['tag']: c for c in json.load(open('pages.json'))}[tag]
    im = Image.open(cfg['page']).convert('L')
    byline = defaultdict(list)
    for r in D['recs']:
        if r['page'] == tag: byline[r['line']].append(r)
    bands = D['bands'][tag]; os.makedirs(outdir, exist_ok=True)
    lines = sorted(byline)
    for k in range(0, len(lines), 2):
        blks = [line_block(im, byline[li], bands[li], cfg['x0'], cfg['x1'], field) for li in lines[k:k+2]]
        H = sum(b.size[1] for b in blks) + 12*(len(blks)-1)
        canvas = Image.new('L', (1900, H), 120); y = 0
        for b in blks: canvas.paste(b, (0, y)); y += b.size[1]+12
        canvas.save('%s/%s_%02d.png' % (outdir, tag, k//2))
    print(tag, 'sheets', (len(lines)+1)//2)
