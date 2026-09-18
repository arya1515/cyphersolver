# -*- coding: utf-8 -*-
"""Magnified strips for a line range, cut at word gaps (no overlap, no repeats).

python wstrip.py SPDIR TAG L0 L1 OUT.png [nseg] [cap]
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
from pipeline import otsu

def cuts_at_gaps(col, W, nseg):
    """Pick nseg-1 cut columns near even spacing, preferring the widest ink gap."""
    on = col > 0
    gaps = []          # (start, end) of zero-ink runs
    i = 0
    while i < len(on):
        if not on[i]:
            j = i
            while j < len(on) and not on[j]: j += 1
            gaps.append((i, j))
            i = j
        else: i += 1
    pts = []
    for k in range(1, nseg):
        t = int(round(k*W/float(nseg)))
        best, bs = None, -1
        for (a, b) in gaps:
            if abs((a+b)//2 - t) > W//(2*nseg): continue
            if b-a > bs: bs, best = b-a, (a+b)//2
        pts.append(best if best is not None else t)
    return [0] + pts + [W]

def build(SP, tag, l0, l1, out, nseg=3, cap=1560, up=76, dn=78):
    D = json.load(open(os.path.join(SP, 'inv.json')))
    pagemap = {c['tag']: c['page'] for c in json.load(open('pages.json'))}
    im = Image.open(pagemap[tag]).convert('L')
    rows, marks = [], []
    for ln in range(l0, l1+1):
        rs = sorted([r for r in D['recs'] if r['page'] == tag and r['line'] == ln],
                    key=lambda r: r['x0'])
        if not rs: continue
        cy = sorted(r['cy'] for r in rs)[len(rs)//2]
        x0 = min(r['x0'] for r in rs) - 16; x1 = max(r['x1'] for r in rs) + 16
        band = im.crop((x0, cy-up, x1, cy+dn))
        a = np.asarray(band, dtype=np.uint8)
        col = (a < otsu(a)).sum(axis=0)
        pts = cuts_at_gaps(col, band.size[0], nseg)
        marks.append(len(rows))
        for i in range(len(pts)-1):
            rows.append((ln, i, band.crop((pts[i], 0, pts[i+1], band.size[1]))))
    if not rows: print('no lines'); return
    cw = max(t.size[0] for _, _, t in rows); ch = rows[0][2].size[1]
    gap = 9
    canvas = Image.new('L', (cw+44, len(rows)*(ch+gap)), 235)
    d = ImageDraw.Draw(canvas)
    for i, (ln, si, t) in enumerate(rows):
        y = i*(ch+gap)
        canvas.paste(t, (44, y))
        d.text((4, y+ch//2-4), '%d%s' % (ln, 'abcdefgh'[si]), fill=0)
        if i in marks: d.line([0, y-gap//2, canvas.size[0], y-gap//2], fill=80, width=3)
    s = min(cap/float(canvas.size[0]), cap/float(canvas.size[1]))
    canvas = canvas.resize((int(canvas.size[0]*s), int(canvas.size[1]*s)), Image.LANCZOS)
    canvas.save(out)
    print('%s  %s L%d-%d  scale=%.2f  %dx%d' % (out, tag, l0, l1, s, canvas.size[0], canvas.size[1]))

if __name__ == '__main__':
    a = sys.argv
    build(a[1], a[2], int(a[3]), int(a[4]), a[5],
          int(a[6]) if len(a) > 6 else 3,
          int(a[7]) if len(a) > 7 else 1560)
