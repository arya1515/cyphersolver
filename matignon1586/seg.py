"""Cut a cipher block into per-glyph boxes by vertical projection inside each line band."""
import numpy as np, json, sys
from PIL import Image, ImageOps

def binarize(a, blk=61, C=10):
    from scipy.ndimage import uniform_filter
    m = uniform_filter(a.astype(np.float32), size=blk)
    return (a < m - C)

def line_boxes(bw, y0, y1, minw=6, gap=5, minink=6):
    band = bw[y0:y1]
    col = band.sum(axis=0)
    on = col >= 2
    runs=[]; s=None
    for i,v in enumerate(on):
        if v and s is None: s=i
        elif not v and s is not None:
            runs.append([s,i]); s=None
    if s is not None: runs.append([s,len(on)])
    # merge runs separated by < gap
    merged=[]
    for r in runs:
        if merged and r[0]-merged[-1][1] < gap: merged[-1][1]=r[1]
        else: merged.append(r)
    out=[]
    for a,b in merged:
        if b-a < 3: continue
        sub = band[:, a:b]
        if sub.sum() < minink: continue
        rows = np.where(sub.sum(axis=1) > 0)[0]
        out.append((a, b, y0+rows[0], y0+rows[-1]+1))
    return out

if __name__ == '__main__':
    src = sys.argv[1]; ysfile = sys.argv[2]; half = int(sys.argv[3]); out = sys.argv[4]
    im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
    a = np.array(im)
    bw = binarize(a)
    ys = [int(v) for v in open(ysfile).read().split(',')]
    res = []
    for i, y in enumerate(ys):
        bs = line_boxes(bw, max(0, y-half), min(bw.shape[0], y+half))
        res.append(bs)
        print(i+1, len(bs))
    json.dump([[list(map(int,b)) for b in r] for r in res], open(out,'w'))
