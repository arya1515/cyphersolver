"""Cut a downloaded DECODE page image into line strips at 2x for glyph-level reading.

Usage:  python crop_lines.py IMG_R92_I692_P2.jpg [--lines 28] [--scale 2]
Writes  crops/<image>/line_NN.png plus a contact sheet crops/<image>/sheet.png.
Line boundaries come from horizontal ink-density valleys; pass --lines to force a count if the
automatic split is off. Needs Pillow and numpy (both already used elsewhere in the repo).
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))


def find_rows(gray, min_gap=6):
    ink = (255 - gray).astype(np.float64)
    prof = ink.mean(axis=1)
    thr = prof.mean() * 0.6
    on = prof > thr
    rows, start = [], None
    for y, v in enumerate(on):
        if v and start is None:
            start = y
        elif not v and start is not None:
            if y - start >= min_gap:
                rows.append((start, y))
            start = None
    if start is not None:
        rows.append((start, len(on)))
    # merge rows separated by tiny gaps (ascender/descender splits)
    merged = []
    for r in rows:
        if merged and r[0] - merged[-1][1] < min_gap:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(r)
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--lines", type=int, default=0, help="force this many equal bands instead of auto-detect")
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--pad", type=int, default=8)
    a = ap.parse_args()

    im = Image.open(os.path.join(HERE, a.image) if not os.path.isabs(a.image) else a.image)
    im = ImageOps.exif_transpose(im).convert("L")
    g = np.asarray(im)
    h, w = g.shape
    if a.lines:
        step = h / a.lines
        rows = [(int(i * step), int((i + 1) * step)) for i in range(a.lines)]
    else:
        rows = find_rows(g)
    out = os.path.join(HERE, "crops", os.path.splitext(os.path.basename(a.image))[0])
    os.makedirs(out, exist_ok=True)
    strips = []
    for i, (y0, y1) in enumerate(rows):
        y0, y1 = max(0, y0 - a.pad), min(h, y1 + a.pad)
        strip = im.crop((0, y0, w, y1))
        strip = strip.resize((int(w * a.scale), int((y1 - y0) * a.scale)), Image.LANCZOS)
        strip.save(os.path.join(out, "line_%02d.png" % (i + 1)))
        strips.append(strip)
    if strips:
        sw = max(s.width for s in strips)
        sh = sum(s.height + 6 for s in strips)
        sheet = Image.new("L", (sw, sh), 255)
        y = 0
        for s in strips:
            sheet.paste(s, (0, y))
            y += s.height + 6
        sheet.save(os.path.join(out, "sheet.png"))
    print("%s: %d x %d, %d lines -> %s" % (a.image, w, h, len(rows), out))


if __name__ == "__main__":
    main()
