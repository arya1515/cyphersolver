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

# snap each fitted centre to the local ink maximum, so a per-leaf offset never has to be set by
# hand again: the profile peak is the line, whatever the fit said
_ink = (A < (A.mean() - 0.45*A.std())).sum(axis=1).astype(float)
_ink = np.convolve(_ink, np.ones(11)/11, 'same')
_pitch = int(np.median(np.diff(ys))) if len(ys) > 2 else 100
_w = max(10, int(0.38*_pitch))
import os as _os
if _os.environ.get('MT_NOSNAP') != '1':
    ys = [int(max(0, y-_w) + np.argmax(_ink[max(0, y-_w):min(len(_ink), y+_w)])) for y in ys]
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
    _slope = float(_os.environ.get('MT_SLOPE', '0') or 0)
    for j in range(ntile):
        x0 = W*j//ntile; x1 = min(W, W*(j+1)//ntile + 70)
        if _slope:
            dy = int(_slope * ((x0 + x1)/2 - W/2))
            yc = y + dy
            s0, s1 = max(0, yc-half-half//2), min(H, yc+half+half//2)
            sb = A[s0:s1].copy(); rr = np.arange(s0, s1)
            kp = ((rr >= yc-band//2) & (rr <= yc+band//2)).astype(float)[:, None]
            sb = sb*kp + (255-(255-sb)*0.22)*(1-kp)
            t = Image.fromarray(np.clip(sb, 0, 255).astype(np.uint8)).crop((x0, 0, x1, s1-s0))
        else:
            t = img.crop((x0, 0, x1, img.height))
        sc = 1900/t.width
        t = t.resize((int(t.width*sc), int(t.height*sc)), Image.LANCZOS)
        t.save(f'{out}_{i+1:02d}_{j}.png')
print('tiled lines', len(list(sel)))
