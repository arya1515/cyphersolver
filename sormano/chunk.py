# -*- coding: utf-8 -*-
"""Render a run of lines of one page side at a chosen scale, for clear-hand reading.

python chunk.py SPDIR TAG L0 L1 OUT.png [cap]
"""
import sys, os, json
from PIL import Image, ImageDraw

def build(SP, tag, l0, l1, out, cap=1540):
    D = json.load(open(os.path.join(SP, 'inv.json')))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    im = Image.open(pagemap[tag]).convert('L')
    rows = []
    for ln in range(l0, l1+1):
        rs = [r for r in D['recs'] if r['page'] == tag and r['line'] == ln]
        if not rs: continue
        cy = sorted(r['cy'] for r in rs)[len(rs)//2]
        rows.append((ln, cy, min(r['x0'] for r in rs)-16, max(r['x1'] for r in rs)+16))
    if not rows: print('none'); return
    x0 = min(r[2] for r in rows); x1 = max(r[3] for r in rows)
    ch = 150
    canvas = Image.new('L', (x1-x0+60, len(rows)*ch), 235)
    d = ImageDraw.Draw(canvas)
    for i, (ln, cy, a, b) in enumerate(rows):
        canvas.paste(im.crop((x0, cy-72, x1, cy+78)), (60, i*ch))
        d.text((4, i*ch+ch//2-5), str(ln), fill=0)
    s = min(cap/float(canvas.size[0]), 1540.0/canvas.size[1])
    canvas = canvas.resize((int(canvas.size[0]*s), int(canvas.size[1]*s)), Image.LANCZOS)
    canvas.save(out)
    print('%s %s L%d-%d scale=%.2f %dx%d' % (out, tag, l0, l1, s, canvas.size[0], canvas.size[1]))

if __name__ == '__main__':
    a = sys.argv
    build(a[1], a[2], int(a[3]), int(a[4]), a[5], int(a[6]) if len(a) > 6 else 1540)
