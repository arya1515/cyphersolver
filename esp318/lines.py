import sys, os, numpy as np
from PIL import Image, ImageOps

def bands(path, x0f=0.0, x1f=1.0, y0f=0.0, y1f=1.0, thr=0.55, minh=18):
    im = Image.open(path).convert('L')
    W,H = im.size
    x0,x1 = int(W*x0f), int(W*x1f); y0,y1 = int(H*y0f), int(H*y1f)
    a = np.asarray(im.crop((x0,y0,x1,y1)), dtype=float)
    a = (a - a.min())/(a.max()-a.min()+1e-9)
    # ink = dark
    ink = (a < thr).sum(axis=1).astype(float)
    ink = np.convolve(ink, np.ones(5)/5, mode='same')
    t = max(3.0, ink.max()*0.10)
    on = ink > t
    out=[]; s=None
    for i,v in enumerate(on):
        if v and s is None: s=i
        elif not v and s is not None:
            if i-s>=minh: out.append((s+y0, i+y0))
            s=None
    if s is not None and len(on)-s>=minh: out.append((s+y0, len(on)+y0))
    return out, (x0,x1,W,H)

if __name__=='__main__':
    p=sys.argv[1]
    b,(x0,x1,W,H)=bands(p, *[float(v) for v in sys.argv[2:6]] if len(sys.argv)>5 else (0,1,0,1))
    print(W,H,len(b))
    for i,(a,c) in enumerate(b,1): print(i,a,c,c-a)
