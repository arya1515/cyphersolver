"""Tile thumbnails into labelled contact sheets for reading foliation and spotting cipher pages.

usage: python montage.py VOL FIRST LAST [COLS] [OUT]   (thumbnails from img/th<VOL>/cNNN.jpg)
"""
import os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
vol, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
out = sys.argv[5] if len(sys.argv) > 5 else os.path.join(HERE, "img", f"sheet{vol}_{first:03d}_{last:03d}.jpg")
src = os.path.join(HERE, "img", f"th{vol}")
tiles = []
for i in range(first, last + 1):
    fn = os.path.join(src, f"c{i:03d}.jpg")
    if os.path.exists(fn):
        im = Image.open(fn).convert("RGB")
        tiles.append((i, im))
if not tiles:
    sys.exit("no thumbnails")
w = max(im.width for _, im in tiles)
h = max(im.height for _, im in tiles)
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * (h + 24)), "white")
d = ImageDraw.Draw(sheet)
for k, (i, im) in enumerate(tiles):
    x, y = (k % cols) * w, (k // cols) * (h + 24)
    sheet.paste(im, (x, y + 24))
    d.rectangle([x, y, x + 70, y + 22], fill="black")
    d.text((x + 4, y + 4), f"c{i}", fill="white")
sheet.save(out, quality=80)
print(out, sheet.size, len(tiles))
