"""Segment the cipher of BnF fr. 3621 no. 97 into glyphs and cluster them by shape.
Reuses the pure-Python tooling built for sormano1529 (see that folder's NOTES.md), retuned for this
page: ink on cream paper rather than microfilm, so the threshold is 120 rather than 130."""
import sys, statistics, math, json
sys.path.insert(0,'.')
from glyphs import read_bmp, components
from glyphs2 import merge_overlaps
INK=120

def bands(g,w,h,t=INK,frac=0.35,minrun=10):
    prof=[sum(1 for x in range(w) if g[y][x]<t) for y in range(h)]
    fl=statistics.median(prof); mx=max(prof); cut=fl+frac*(mx-fl)
    out=[];s=None
    for y,p in enumerate(prof):
        if p>cut and s is None: s=y
        if p<=cut and s is not None:
            if y-s>=minrun: out.append((s,y-1))
            s=None
    if s is not None: out.append((s,h-1))
    return out

def run(bmp):
    w,h,g=read_bmp(bmp)
    cs=components(g,w,h,INK,30,8)
    bs=bands(g,w,h)
    rows={i:[] for i in range(len(bs))}
    for c in cs:
        m=(c['y0']+c['y1'])/2
        bi=min(range(len(bs)), key=lambda i: 0 if bs[i][0]<=m<=bs[i][1] else min(abs(m-bs[i][0]),abs(m-bs[i][1])))
        rows[bi].append(c)
    seq=[]
    for i in sorted(rows):
        rows[i].sort(key=lambda c:c['x0'])
        mg=merge_overlaps(rows[i], frac=0.6)
        mg=[c for c in mg if c['n']>=45]
        seq.append(mg)
    return w,h,g,bs,seq

if __name__=='__main__':
    w,h,g,bs,seq=run('/tmp/lor.bmp')
    print('bands',len(bs))
    print('per band', [len(s) for s in seq], 'total', sum(len(s) for s in seq))
    for i,(b,s) in enumerate(zip(bs,seq)):
        print(f'  band {i}: y{b[0]}-{b[1]}  glyphs {len(s)}')
