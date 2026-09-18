"""Generate per-line crops for hand transcription. One PNG per manuscript line,
split into left/right halves, upscaled 1.6x, using geometry from raince_tokens.json."""
import json, os
from PIL import Image

d = json.load(open('raince_tokens.json'))
os.makedirs('img/bands', exist_ok=True)
imgs = {}
for page, r in d['regions'].items():
    img = r['img']
    if img not in imgs:
        imgs[img] = Image.open(img).convert('L')
    im = imgs[img]
    pitch = r['pitch']
    for k, ly in enumerate(r['lines']):
        y = int(r['y0'] + ly)
        # region x extent: min/max token x on this page
        toks = [t for t in d['tokens'] if t['page'] == page]
        x0 = r['x0'] + min(t['x0'] for t in toks) - 20
        x1 = r['x0'] + max(t['x1'] for t in toks) + 20
        top = int(y - pitch * 0.75); bot = int(y + pitch * 0.45)
        band = im.crop((x0, top, x1, bot))
        w, h = band.size
        half = w // 2
        for side, (a, b) in (('L', (0, half + 60)), ('R', (half - 60, w))):
            c = band.crop((a, 0, b, h))
            c = c.resize((int(c.width * 1.6), int(c.height * 1.6)), Image.LANCZOS)
            c.save(f'img/bands/{page}_{k+1:02d}{side}.png')
print('done', {p: len(r['lines']) for p, r in d['regions'].items()})
