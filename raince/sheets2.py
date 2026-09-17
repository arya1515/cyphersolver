"""Tight-crop cluster contact sheets: one row per cluster, glyphs cropped to bbox."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
d = json.load(open(sys.argv[1] if len(sys.argv)>1 else 'raince_tokens.json'))
OUT = sys.argv[2] if len(sys.argv)>2 else 'img/t'
regs = d['regions']; toks = d['tokens']
imgs = {n: Image.open(r['img']).convert('L') for n, r in regs.items()}
CELL = 150; NCOL = 12; PER = 8
cls = sorted({t['cl'] for t in toks})
font = ImageFont.truetype('arialbd.ttf', 26)
for s in range(0, len(cls), PER):
    grp = cls[s:s+PER]
    sheet = Image.new('L', (NCOL*CELL+90, len(grp)*CELL), 255)
    dr = ImageDraw.Draw(sheet)
    for i, c in enumerate(grp):
        ts = [t for t in toks if t['cl'] == c]
        ts = ts[::max(1, len(ts)//NCOL)][:NCOL]
        for j, t in enumerate(ts):
            r = regs[t['page']]
            x0 = r['x0']+t['x0']-6; x1 = r['x0']+t['x1']+6
            y0 = r['y0']+t['y0']-6; y1 = r['y0']+t['y1']+6
            p = imgs[t['page']].crop((int(x0), int(y0), int(x1), int(y1)))
            p.thumbnail((CELL-8, CELL-8), Image.LANCZOS)
            sheet.paste(p, (90+j*CELL+(CELL-p.width)//2, i*CELL+(CELL-p.height)//2))
        dr.text((6, i*CELL+CELL//2-14), f'{c:02d}/{len([t for t in toks if t["cl"]==c])}', fill=0, font=font)
        dr.line([(0,i*CELL),(sheet.width,i*CELL)], fill=170)
    sheet.save(f'{OUT}_sheet_{s//PER:02d}.png')
print('sheets', (len(cls)+PER-1)//PER)
