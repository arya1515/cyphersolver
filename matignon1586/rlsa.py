"""Find text lines by run-length smoothing (RLSA), which is what actually survives pitch wander.

Smear the binary image horizontally so each written line closes into one solid bar, label the
bars, and keep the ones that look like lines. Each bar carries its own bounding box, so tiles cut
from it are framed on the line itself and cannot be clipped by a drifting grid.
"""
import sys, json
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage

def otsu(a):
    hist,_ = np.histogram(a, bins=256, range=(0,256))
    tot = a.size; sall = float(np.dot(np.arange(256), hist))
    sB = 0.0; wB = 0; best = (0.0, 128)
    for t in range(256):
        wB += hist[t]
        if wB == 0: continue
        wF = tot - wB
        if wF == 0: break
        sB += t*hist[t]
        v = wB*wF*((sB/wB) - ((sall-sB)/wF))**2
        if v > best[0]: best = (v, t)
    return best[1]

def binarize(path):
    im = ImageOps.autocontrast(Image.open(path).convert('L'), 1)
    a = np.array(im)
    bw = a < otsu(a)
    return ndimage.median_filter(bw, size=3), a

def lines_of(bw, smear=55, vclose=3, min_w_frac=0.25):
    m = ndimage.binary_closing(bw, structure=np.ones((1, smear), bool))
    if vclose > 1:
        m = ndimage.binary_closing(m, structure=np.ones((vclose, 1), bool))
    lab, n = ndimage.label(m)
    out = []
    W = bw.shape[1]
    for sl in ndimage.find_objects(lab):
        if sl is None: continue
        ys, xs = sl
        w = xs.stop - xs.start; h = ys.stop - ys.start
        if w < min_w_frac * W: continue
        if h < 12 or h > 260: continue
        out.append({'x0': int(xs.start), 'x1': int(xs.stop),
                    'y0': int(ys.start), 'y1': int(ys.stop),
                    'cy': float((ys.start + ys.stop) / 2)})
    out.sort(key=lambda L: L['cy'])
    return out

if __name__ == '__main__':
    src, outf = sys.argv[1], sys.argv[2]
    smear = int(sys.argv[3]) if len(sys.argv) > 3 else 55
    bw, a = binarize(src)
    L = lines_of(bw, smear=smear)
    json.dump(L, open(outf, 'w'))
    print('lines', len(L))
    print('cy   ', [int(x['cy']) for x in L])
    print('h    ', [x['y1']-x['y0'] for x in L])
    if len(L) > 1:
        print('pitch', [int(L[i+1]['cy']-L[i]['cy']) for i in range(len(L)-1)])
