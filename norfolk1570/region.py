"""Fetch a region of a folio at scale 1 by 1024-px tiles. usage: python region.py 'f. 74r' x0 y0 x1 y1 out.jpg"""
import json, sys, io, urllib.request
from PIL import Image
m = json.load(open('manifest.json'))
lab = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); fn = sys.argv[6]
c = next(c for c in m['items'] if c['label']['en'][0] == lab)
sid = c['items'][0]['items'][0]['body']['service'][0]['@id']
out = Image.new('RGB', (x1 - x0, y1 - y0))
for y in range(y0, y1, 1024):
    for x in range(x0, x1, 1024):
        w, h = min(1024, x1 - x), min(1024, y1 - y)
        url = f"{sid}/{x},{y},{w},{h}/{w},/0/default.jpg"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        for t in range(4):
            try:
                im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=120).read())); break
            except Exception as e: print('retry', e)
        out.paste(im.convert('RGB'), (x - x0, y - y0))
out.save(fn, quality=93); print(fn, out.size)
