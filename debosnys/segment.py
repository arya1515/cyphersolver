"""Segment the monographe verse into glyph images by vertical ink gaps, and make numbered contact sheets."""
import json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# (image, x0, x1, y_center) per line; y windows chosen from the page layout
LINES = [('c4a.png', 295, 960, c) for c in [405, 478, 550, 625, 700, 775, 850, 925, 1000, 1078, 1152, 1230, 1300, 1378, 1450]] + \
        [('c4b.png', 340, 900, c) for c in [55, 125, 200, 275, 350]]


def ink(a, thr):
    return a < thr


def segment(img, x0, x1, yc, thr=120, gap=4, minw=3):
    a = np.array(Image.open(img).convert('L')).astype(int)
    win = a[yc - 38: yc + 34, x0:x1]
    m = ink(win, thr)
    col = m.sum(axis=0)
    runs, s = [], None
    for x, v in enumerate(col):
        if v > 0 and s is None: s = x
        if v == 0 and s is not None:
            runs.append([s, x]); s = None
    if s is not None: runs.append([s, len(col)])
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < gap: merged[-1][1] = r[1]
        else: merged.append(r)
    boxes = []
    for sx, ex in merged:
        sub = m[:, sx:ex]
        rows = np.where(sub.sum(axis=1) > 0)[0]
        if ex - sx < minw and len(rows) < 4: continue
        boxes.append((x0 + sx, yc - 38 + rows[0], x0 + ex, yc - 38 + rows[-1] + 1, int(sub.sum())))
    return boxes


def sheet(li, img, boxes, scale=3):
    im = Image.open(img).convert('L')
    tiles = []
    for k, (a, b, c, d, n) in enumerate(boxes):
        t = im.crop((a - 2, b - 2, c + 2, d + 2))
        t = t.resize((max(1, t.width * scale), max(1, t.height * scale)), Image.LANCZOS)
        tiles.append(t)
    W = sum(t.width + 24 for t in tiles) + 20; H = max(t.height for t in tiles) + 40
    out = Image.new('L', (W, H), 255); dr = ImageDraw.Draw(out); x = 10
    for k, t in enumerate(tiles):
        out.paste(t, (x, 30)); dr.text((x, 5), str(k), fill=0); x += t.width + 24
    out.save('glyphs/line%02d.png' % li)


if __name__ == '__main__':
    allb = {}
    for li, (img, x0, x1, yc) in enumerate(LINES, 1):
        b = segment(img, x0, x1, yc)
        allb[li] = b
        sheet(li, img, b)
        print(li, len(b), [bx[4] for bx in b])
    json.dump({k: [list(map(int, x)) for x in v] for k, v in allb.items()}, open('glyphs/boxes.json', 'w'))
