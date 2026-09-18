"""Stitch strip-wise line segments into whole sloping lines, left to right."""
import sys
sys.path.insert(0,'.')
from lines import run
from glyphs2 import merge_overlaps

def stitch(strips, tol=55):
    active=[]   # list of dicts: yest, glyphs
    for si,s in enumerate(strips):
        if not s: continue
        segs=[(sum((c['y0']+c['y1'])/2 for c in l)/len(l), l) for l in s]
        segs.sort()
        if not active:
            active=[{'y':y,'g':list(l)} for y,l in segs]
            continue
        used=set()
        for y,l in segs:
            best,bi=None,None
            for i,a in enumerate(active):
                if i in used: continue
                d=abs(a['y']-y)
                if best is None or d<best: best,bi=d,i
            if bi is not None and best<=tol:
                active[bi]['g'].extend(l); active[bi]['y']=y; used.add(bi)
            else:
                active.append({'y':y,'g':list(l)}); active.sort(key=lambda a:a['y'])
    return active

if __name__=='__main__':
    w,h,g,cs,strips=run('/tmp/lor.bmp')
    act=stitch(strips)
    print('lines stitched:',len(act))
    tot=0
    for i,a in enumerate(act):
        gl=sorted(a['g'], key=lambda c:c['x0'])
        gl=merge_overlaps(gl, frac=0.6)
        gl=[c for c in gl if c['n']>=45]
        a['g']=gl; tot+=len(gl)
        print(f'  line {i:2d} y~{a["y"]:6.0f}  glyphs {len(gl):3d}  x {gl[0]["x0"] if gl else 0}-{gl[-1]["x1"] if gl else 0}')
    print('total glyphs',tot)
