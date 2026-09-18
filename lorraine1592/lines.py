"""Line segmentation for sloping manuscript lines: split the page into vertical strips, find lines
within each strip (where the slope is small), then stitch strips left to right by line order."""
import sys, statistics
sys.path.insert(0,'.')
from glyphs import read_bmp, components
from glyphs2 import merge_overlaps
INK=120

def strip_lines(cs, gap=38):
    """Cluster components of one strip into lines by y-centre gaps."""
    cs=sorted(cs, key=lambda c:(c['y0']+c['y1'])/2)
    out=[]; cur=[]; last=None
    for c in cs:
        m=(c['y0']+c['y1'])/2
        if last is not None and m-last>gap:
            out.append(cur); cur=[]
        cur.append(c); last=m
    if cur: out.append(cur)
    return [sorted(l,key=lambda c:c['x0']) for l in out]

def run(bmp, nstrips=8, gap=38):
    w,h,g=read_bmp(bmp)
    cs=components(g,w,h,INK,30,8)
    sw=w//nstrips
    strips=[]
    for i in range(nstrips):
        lo,hi=i*sw,(i+1)*sw if i<nstrips-1 else w
        sub=[c for c in cs if lo <= (c['x0']+c['x1'])/2 < hi]
        strips.append(strip_lines(sub,gap))
    return w,h,g,cs,strips

if __name__=='__main__':
    w,h,g,cs,strips=run('/tmp/lor.bmp')
    print('components',len(cs))
    for i,s in enumerate(strips):
        print(f'strip {i}: {len(s)} lines, sizes {[len(l) for l in s]}')
