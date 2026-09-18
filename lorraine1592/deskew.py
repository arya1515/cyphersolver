"""Line segmentation by shear-deskew: the baselines of this page slope, so find the shear that sharpens
the histogram of component y-centres, then assign components to lines in deskewed coordinates."""
import sys, collections, math
sys.path.insert(0,'.')
from glyphs import read_bmp, components
from glyphs2 import merge_overlaps
INK=120; XMAX=2620

def load(bmp):
    w,h,g=read_bmp(bmp)
    cs=[c for c in components(g,w,h,INK,30,8) if (c['x0']+c['x1'])/2 < XMAX]
    return w,h,g,cs

def best_shear(cs, bw=8):
    def ent(s):
        hist=collections.Counter()
        for c in cs:
            y=(c['y0']+c['y1'])/2 - s*((c['x0']+c['x1'])/2)
            hist[int(y//bw)]+=1
        t=sum(hist.values())
        return -sum((n/t)*math.log(n/t) for n in hist.values())
    return min((ent(k/1000.0), k/1000.0) for k in range(-60,5))[1]

def lines(cs, slope, gap=45):
    ys=[(((c['y0']+c['y1'])/2 - slope*((c['x0']+c['x1'])/2)), c) for c in cs]
    ys.sort(key=lambda t: t[0])
    out=[]; cur=[]; last=None
    for y,c in ys:
        if last is not None and y-last>gap: out.append(cur); cur=[]
        cur.append(c); last=y
    if cur: out.append(cur)
    res=[]
    for l in out:
        l=sorted(l,key=lambda c:c['x0'])
        l=merge_overlaps(l, frac=0.6)
        l=[c for c in l if c['n']>=45]
        if len(l)>=4: res.append(l)
    return res

if __name__=='__main__':
    w,h,g,cs=load('/tmp/lor.bmp')
    s=best_shear(cs)
    ls=lines(cs,s)
    print(f'shear {s}  lines {len(ls)}  glyphs {sum(len(l) for l in ls)}')
    for i,l in enumerate(ls): print(f'  line {i:2d}: {len(l):3d} glyphs  x {l[0]["x0"]:4d}-{l[-1]["x1"]:4d}')
