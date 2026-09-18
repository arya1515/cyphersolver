import numpy as np, sys, os
from PIL import Image, ImageOps
def segment(fn, x0=90, x1=None, y0=0, y1=None, thr=0.5):
    im = Image.open(fn).convert('L'); a = np.asarray(im).astype(float)
    x1 = x1 or a.shape[1]-20; y1 = y1 or a.shape[0]
    ink = (a[y0:y1, x0:x1] < 110).sum(1).astype(float)
    k = np.convolve(ink, np.ones(9)/9, 'same')
    # find valleys: local minima spaced by ~ line pitch
    pitch = 36
    lines = []; y = 0
    peaks = []
    for i in range(len(k)):
        lo, hi = max(0, i-pitch//2), min(len(k), i+pitch//2)
        if k[i] == k[lo:hi].max() and k[i] > thr*np.median(k[k>0]):
            if not peaks or i - peaks[-1] > pitch*0.6: peaks.append(i)
    return im, [p+y0 for p in peaks]
if __name__ == '__main__':
    fn, tag, y0, y1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    im, peaks = segment(fn, y0=y0, y1=y1)
    im = ImageOps.autocontrast(im, cutoff=1)
    os.makedirs('lines', exist_ok=True)
    W = im.size[0]
    for n, p in enumerate(peaks):
        c = im.crop((70, p-30, W-10, p+26))
        w = c.size[0]//2 + 30
        for h, (a, b) in enumerate([(0, w), (c.size[0]-w, c.size[0])]):
            d = c.crop((a, 0, b, c.size[1])); d = d.resize((d.size[0]*3, d.size[1]*3), Image.LANCZOS)
            d.save(f'lines/{tag}_{n:02d}{"ab"[h]}.png')
    print(len(peaks), peaks)
