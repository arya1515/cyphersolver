import numpy as np, pickle, sys
from PIL import Image
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from glyphs import extract

S = 28
def feat(b):
    h, w = b.shape
    im = Image.fromarray((b*255).astype('uint8'))
    # scale so the larger side is S, pad to SxS centred
    sc = S/max(h, w)
    nw, nh = max(1,int(round(w*sc))), max(1,int(round(h*sc)))
    im = im.resize((nw, nh), Image.BILINEAR)
    a = np.zeros((S, S), np.float32)
    y0 = (S-nh)//2; x0 = (S-nw)//2
    a[y0:y0+nh, x0:x0+nw] = np.asarray(im, np.float32)/255.
    v = a.ravel()
    v = v - v.mean()
    n = np.linalg.norm(v)
    return v/n if n > 0 else v, w/float(h)

def build(path, x0f, x1f, y0, y1, pitch, first_top, out):
    g, bw = extract(path, x0f, x1f, y0, y1, pitch=pitch, first_top=first_top)
    F = []; AR = []
    for x in g:
        f, ar = feat(x['bmp']); F.append(f); AR.append(ar)
    F = np.array(F); AR = np.array(AR)
    X = np.hstack([F, (np.clip(AR,0.15,6.0)[:,None])*0.9])
    D = pdist(X, 'cosine')
    Z = linkage(D, 'average')
    pickle.dump(dict(g=[{k:v for k,v in x.items() if k!='bmp'} for x in g],
                     bmps=[x['bmp'] for x in g], Z=Z, X=X), open(out,'wb'))
    return g, Z, X

def montage(g, labels, path, maxper=14, cell=64):
    ks = sorted(set(labels), key=lambda k: -list(labels).count(k))
    rows = []
    for k in ks:
        idx = [i for i,l in enumerate(labels) if l==k][:maxper]
        row = np.ones((cell, cell*(maxper+1)), np.uint8)*255
        for j,i in enumerate(idx):
            b = g[i]['bmp']; h,w = b.shape
            sc = (cell-8)/max(h,w); nw,nh = max(1,int(w*sc)), max(1,int(h*sc))
            im = np.asarray(Image.fromarray((~b*255).astype('uint8')).resize((nw,nh), Image.BILINEAR))
            yo=(cell-nh)//2; xo=cell*(j+1)+(cell-nw)//2
            row[yo:yo+nh, xo:xo+nw] = im
        rows.append((k, len(([i for i,l in enumerate(labels) if l==k])), row))
    H = cell*len(rows)
    out = np.ones((H, cell*(maxper+1)), np.uint8)*255
    for r,(k,n,row) in enumerate(rows): out[r*cell:(r+1)*cell] = row
    Image.fromarray(out).save(path)
    return [(k,n) for k,n,_ in rows]

if __name__=='__main__':
    g, Z, X = build('full/f122r.jpg', 0.14, 0.93, 800, 4250, 114, 32, 'f122r_glyphs.pkl')
    for nc in (45, 60, 80):
        lab = fcluster(Z, nc, 'maxclust')
        sizes = np.bincount(lab)[1:]
        print(nc, 'clusters; singletons', (sizes==1).sum(), 'top sizes', sorted(sizes)[::-1][:12])
