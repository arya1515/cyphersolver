"""Per-glyph segmentation, second version.

Vertical projection inside each fitted line band, then two clean-ups that the first version
lacked: runs separated by less than a fraction of the median glyph width are merged (a glyph
drawn in two strokes), and small high boxes (diacritic dots, the dots of the .v. figure) are
absorbed into the nearest real box instead of becoming glyphs of their own.
"""
import numpy as np, json, sys
from PIL import Image, ImageOps
from scipy.ndimage import uniform_filter

def binarize(a, blk=61, C=10):
    m = uniform_filter(a.astype(np.float32), size=blk)
    return (a < m - C)

def runs_of(on):
    out=[]; s=None
    for i,v in enumerate(on):
        if v and s is None: s=i
        elif not v and s is not None: out.append([s,i]); s=None
    if s is not None: out.append([s,len(on)])
    return out

def segment_line(bw, y0, y1):
    band = bw[y0:y1]
    col = band.sum(axis=0)
    rs = runs_of(col >= 1)
    rs = [r for r in rs if r[1]-r[0] >= 2]
    if not rs: return []
    widths = sorted(r[1]-r[0] for r in rs)
    med = widths[len(widths)//2]
    gap = max(4, int(0.45*med))
    merged=[]
    for r in rs:
        if merged and r[0]-merged[-1][1] < gap: merged[-1][1]=r[1]
        else: merged.append(list(r))
    # absorb small fragments into a neighbour
    boxes=[]
    for a,b in merged:
        sub=band[:, a:b]
        ink=int(sub.sum())
        w=b-a
        rows=np.where(sub.sum(axis=1)>0)[0]
        h=int(rows[-1]-rows[0]+1) if len(rows) else 0
        boxes.append({'a':a,'b':b,'ink':ink,'w':w,'h':h,'t':int(rows[0]) if len(rows) else 0,
                      'bt':int(rows[-1])+1 if len(rows) else 0})
    med_ink = sorted(x['ink'] for x in boxes)[len(boxes)//2]
    out=[]
    for bx in boxes:
        small = bx['ink'] < 0.22*med_ink or (bx['w']<=5 and bx['h']<=8)
        if small and out and bx['a']-out[-1]['b'] < 3.0*gap:
            out[-1]['b']=max(out[-1]['b'],bx['b']); out[-1]['ink']+=bx['ink']
            out[-1]['t']=min(out[-1]['t'],bx['t']); out[-1]['bt']=max(out[-1]['bt'],bx['bt'])
        elif small and out is not None and len(out)==0:
            continue
        else:
            out.append(bx)
    return [(o['a'],o['b'],y0+o['t'],y0+o['bt']) for o in out if o['ink']>=0.15*med_ink]

if __name__=='__main__':
    src, ysfile, half, outf = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    im=ImageOps.autocontrast(Image.open(src).convert('L'),1)
    a=np.array(im); bw=binarize(a)
    ys=[int(v) for v in open(ysfile).read().split(',')]
    res=[]
    for y in ys:
        res.append(segment_line(bw, max(0,int(y-half)), min(bw.shape[0], int(y+half))))
    json.dump([[list(map(int,b)) for b in r] for r in res], open(outf,'w'))
    print('lines',len(res),'counts',[len(r) for r in res])
