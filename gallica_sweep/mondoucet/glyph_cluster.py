# Segment cipher glyphs from full-resolution page images and cluster them by shape, so that the transcription is
# consistent (same shape -> same id). usage: python glyph_cluster.py <out_prefix> <K> <img:linefrom-lineto>[,...]
# e.g. python glyph_cluster.py c019 90 full_c019.jpg:6-35
import sys, os, json, re
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy import ndimage
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
Image.MAX_IMAGE_PIXELS = None
pref = sys.argv[1]; K = int(sys.argv[2]); specs = sys.argv[3:]
X0F, X1F = 0.17, 0.99


def find_lines(box):
    a = np.asarray(box, dtype=float); ink = (a < 110).mean(axis=1)
    sm = np.convolve(ink, np.ones(9) / 9, mode='same'); thr = max(0.012, sm.max() * 0.12)
    rows = sm > thr; lines = []; i = 0; n = len(rows)
    while i < n:
        if rows[i]:
            j = i
            while j < n and rows[j]:
                j += 1
            if j - i > 25:
                lines.append((i, j))
            i = j
        else:
            i += 1
    merged = []
    for s, e in lines:
        if merged and s - merged[-1][1] < 14:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return merged


glyphs = []   # dict(img(32x32 array), page, line, x0, y0, x1, y1)
for spec in specs:
    path, rng = spec.split(':'); lo, hi = (int(v) for v in rng.split('-'))
    im = Image.open(path).convert('L'); im = ImageOps.autocontrast(im, cutoff=1)
    W, H = im.size; box = im.crop((int(W * X0F), 0, int(W * X1F), H))
    lines = find_lines(box)
    print(path, 'lines', len(lines))
    A = np.asarray(box)
    for li, (s, e) in enumerate(lines, 1):
        if li < lo or li > hi:
            continue
        pad = 22
        y0 = max(0, s - pad); y1 = min(A.shape[0], e + pad)
        strip = A[y0:y1, :]
        binim = strip < 120
        lab, n = ndimage.label(binim, structure=np.ones((3, 3)))
        objs = ndimage.find_objects(lab)
        comps = []
        for k, sl in enumerate(objs, 1):
            if sl is None:
                continue
            ys, xs = sl; area = int((lab[sl] == k).sum())
            if area < 25:
                continue
            comps.append([xs.start, ys.start, xs.stop, ys.stop, area])
        comps.sort()
        # diacritics: small components (dots, apostrophes, bars) are attached to the nearest large glyph whose
        # x-range lies within 16 px; large glyphs whose x-ranges overlap by > 30% are merged (stacked parts)
        if comps:
            hs = sorted(c[3] - c[1] for c in comps); medh = hs[len(hs) // 2]
            ars = sorted(c[4] for c in comps); meda = ars[len(ars) // 2]
        big = [list(c) for c in comps if (c[3] - c[1]) >= 0.45 * medh and c[4] >= 0.25 * meda]
        small = [c for c in comps if not ((c[3] - c[1]) >= 0.45 * medh and c[4] >= 0.25 * meda)]
        merged = []
        for c in sorted(big):
            if merged:
                p = merged[-1]
                ov = min(p[2], c[2]) - max(p[0], c[0]); wmin = min(p[2] - p[0], c[2] - c[0])
                if ov > 0.3 * wmin:
                    merged[-1] = [min(p[0], c[0]), min(p[1], c[1]), max(p[2], c[2]), max(p[3], c[3]), p[4] + c[4]]
                    continue
            merged.append(list(c))
        for c in small:
            cx = (c[0] + c[2]) / 2
            best = None; bd = 1e9
            for g in merged:
                d = 0 if g[0] - 16 <= cx <= g[2] + 16 else min(abs(cx - g[0]), abs(cx - g[2]))
                if d < bd:
                    bd = d; best = g
            if best is not None and bd <= 16:
                best[0] = min(best[0], c[0]); best[1] = min(best[1], c[1]); best[2] = max(best[2], c[2]); best[3] = max(best[3], c[3]); best[4] += c[4]
        for c in merged:
            x0, yy0, x1, yy1, area = c
            h = yy1 - yy0; w = x1 - x0
            if h < 12 or w < 4 or area < 60:
                continue
            g = binim[yy0:yy1, x0:x1].astype(np.uint8) * 255
            gi = Image.fromarray(255 - g)
            side = max(w, h); canvas = Image.new('L', (side, side), 255); canvas.paste(gi, ((side - w) // 2, (side - h) // 2))
            small = np.asarray(canvas.resize((32, 32), Image.LANCZOS), dtype=float) / 255.0
            glyphs.append({'v': (1 - small).ravel(), 'page': path, 'line': li, 'x0': int(x0 + W * X0F), 'y0': int(yy0 + y0), 'x1': int(x1 + W * X0F), 'y1': int(yy1 + y0), 'w': w, 'h': h})
print('glyphs', len(glyphs))
X = np.stack([g['v'] for g in glyphs])
# add aspect features
asp = np.array([[g['w'] / max(1, g['h']), g['h'] / 60.0] for g in glyphs])
Xp = PCA(n_components=min(40, X.shape[0] - 1), random_state=0).fit_transform(X)
Xf = np.hstack([Xp, asp * 3.0])
km = KMeans(n_clusters=K, n_init=10, random_state=0).fit(Xf)
labels = km.labels_
for g, l in zip(glyphs, labels):
    g['c'] = int(l); del g['v']
json.dump(glyphs, open(f'{pref}_glyphs.json', 'w'))
# transcription by line
lines_out = {}
for g in glyphs:
    lines_out.setdefault((g['page'], g['line']), []).append(g)
with open(f'{pref}_clusters.txt', 'w') as f:
    for (p, li), gs in sorted(lines_out.items()):
        gs.sort(key=lambda g: g['x0'])
        f.write('%s %02d: %s\n' % (os.path.basename(p), li, ' '.join('c%d' % g['c'] for g in gs)))
# cluster sheets: up to 14 exemplars per cluster, 48px each
os.makedirs('clusters', exist_ok=True)
ims = {}
def crop(g):
    if g['page'] not in ims:
        ims[g['page']] = ImageOps.autocontrast(Image.open(g['page']).convert('L'), cutoff=1)
    im = ims[g['page']]
    c = im.crop((g['x0'] - 4, g['y0'] - 4, g['x1'] + 4, g['y1'] + 4))
    side = max(c.size); cv = Image.new('L', (side, side), 255); cv.paste(c, ((side - c.width) // 2, (side - c.height) // 2))
    return cv.resize((56, 56), Image.LANCZOS)
counts = np.bincount(labels, minlength=K)
order = np.argsort(-counts)
rows = []
for cl in order:
    idx = [i for i, l in enumerate(labels) if l == cl][:14]
    row = Image.new('L', (110 + 14 * 60, 60), 255); d = ImageDraw.Draw(row)
    d.text((4, 4), 'c%d' % cl, fill=0); d.text((4, 30), 'n=%d' % counts[cl], fill=0)
    for k, i in enumerate(idx):
        row.paste(crop(glyphs[i]), (110 + k * 60, 2))
    rows.append(row)
per = 22
for s in range(0, len(rows), per):
    grp = rows[s:s + per]; sheet = Image.new('L', (rows[0].width, 60 * len(grp)), 255)
    for k, r in enumerate(grp):
        sheet.paste(r, (0, 60 * k))
    sheet.save(f'clusters/{pref}_sheet{s // per:02d}.png')
print('cluster sizes', sorted(counts.tolist(), reverse=True))
