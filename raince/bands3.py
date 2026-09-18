"""One image per manuscript line: the line cut into 3 overlapping thirds, stacked,
upscaled, with the third index drawn at the left. For hand transcription."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
Z = 2.0
d = json.load(open('raince_tokens.json'))
os.makedirs('img/lines', exist_ok=True)
font = ImageFont.truetype('arialbd.ttf', 30)
imgs = {}
only = sys.argv[1:] or None
for page, r in d['regions'].items():
    if only and page not in only: continue
    if r['img'] not in imgs: imgs[r['img']] = Image.open(r['img']).convert('L')
    im = imgs[r['img']]
    pitch = r['pitch']
    toks = [t for t in d['tokens'] if t['page'] == page]
    x0 = r['x0'] + min(t['x0'] for t in toks) - 25
    x1 = r['x0'] + max(t['x1'] for t in toks) + 25
    W = x1 - x0
    ov = 85
    n = 4
    cuts = [(max(0, i*W//n - ov), min(W, (i+1)*W//n + ov)) for i in range(n)]
    for k, ly in enumerate(r['lines']):
        y = int(r['y0'] + ly)
        top = int(y - pitch*0.72); bot = int(y + pitch*0.46)
        band = im.crop((x0, top, x1, bot))
        parts = []
        for a, b in cuts:
            c = band.crop((a, 0, b, band.height))
            c = c.resize((int(c.width*Z), int(c.height*Z)), Image.LANCZOS)
            parts.append(c)
        w = max(p.width for p in parts); h = parts[0].height
        out = Image.new('L', (w + 44, len(parts)*(h+12)), 255)
        dr = ImageDraw.Draw(out)
        for i, p in enumerate(parts):
            out.paste(p, (44, i*(h+12)))
            dr.text((6, i*(h+12) + h//2 - 16), 'abcd'[i], fill=0, font=font)
            dr.line([(0, i*(h+12)-6), (out.width, i*(h+12)-6)], fill=150)
        out.save(f'img/lines/{page}_{k+1:02d}.png')
    print(page, len(r['lines']), 'W', W, 'out', out.size)
