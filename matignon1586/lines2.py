"""Find text lines by assembling connected components, not by fitting a grid.

A grid assumes constant pitch; these leaves wander 10-15 % line to line and the page is slightly
skewed, which is what kept clipping the tiles. Here every ink blob is found, noise is dropped, and
the blobs are swept left to right and attached to whichever line's running baseline they sit on.
Each line then has its own bounding box, so a tile cropped to it cannot be mis-centred.
"""
import sys, json
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage

def find_lines(bw, pitch, min_area=12, tol_frac=0.34):
    lab, n = ndimage.label(bw)
    objs = ndimage.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs):
        if sl is None: continue
        ys, xs = sl
        h = ys.stop - ys.start; w = xs.stop - xs.start
        area = int(bw[sl].sum())
        if area < min_area: continue
        if h > 200 or w > 400: continue          # blots, rules, bleed-through
        comps.append({'x0': xs.start, 'x1': xs.stop, 'y0': ys.start, 'y1': ys.stop,
                      'cx': (xs.start+xs.stop)/2, 'cy': (ys.start+ys.stop)/2, 'h': h})
    if not comps: return []
    tol = tol_frac * pitch                       # a blob belongs to a line if it sits within
                                                 # about a third of the line pitch of its baseline
    comps.sort(key=lambda c: c['cx'])
    lines = []                                   # each: {'cys': [...], 'comps': [...]}
    for c in comps:
        best, bd = None, 1e9
        for L in lines:
            ref = np.mean(L['cys'][-8:])
            d = abs(c['cy'] - ref)
            if d < bd: bd, best = d, L
        if best is not None and bd <= tol:
            best['cys'].append(c['cy']); best['comps'].append(c)
        else:
            lines.append({'cys': [c['cy']], 'comps': [c]})
    out = []
    for L in lines:
        if len(L['comps']) < 6: continue
        xs0 = min(c['x0'] for c in L['comps']); xs1 = max(c['x1'] for c in L['comps'])
        ys0 = min(c['y0'] for c in L['comps']); ys1 = max(c['y1'] for c in L['comps'])
        out.append({'x0': int(xs0), 'x1': int(xs1), 'y0': int(ys0), 'y1': int(ys1),
                    'cy': float(np.mean(L['cys'])), 'n': len(L['comps'])})
    out.sort(key=lambda L: L['cy'])
    # merge lines whose vertical spans overlap heavily (a split line)
    merged = []
    for L in out:
        if merged and abs(L['cy'] - merged[-1]['cy']) < 0.45 * tol:
            m = merged[-1]
            m['x0'] = min(m['x0'], L['x0']); m['x1'] = max(m['x1'], L['x1'])
            m['y0'] = min(m['y0'], L['y0']); m['y1'] = max(m['y1'], L['y1'])
            m['cy'] = (m['cy']*m['n'] + L['cy']*L['n'])/(m['n']+L['n']); m['n'] += L['n']
        else:
            merged.append(L)
    return merged

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
    a = np.array(im)
    bw = a < (a.mean() - 0.35*a.std())
    # pitch from a comb over the row-ink profile: robust, and only one number is needed
    prof = np.convolve(bw.sum(axis=1).astype(float), np.ones(9)/9, 'same')
    best = None
    for sp in np.arange(80, 180, 0.5):
        n = int(len(prof)/sp)
        for ph in np.arange(0, sp, 2.0):
            ys = [ph+sp*i for i in range(n)]
            if ys[-1] >= len(prof): continue
            sc = sum(prof[int(y)] for y in ys)/n
            if best is None or sc > best[0]: best = (sc, sp)
    pitch = best[1]
    print('pitch est', round(pitch,1))
    L = find_lines(bw, pitch)
    json.dump(L, open(out, 'w'))
    print('lines', len(L))
    print('cy   ', [int(x['cy']) for x in L])
    print('pitch', [int(L[i+1]['cy']-L[i]['cy']) for i in range(len(L)-1)])
