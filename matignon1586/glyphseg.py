"""Segment a cipher page into individual glyph images, row by row, by cutting at the gaps in each
row's column ink-profile.   python glyphseg.py <flat.png> <lines.txt> <out.npz> [minw] [gap]"""
import sys
import numpy as np
from PIL import Image, ImageOps
src, ysf, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
a = np.array(im).astype(float)
ys = [int(v) for v in open(ysf).read().split(',')]
pitch = (ys[-1]-ys[0])/max(1, len(ys)-1)
MINW = int(sys.argv[4]) if len(sys.argv) > 4 else 7
GAPT = float(sys.argv[5]) if len(sys.argv) > 5 else 0.06
SPLIT = float(sys.argv[6]) if len(sys.argv) > 6 else 1.45   # >=9 disables splitting
H = int(0.95*pitch)
glyphs, rows, xs = [], [], []
for r, y in enumerate(ys):
    y0, y1 = max(0, int(y-0.62*pitch)), min(a.shape[0], int(y+0.40*pitch))
    band = a[y0:y1]
    ink = (band < 118).sum(axis=0).astype(float)
    if ink.max() < 2: continue
    on = ink > GAPT*band.shape[0]
    segs = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            segs.append((i, j)); i = j
        else: i += 1
    # merge slivers into the previous segment, drop the left margin junk
    merged = []
    for s, e in segs:
        if merged and s - merged[-1][1] <= 2: merged[-1] = (merged[-1][0], e)
        elif e - s >= 3: merged.append((s, e))
    # cursive joins leave two or three figures inside one segment; split anything much wider than
    # the row's typical figure at its weakest interior column, recursively.
    if merged:
        wmed = float(np.median([e-s for s, e in merged]))
        queue = list(merged); merged = []
        while queue:
            s, e = queue.pop(0)
            if e - s > SPLIT*wmed and e - s >= 2*MINW:
                lo, hi = s+MINW, e-MINW
                if hi > lo:
                    cut = lo + int(np.argmin(ink[lo:hi]))
                    queue.append((s, cut)); queue.append((cut, e)); continue
            merged.append((s, e))
        merged.sort()
    for s, e in merged:
        if e - s < 4 or e - s > 5*MINW: continue
        sub = band[:, s:e]
        col = (sub < 118)
        if col.sum() < 12: continue
        r0 = np.where(col.any(axis=1))[0]
        if len(r0) < 4: continue
        g = sub[r0.min():r0.max()+1]
        # pad to square before resizing: squashing a wide figure into a box makes it look like a
        # narrow one, which is exactly the confusion that must not be introduced here
        h, w = g.shape
        side = max(h, w)
        pad = np.full((side, side), 255.0)
        pad[(side-h)//2:(side-h)//2+h, (side-w)//2:(side-w)//2+w] = g
        g = np.array(Image.fromarray(pad.astype(np.uint8)).resize((20, 20), Image.LANCZOS), dtype=float)
        g = (g - g.mean())/(g.std()+1e-6)
        glyphs.append(g.ravel()); rows.append(r); xs.append(s)
G = np.array(glyphs)
np.savez(out, G=G, rows=np.array(rows), xs=np.array(xs))
print(f'{len(G)} glyphs over {len(set(rows))} rows  (mean {len(G)/max(1,len(set(rows))):.1f} per row)')
