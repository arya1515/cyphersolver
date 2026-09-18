"""cut.py <canvas> <x0> <y0> <x1> <y1> <prefix> [nparts] [zoom] [nlines]
Cut text lines inside a fractional box of full/cNNN.jpg by ink-profile peaks (robust to touching
descenders) and write <prefix>_L<nn><a|b|c>.jpg. If nlines is given, force that many lines."""
import sys, os
import numpy as np
from PIL import Image, ImageOps

c = int(sys.argv[1]); x0f, y0f, x1f, y1f = [float(v) for v in sys.argv[2:6]]
prefix = sys.argv[6]
nparts = int(sys.argv[7]) if len(sys.argv) > 7 else 3
zoom = float(sys.argv[8]) if len(sys.argv) > 8 else 3.0
nlines = int(sys.argv[9]) if len(sys.argv) > 9 else 0
im = Image.open(f'bethune/full/c{c:03d}.jpg')
W, H = im.size
bx0, by0, bx1, by1 = int(W*x0f), int(H*y0f), int(W*x1f), int(H*y1f)
reg = im.crop((bx0, by0, bx1, by1)).convert('L')
a = np.asarray(reg, dtype=np.float32)
ink = (a < 145).mean(axis=1)
sm = np.convolve(ink, np.ones(9)/9, mode='same')
Hr = len(sm)
# dominant line spacing by autocorrelation of the mean-removed profile
d = sm - sm.mean()
ac = np.correlate(d, d, 'full')[Hr-1:]
lo, hi = 40, min(400, Hr//2)
period = int(lo + np.argmax(ac[lo:hi])) if hi > lo else 100
# peak picking: local maxima at least 0.55*period apart, tallest first
order = np.argsort(-sm)
peaks = []
minsep = int(0.78*period)
for idx in order:
    if sm[idx] < sm.max()*0.25: break
    if all(abs(idx-p) >= minsep for p in peaks): peaks.append(int(idx))
peaks.sort()
if nlines and len(peaks) != nlines:      # fall back to even spacing over the peak span
    if len(peaks) >= 2:
        lo_p, hi_p = peaks[0], peaks[-1]
    else:
        lo_p, hi_p = int(0.05*Hr), int(0.95*Hr)
    peaks = [int(round(lo_p + (hi_p-lo_p)*i/(nlines-1))) for i in range(nlines)] if nlines > 1 else [ (lo_p+hi_p)//2 ]
half = int(period*0.62)
os.makedirs(os.path.dirname(prefix) or '.', exist_ok=True)
Wr = bx1-bx0
for n, pk in enumerate(peaks, 1):
    y0 = max(0, pk-half); y1 = min(Hr, pk+half)
    for p in range(nparts):
        l = int(Wr*p/nparts) - int(0.015*Wr); r = int(Wr*(p+1)/nparts) + int(0.015*Wr)
        s = reg.crop((max(0, l), y0, min(Wr, r), y1))
        s = ImageOps.autocontrast(s, cutoff=1)
        s = s.resize((int(s.width*zoom), int(s.height*zoom)), Image.LANCZOS)
        s.save(f'{prefix}_L{n:02d}{"abcdef"[p]}.jpg', quality=94)
print(prefix, 'period', period, 'lines', len(peaks), 'centres', peaks)
