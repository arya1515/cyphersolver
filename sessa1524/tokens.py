"""Segment a cipher line strip into tokens (ink runs separated by horizontal gaps) and build a numbered contact sheet.
usage: python tokens.py <image> <x0> <y0> <x1> <y1> <out.png> [gap_px] [thresh]
coordinates in original-image pixels."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def main():
    img, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
    gap = int(sys.argv[7]) if len(sys.argv) > 7 else 6
    thr = int(sys.argv[8]) if len(sys.argv) > 8 else 120
    im = Image.open(img).convert('L').crop((x0, y0, x1, y1))
    a = np.array(im)
    ink = a < thr
    h=ink.shape[0]
    core = ink[int(h*0.22):int(h*0.82), :]
    col = core.sum(axis=0)
    # runs of columns with ink
    runs = []
    inrun = False
    for i, v in enumerate(col):
        if v > 0 and not inrun:
            st = i; inrun = True
        elif v == 0 and inrun:
            inrun = False; runs.append([st, i])
    if inrun:
        runs.append([st, len(col)])
    # merge runs separated by small gaps
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= gap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    merged = [r for r in merged if r[1] - r[0] >= 4]
    H = 150
    tiles = []
    for (s, e) in merged:
        sub = ink[:, s:e]
        rows = np.where(sub.sum(axis=1) > 0)[0]
        if len(rows) == 0:
            continue
        t = im.crop((max(0, s - 3), max(0, rows[0] - 4), min(im.width, e + 3), min(im.height, rows[-1] + 5)))
        sc = H / t.height
        t = t.resize((max(8, int(t.width * sc)), H), Image.LANCZOS)
        tiles.append(t)
    import os
    tdir = out[:-4] + '_tiles'
    os.makedirs(tdir, exist_ok=True)
    for i, t in enumerate(tiles):
        t.save(os.path.join(tdir, f'{i:02d}.png'))
    W = sum(t.width + 26 for t in tiles) + 20
    sheet = Image.new('L', (W, H + 40), 255)
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('arial.ttf', 22)
    except Exception:
        font = ImageFont.load_default()
    x = 10
    for i, t in enumerate(tiles):
        sheet.paste(t, (x, 30))
        d.text((x, 2), str(i), fill=0, font=font)
        d.line((x - 8, 30, x - 8, H + 30), fill=180)
        x += t.width + 26
    sheet.save(out)
    print(out, len(tiles), 'tokens', [e - s for s, e in merged])

if __name__ == '__main__':
    main()
