"""Stitch BL IIIF (bl.digirati.io) folio images from tiles; server refuses outputs > ~1024 px.
usage: python fetch.py 'f. 74r' SCALE   (SCALE 1 = full 7144 px wide, 2 = half ...)"""
import json, sys, io, urllib.request
from PIL import Image
m = json.load(open('manifest.json'))
lab, sc = sys.argv[1], int(sys.argv[2])
c = next(c for c in m['items'] if c['label']['en'][0] == lab)
svc = c['items'][0]['items'][0]['body']['service'][0]
sid, W, H = svc['@id'], svc['width'], svc['height']
step = 1024 * sc
out = Image.new('RGB', ((W + sc - 1) // sc, (H + sc - 1) // sc))
for y in range(0, H, step):
    for x in range(0, W, step):
        w, h = min(step, W - x), min(step, H - y)
        url = f"{sid}/{x},{y},{w},{h}/{max(1, w // sc)},/0/default.jpg"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        for t in range(4):
            try:
                im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=120).read())); break
            except Exception as e:
                print('retry', url, e)
        out.paste(im.convert('RGB'), (x // sc, y // sc))
fn = 'img/' + lab.replace('. ', '') + f'_s{sc}.jpg'
out.save(fn, quality=92); print(fn, out.size)
