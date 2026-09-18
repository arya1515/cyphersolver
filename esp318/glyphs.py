import sys, numpy as np
from scipy import ndimage
from seg import binarize

def extract(path, x0f, x1f, y0, y1, pitch, first_top, C=22, minpix=20, ov=0.35, small=None):
    bw, gray = binarize(path, x0f, x1f, y0, y1, C=C)
    lab, n = ndimage.label(bw)
    objs = ndimage.find_objects(lab)
    sizes = ndimage.sum(bw, lab, range(1, n+1))
    if small is None: small = pitch*pitch*0.035
    comps = []
    for i, sl in enumerate(objs):
        if sizes[i] < minpix: continue
        ys, xs = sl
        h = ys.stop-ys.start; w = xs.stop-xs.start
        if h > 3.2*pitch or w > 6*pitch: continue
        comps.append(dict(i=i+1, y0=ys.start, y1=ys.stop, x0=xs.start, x1=xs.stop,
                          cy=(ys.start+ys.stop)/2., cx=(xs.start+xs.stop)/2., n=int(sizes[i])))
    ncent = int(round((y1-y0-first_top)/pitch))+1
    cent = np.array([first_top + k*pitch for k in range(ncent)])
    for c in comps:
        c['line'] = int(np.argmin(np.abs(cent - c['cy'])))
    glyphs = []
    for ln in sorted(set(c['line'] for c in comps)):
        cs = sorted([c for c in comps if c['line']==ln], key=lambda c: c['x0'])
        big = [c for c in cs if c['n'] >= small]
        sml = [c for c in cs if c['n'] <  small]
        # seed glyphs from big components, merging those that overlap in x by >= ov of the narrower
        groups = []
        for c in big:
            placed = False
            for g in groups:
                gx0 = min(x['x0'] for x in g); gx1 = max(x['x1'] for x in g)
                inter = min(gx1, c['x1']) - max(gx0, c['x0'])
                narrow = min(gx1-gx0, c['x1']-c['x0'])
                if narrow > 0 and inter >= ov*narrow:
                    g.append(c); placed = True; break
            if not placed: groups.append([c])
        # attach small components (dots, bars) to the group with most x-overlap / nearest
        for c in sml:
            best, bs = None, -1e9
            for g in groups:
                gx0 = min(x['x0'] for x in g); gx1 = max(x['x1'] for x in g)
                inter = min(gx1, c['x1']) - max(gx0, c['x0'])
                s = inter if inter > 0 else -min(abs(c['x0']-gx1), abs(gx0-c['x1']))
                if s > bs: bs, best = s, g
            if best is not None and bs > -pitch*0.25: best.append(c)
            else: groups.append([c])
        groups.sort(key=lambda g: min(x['x0'] for x in g))
        for g in groups: glyphs.append((ln, g))
    out=[]
    for ln, cs in glyphs:
        x0=min(c['x0'] for c in cs); x1=max(c['x1'] for c in cs)
        yy0=min(c['y0'] for c in cs); yy1=max(c['y1'] for c in cs)
        mask=np.zeros((yy1-yy0, x1-x0), bool)
        for c in cs:
            sub = (lab[yy0:yy1, x0:x1]==c['i']); mask |= sub
        out.append(dict(line=ln, x0=int(x0), x1=int(x1), y0=int(yy0), y1=int(yy1),
                        n=int(sum(c['n'] for c in cs)), ncomp=len(cs), bmp=mask))
    return out, bw

if __name__=='__main__':
    import collections
    g,bw = extract('full/f122r.jpg', 0.14, 0.93, 800, 4250, pitch=114, first_top=32)
    per = collections.Counter(x['line'] for x in g)
    print('glyphs', len(g), 'lines', len(per), 'median/line', np.median(list(per.values())))
    ws=np.array([x['x1']-x['x0'] for x in g]); hs=np.array([x['y1']-x['y0'] for x in g])
    print('w pct', np.percentile(ws,[5,25,50,75,95]).round(0))
    print('h pct', np.percentile(hs,[5,25,50,75,95]).round(0))
