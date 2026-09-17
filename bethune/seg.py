"""seg.py — glyph segmentation for the Bethune cipher hand.

usage: python seg.py <canvas> <x0> <y0> <x1> <y1> <outjson> [--lines N] [--montage PREFIX] [--deskew]

Finds text lines by ink-profile peaks inside a fractional box of full/cNNN.jpg, then cuts each line into
glyphs: connected components, small parts merged into the component they sit over/under (dots, ticks,
broken strokes), then components whose x-spans overlap heavily merged left to right.
Writes {'canvas':.., 'box':[..], 'lines':[{'y':[y0,y1],'boxes':[[x0,y0,x1,y1],..]},..]} in REGION pixel
coordinates, and optionally numbered montages for eyeballing.
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy import ndimage

def otsu(a):
    hist, _ = np.histogram(a, bins=256, range=(0, 256))
    tot = hist.sum(); s = (np.arange(256)*hist).sum()
    wB = 0.0; sB = 0.0; best = 0.0; thr = 128
    for i in range(256):
        wB += hist[i]
        if wB == 0: continue
        wF = tot - wB
        if wF == 0: break
        sB += i*hist[i]
        mB = sB/wB; mF = (s-sB)/wF
        v = wB*wF*(mB-mF)**2
        if v > best: best = v; thr = i
    return thr

def find_lines(reg_arr, nlines=0):
    ink = (reg_arr < 145).mean(axis=1)
    sm = np.convolve(ink, np.ones(9)/9, mode='same')
    H = len(sm)
    d = sm - sm.mean()
    ac = np.correlate(d, d, 'full')[H-1:]
    lo, hi = 40, min(400, H//2)
    period = int(lo + np.argmax(ac[lo:hi])) if hi > lo else 110
    order = np.argsort(-sm); peaks = []; minsep = int(0.55*period)
    for idx in order:
        if sm[idx] < sm.max()*0.25: break
        if all(abs(idx-p) >= minsep for p in peaks): peaks.append(int(idx))
    peaks.sort()
    if nlines and len(peaks) != nlines and len(peaks) >= 2:
        lo_p, hi_p = peaks[0], peaks[-1]
        peaks = [int(round(lo_p+(hi_p-lo_p)*i/(nlines-1))) for i in range(nlines)]
    return peaks, period

def glyphs_in_line(band, thr):
    """band: 2-D uint8 array of the line. returns list of [x0,y0,x1,y1] in band coords."""
    bw = band < thr
    bw = ndimage.binary_closing(bw, structure=np.ones((2, 2)))
    lab, n = ndimage.label(bw, structure=np.ones((3, 3)))
    if n == 0: return []
    objs = ndimage.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs):
        ys, xs = sl
        area = int(bw[sl].sum())
        comps.append({'x0': xs.start, 'x1': xs.stop, 'y0': ys.start, 'y1': ys.stop, 'area': area})
    med_area = np.median([c['area'] for c in comps]) if comps else 1
    # drop specks
    comps = [c for c in comps if c['area'] >= max(6, 0.04*med_area)]
    comps.sort(key=lambda c: (c['x0']+c['x1'])/2)
    # merge: a component whose x-span is mostly inside another's (dots/ticks/broken strokes)
    changed = True
    while changed:
        changed = False
        for i in range(len(comps)-1):
            a, b = comps[i], comps[i+1]
            ov = min(a['x1'], b['x1']) - max(a['x0'], b['x0'])
            wmin = min(a['x1']-a['x0'], b['x1']-b['x0'])
            if wmin <= 0: continue
            if ov > 0.55*wmin:
                comps[i] = {'x0': min(a['x0'], b['x0']), 'x1': max(a['x1'], b['x1']),
                            'y0': min(a['y0'], b['y0']), 'y1': max(a['y1'], b['y1']),
                            'area': a['area']+b['area']}
                del comps[i+1]; changed = True; break
    return [[c['x0'], c['y0'], c['x1'], c['y1']] for c in comps]

def main():
    canvas = int(sys.argv[1]); x0f, y0f, x1f, y1f = [float(v) for v in sys.argv[2:6]]
    outjson = sys.argv[6]
    nlines = int(sys.argv[sys.argv.index('--lines')+1]) if '--lines' in sys.argv else 0
    montage = sys.argv[sys.argv.index('--montage')+1] if '--montage' in sys.argv else None
    im = Image.open(f'bethune/full/c{canvas:03d}.jpg').convert('L')
    W, H = im.size
    box = (int(W*x0f), int(H*y0f), int(W*x1f), int(H*y1f))
    reg = im.crop(box)
    reg = ImageOps.autocontrast(reg, cutoff=1)
    arr = np.asarray(reg, dtype=np.uint8)
    thr = min(otsu(arr), 150)
    peaks, period = find_lines(arr, nlines)
    half = int(period*0.62)
    lines = []
    for pk in peaks:
        ya, yb = max(0, pk-half), min(arr.shape[0], pk+half)
        band = arr[ya:yb]
        bs = glyphs_in_line(band, thr)
        lines.append({'y': [int(ya), int(yb)], 'boxes': [[b[0], b[1]+ya, b[2], b[3]+ya] for b in bs]})
    json.dump({'canvas': canvas, 'box': list(box), 'thr': int(thr), 'period': int(period), 'lines': lines},
              open(outjson, 'w'), indent=1)
    print(outjson, 'thr', thr, 'period', period, 'lines', len(lines), 'glyphs', [len(l['boxes']) for l in lines])
    if montage:
        for n, l in enumerate(lines, 1):
            ya, yb = l['y']
            strip = reg.crop((0, ya, reg.width, yb)).convert('RGB')
            d = ImageDraw.Draw(strip)
            for k, (bx0, by0, bx1, by1) in enumerate(l['boxes']):
                d.rectangle([bx0, by0-ya, bx1, by1-ya], outline=(255, 0, 0), width=2)
                d.text((bx0+2, 2), str(k+1), fill=(0, 0, 255))
            strip = strip.resize((int(strip.width*2.2), int(strip.height*2.2)), Image.LANCZOS)
            strip.save(f'{montage}_L{n:02d}.jpg', quality=92)
        print('montages', montage)

if __name__ == '__main__':
    main()
