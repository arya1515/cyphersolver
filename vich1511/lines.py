"""Find text lines on a PARES page image and write upscaled strips, 3 lines per strip."""
import numpy as np, sys, os
from PIL import Image, ImageOps, ImageDraw
def peaks(a, pitch, x0, x1, y0, y1):
    ink = (a[y0:y1, x0:x1] < 120).sum(1).astype(float)
    k = np.convolve(ink, np.ones(7)/7, 'same'); med = np.median(k[k > 0])
    out = []
    for i in range(len(k)):
        lo, hi = max(0, i-pitch//2), min(len(k), i+pitch//2)
        if k[i] == k[lo:hi].max() and k[i] > 0.4*med and (not out or i-out[-1] > pitch*0.6): out.append(i)
    return [p+y0 for p in out]
def run(fn, tag, y0=150, y1=None, pitch=32, per=3, s=2.0, X0=85):
    im = ImageOps.autocontrast(Image.open(fn).convert('L'), cutoff=1); a = np.asarray(im)
    W, H = im.size; y1 = y1 or H-80
    P = peaks(a, pitch, X0+40, W-60, y0, y1)
    os.makedirs('lines', exist_ok=True)
    for n in range(0, len(P), per):
        grp = P[n:n+per]
        c = im.crop((X0, grp[0]-pitch//2-4, W-15, grp[-1]+pitch//2+4))
        c = c.resize((int(c.width*s), int(c.height*s)), Image.LANCZOS)
        d = ImageDraw.Draw(c)
        for j, p in enumerate(grp): d.text((2, int((p-(grp[0]-pitch//2-4))*s)-8), str(n+j+1), fill=0)
        c.save(f'lines/{tag}_{n//per:02d}.png')
    print(tag, len(P), P)
if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], *[int(x) for x in sys.argv[3:]])
