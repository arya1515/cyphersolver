"""Band crops for the glossed regions (f29r lines 1-10, f105r cipher lines 1-12).
Line detection: y-histogram of dark pixels (cipher ink is darker than the gloss)."""
import numpy as np, os
from PIL import Image
from scipy.ndimage import uniform_filter

os.makedirs('img/bands', exist_ok=True)
JOBS = [
    ('../f2984/c16_full.jpg', 'f29rG', 0.585, 0.965, 0.020, 0.245),
    ('../f2984/c54_full.jpg', 'f105rG', 0.545, 0.975, 0.055, 0.360),
]
for img, name, x0f, x1f, y0f, y1f in JOBS:
    im = Image.open(img).convert('L'); W, H = im.size
    x0, x1, y0, y1 = int(W*x0f), int(W*x1f), int(H*y0f), int(H*y1f)
    reg = np.array(im.crop((x0, y0, x1, y1))).astype(float)
    bg = uniform_filter(reg, size=81)
    dark = (reg < bg - 50).sum(axis=1).astype(float)
    sm = np.convolve(dark, np.ones(25)/25, mode='same')
    thr = sm.max() * 0.35
    rows = sm > thr
    lines = []
    i = 0
    while i < len(rows):
        if rows[i]:
            j = i
            while j < len(rows) and rows[j]: j += 1
            if j - i > 20: lines.append((i + j) / 2)
            i = j
        else: i += 1
    # merge close
    merged = []
    for p in lines:
        if merged and p - merged[-1] < 65: merged[-1] = (merged[-1]+p)/2
        else: merged.append(p)
    pitch = float(np.median(np.diff(merged))) if len(merged) > 1 else 110
    print(name, len(merged), 'lines, pitch', round(pitch))
    for k, ly in enumerate(merged):
        y = int(y0 + ly)
        top = int(y - pitch*0.85); bot = int(y + pitch*0.50)
        band = im.crop((x0-10, top, x1+10, bot))
        w, h = band.size; half = w//2
        for side, (a, b) in (('L', (0, half+60)), ('R', (half-60, w))):
            c = band.crop((a, 0, b, h))
            c = c.resize((int(c.width*1.6), int(c.height*1.6)), Image.LANCZOS)
            c.save(f'img/bands/{name}_{k+1:02d}{side}.png')
