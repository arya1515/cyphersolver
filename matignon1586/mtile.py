"""Tile a block line by line, fading everything that is not the target line.

The lines on these leaves interleave, so a tile always shows its neighbours and the eye has to
guess which row to read — which is where the transcription errors came from. Here the rows outside
the target band are lightened, so the line to read is unmistakable while its neighbours stay
visible for context (ascenders and descenders belong to them).
"""
import sys
import numpy as np
from PIL import Image, ImageOps

src, ysfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
ntile = int(sys.argv[4]) if len(sys.argv) > 4 else 5
half = int(sys.argv[5]) if len(sys.argv) > 5 else 46
band = int(sys.argv[6]) if len(sys.argv) > 6 else 88
which = sys.argv[7] if len(sys.argv) > 7 else None

im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
A = np.array(im).astype(np.float32)
ys = [int(v) for v in open(ysfile).read().split(',')]
sel = [int(v)-1 for v in which.split(',')] if which else range(len(ys))
H, W = A.shape
for i in sel:
    y = ys[i]
    t0, t1 = max(0, y-half-half//2), min(H, y+half+half//2)
    sub = A[t0:t1].copy()
    rows = np.arange(t0, t1)
    keep = (rows >= y-band//2) & (rows <= y+band//2)
    fade = np.where(keep, 1.0, 0.0)[:, None]
    sub = sub*fade + (255 - (255-sub)*0.22)*(1-fade)   # neighbours washed out, not removed
    img = Image.fromarray(np.clip(sub, 0, 255).astype(np.uint8))
    for j in range(ntile):
        x0 = W*j//ntile; x1 = min(W, W*(j+1)//ntile + 70)
        t = img.crop((x0, 0, x1, img.height))
        sc = 1900/t.width
        t = t.resize((int(t.width*sc), int(t.height*sc)), Image.LANCZOS)
        t.save(f'{out}_{i+1:02d}_{j}.png')
print('tiled lines', len(list(sel)))
