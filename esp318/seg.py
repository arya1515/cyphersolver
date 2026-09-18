import sys, json, numpy as np
from PIL import Image
from scipy import ndimage

def binarize(path, x0f, x1f, y0, y1, block=81, C=14):
    im = Image.open(path).convert('L')
    W,H = im.size
    a = np.asarray(im.crop((int(W*x0f), y0, int(W*x1f), y1)), dtype=np.float32)
    # local mean threshold
    k = block
    m = ndimage.uniform_filter(a, size=k, mode='nearest')
    bw = (a < m - C)
    bw = ndimage.binary_opening(bw, np.ones((2,2)))
    return bw, a

if __name__ == '__main__':
    p = sys.argv[1]; x0f=float(sys.argv[2]); x1f=float(sys.argv[3]); y0=int(sys.argv[4]); y1=int(sys.argv[5])
    bw,a = binarize(p,x0f,x1f,y0,y1)
    lab,n = ndimage.label(bw)
    sl = ndimage.find_objects(lab)
    sizes = ndimage.sum(bw, lab, range(1,n+1))
    print('components', n, 'ink frac', bw.mean().round(4))
    import collections
    hs=[s[0].stop-s[0].start for s in sl]; ws=[s[1].stop-s[1].start for s in sl]
    hs=np.array(hs); ws=np.array(ws); sizes=np.array(sizes)
    big = sizes>25
    print('kept', big.sum(), 'median h', np.median(hs[big]), 'median w', np.median(ws[big]))
    print('h pct', np.percentile(hs[big],[10,50,90]).round(1), 'w pct', np.percentile(ws[big],[10,50,90]).round(1))
