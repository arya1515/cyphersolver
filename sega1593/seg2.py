# Gap-based glyph segmenter for the Desportes 1593 line crops.
# usage: seg2.py prefix line_from line_to [gap] [thr]  -> writes {prefix}_g2.json (merges into existing) and box renders
import sys, json, os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

def segment(a, thr=160, gap=6, minarea=14):
    ink = a < thr
    lab, nl = ndimage.label(ink, structure=np.ones((3, 3)))
    sizes = ndimage.sum(ink, lab, range(1, nl + 1))
    keep = np.zeros(nl + 1, bool); keep[1:] = sizes >= minarea
    # drop long horizontal rules
    objs = ndimage.find_objects(lab)
    for i, sl in enumerate(objs):
        if sl is None: continue
        if (sl[1].stop - sl[1].start) > 160 and (sl[0].stop - sl[0].start) < 12: keep[i + 1] = False
    ink = keep[lab]
    col = ink.sum(0)
    runs = []; i = 0; n = len(col)
    while i < n:
        if col[i] > 0:
            j = i
            while j < n and col[j] > 0: j += 1
            runs.append([i, j]); i = j
        else: i += 1
    # merge runs separated by small gaps
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= gap: merged[-1][1] = r[1]
        else: merged.append(list(r))
    boxes = []
    for x0, x1 in merged:
        sub = ink[:, x0:x1]
        area = int(sub.sum())
        if area < 25: continue
        ys = np.where(sub.any(1))[0]
        boxes.append([int(x0), int(ys[0]), int(x1), int(ys[-1]) + 1, area])
    # split over-wide boxes at a low-ink valley
    widths = sorted(b[2] - b[0] for b in boxes if b[4] > 150)
    med = widths[len(widths) // 2] if widths else 40
    out = []
    def addbox(x0, x1):
        sub = ink[:, x0:x1]
        if sub.sum() < 25: return
        ys = np.where(sub.any(1))[0]; xs = np.where(sub.any(0))[0]
        out.append([x0 + int(xs[0]), int(ys[0]), x0 + int(xs[-1]) + 1, int(ys[-1]) + 1, int(sub.sum())])
    def rec(x0, x1):
        w = x1 - x0
        if w <= 1.45 * med: addbox(x0, x1); return
        m = int(0.35 * med)
        seg = col[x0 + m:x1 - m]
        if len(seg) == 0: addbox(x0, x1); return
        c = x0 + m + int(seg.argmin())
        if seg.min() <= max(2, 0.2 * col[x0:x1].max()) or w > 2.2 * med:
            rec(x0, c); rec(c, x1)
        else: addbox(x0, x1)
    for b in boxes: rec(b[0], b[2])
    return out, ink

if __name__ == '__main__':
    pre = sys.argv[1]; k0, k1 = int(sys.argv[2]), int(sys.argv[3])
    gap = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    thr = int(sys.argv[5]) if len(sys.argv) > 5 else 160
    fn = f'{pre}_g2.json'
    out = json.load(open(fn)) if os.path.exists(fn) else {}
    for k in range(k0, k1 + 1):
        im = Image.open(f'{pre}_l{k:02d}.png').convert('L'); a = np.asarray(im)
        boxes, ink = segment(a, thr, gap)
        out[str(k)] = boxes
        print(k, len(boxes))
    json.dump(out, open(fn, 'w'))
