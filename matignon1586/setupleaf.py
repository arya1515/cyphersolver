"""Set up a leaf for token transcription: fetch the page, crop, flatten, find lines by ink peaks,
cut two-tile faded strips.   python setupleaf.py <name> <canvas> <left|right> [x0 y0 x1 y1 as page fractions]"""
import sys, os, urllib.request, subprocess
import numpy as np
from PIL import Image, ImageOps
name, canvas, side = sys.argv[1], int(sys.argv[2]), sys.argv[3]
fr = [float(v) for v in sys.argv[4:8]] if len(sys.argv) > 7 else [0.10, 0.12, 0.96, 0.92]
pct = '0,0,50,100' if side == 'left' else '50,0,50,100'
src = f'hi/{name}.jpg'
if not os.path.exists(src):
    url = f'https://gallica.bnf.fr/iiif/ark:/12148/btv1b9061879d/f{canvas}/pct:{pct}/4400,/0/native.jpg'
    open(src, 'wb').write(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=240).read())
im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
W, H = im.size
im.resize((900, int(H*900/W))).save(f'hi/{name}_sm.png')
blk = im.crop((int(fr[0]*W), int(fr[1]*H), int(fr[2]*W), int(fr[3]*H)))
blk.save(f'hi/{name}blk.png')
subprocess.run([sys.executable, 'flatten.py', f'hi/{name}blk.png', f'hi/{name}flat.png'], capture_output=True)
a = np.array(ImageOps.autocontrast(Image.open(f'hi/{name}flat.png').convert('L'), 1))
ink = np.convolve((a < 110).sum(axis=1).astype(float), np.ones(31)/31, 'same')
rows = np.where(ink > 0.15*ink.max())[0]
ys = []; y = int(rows.min()) if len(rows) else 0
while y < a.shape[0]-40:
    lo, hi = y, min(a.shape[0], y+80)
    pk = lo + int(np.argmax(ink[lo:hi]))
    if ink[pk] > 0.15*ink.max(): ys.append(pk)
    y = pk + 60
d = np.diff(ys); med = float(np.median(d)) if len(d) else 100
out = [ys[0]]
for yy in ys[1:]:
    g = yy - out[-1]
    if g < 0.75*med: continue
    if g > 1.6*med: out.append(out[-1] + g//2)
    out.append(yy)
open(f'{name}_lines.txt', 'w').write(','.join(map(str, out)))
env = dict(os.environ, MT_NOSNAP='1')
subprocess.run([sys.executable, 'mtile.py', f'hi/{name}flat.png', f'{name}_lines.txt', f'hi/{name}T', '2', '44', '84',
                ','.join(str(i) for i in range(1, len(out)+1))], capture_output=True, env=env)
print(f'{name}: {len(out)} lines, pitch ~{med:.0f}; tiles hi/{name}T_NN_0/1.png')
