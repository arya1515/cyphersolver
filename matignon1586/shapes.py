"""Segment a block into glyph boxes, describe each by shape, and cluster them.

Everything downstream works on cluster ids, not on what the eye thinks a figure is: the page
becomes a sequence of symbols and the cipher becomes an ordinary homophonic substitution again.
"""
import numpy as np, json, sys
from PIL import Image, ImageOps, ImageFilter
from scipy.cluster.hierarchy import linkage, fcluster
from seg2 import binarize, runs_of

def line_boxes(bw, y, half, gap):
    band = bw[max(0,y-half):y+half]
    col = band.sum(axis=0)
    rs = [r for r in runs_of(col >= 1) if r[1]-r[0] >= 2]
    if not rs: return []
    m = []
    for r in rs:
        if m and r[0]-m[-1][1] < gap: m[-1][1] = r[1]
        else: m.append(list(r))
    inks = [int(band[:, x:z].sum()) for x, z in m]
    med = sorted(inks)[len(inks)//2]
    keep = []
    for (x, z), ink in zip(m, inks):
        if ink < 0.25*med and keep and x-keep[-1][1] < 3*gap: keep[-1][1] = z
        elif ink < 0.12*med: continue
        else: keep.append([x, z])
    out = []
    for x, z in keep:
        sub = band[:, x:z]
        rows = np.where(sub.sum(axis=1) > 0)[0]
        if not len(rows): continue
        out.append((x, z, int(max(0,y-half)+rows[0]), int(max(0,y-half)+rows[-1])+1))
    return out

S = 26
def feat(bw, box):
    x0, x1, y0, y1 = box
    sub = bw[y0:y1, x0:x1]
    h, w = sub.shape
    if h == 0 or w == 0: return None
    sc = (S-4)/max(h, w)
    g = Image.fromarray((sub*255).astype(np.uint8)).resize(
        (max(1, int(w*sc)), max(1, int(h*sc))), Image.BILINEAR)
    canv = Image.new('L', (S, S), 0)
    canv.paste(g, ((S-g.width)//2, (S-g.height)//2))
    canv = canv.filter(ImageFilter.GaussianBlur(1.1))
    v = np.asarray(canv, dtype=np.float32).ravel()
    v -= v.mean()
    v /= (np.linalg.norm(v) or 1.0)
    return np.concatenate([v, [1.2*np.log(max(w,1)/max(h,1)), 0.5*min(h,80)/80.0]])

def build(src, ysfile, half, gap, K):
    im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
    bw = binarize(np.array(im))
    ys = [int(v) for v in open(ysfile).read().split(',')]
    lines, feats, index = [], [], []
    for li, y in enumerate(ys):
        bs = line_boxes(bw, y, half, gap)
        ids = []
        for b in bs:
            f = feat(bw, b)
            if f is None: continue
            ids.append(len(feats)); feats.append(f); index.append((li, b))
        lines.append(ids)
    F = np.array(feats)
    Z = linkage(F, method='average', metric='correlation')
    lab = fcluster(Z, t=K, criterion='maxclust')
    return lines, lab.tolist(), index, bw

if __name__ == '__main__':
    src, ysfile, half, gap, K, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    lines, lab, index, bw = build(src, ysfile, half, gap, K)
    json.dump({'lines': lines, 'labels': lab,
               'index': [[li, list(map(int, b))] for li, b in index]}, open(out, 'w'))
    print('boxes', len(lab), 'clusters', max(lab), 'per line', [len(l) for l in lines])
