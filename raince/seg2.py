"""Joint glyph segmentation + clustering over several page regions.
Regions are given in REGIONS below. Writes: raince_tokens.json, raince_cipher.txt (fasthomo format,
one text line per manuscript line, symbols = cluster ids), montage sheets sheet_XX.png.
"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.ndimage import uniform_filter, gaussian_filter
from scipy.cluster.hierarchy import linkage, fcluster

NCL = int(sys.argv[1]) if len(sys.argv) > 1 else 70
OUT = sys.argv[2] if len(sys.argv) > 2 else 'raince'
REGIONS = [
    # image, name, x0f, x1f, y0f, y1f
    ('../f2984/c16_full.jpg', 'f29r', 0.59, 0.965, 0.230, 0.746),   # 13 May, f.29r lines 11-36 (unglossed)
    ('../f2984/c17_full.jpg', 'f30v', 0.06, 0.50, 0.03, 0.775),     # 13 May, f.30v all
    ('../f2984/c17_full.jpg', 'f31r', 0.585, 0.965, 0.03, 0.535),   # 13 May, f.31r cipher part
    ('../f2984/c54_full.jpg', 'f105r', 0.55, 0.965, 0.345, 0.80),   # 20 Nov, f.105r unglossed lower part
]
SZ = 24
alltoks = []; feats = []; regs = {}
for img, name, x0f, x1f, y0f, y1f in REGIONS:
    im = Image.open(img).convert('L'); W, H = im.size
    x0, x1, y0, y1 = int(W * x0f), int(W * x1f), int(H * y0f), int(H * y1f)
    reg = np.array(im.crop((x0, y0, x1, y1))).astype(float)
    bg = uniform_filter(reg, size=81)
    bw = (reg < bg - 45)
    lab, n = ndimage.label(bw)
    objs = ndimage.find_objects(lab)
    comps = []
    for i, o in enumerate(objs):
        m = (lab[o] == i + 1); s = m.sum()
        h = o[0].stop - o[0].start
        dark = (bg[o] - reg[o])[m].mean()
        if s >= 60 and h >= 14 and dark >= 55:
            comps.append(dict(y0=int(o[0].start), y1=int(o[0].stop), x0=int(o[1].start), x1=int(o[1].stop), s=int(s), id=i + 1))
    yc = np.array([(c['y0'] + c['y1']) / 2 for c in comps])
    hist, edges = np.histogram(yc, bins=np.arange(0, y1 - y0 + 20, 8))
    sm = np.convolve(hist, np.ones(5) / 5, mode='same')
    peaks = []
    for i in range(2, len(sm) - 2):
        if sm[i] >= sm[i - 1] and sm[i] >= sm[i + 1] and sm[i] > 2.5 and sm[i] >= sm[i - 2] and sm[i] >= sm[i + 2]:
            peaks.append(edges[i] + 4)
    lines = []
    for p in peaks:
        if lines and p - lines[-1] < 60: lines[-1] = (lines[-1] + p) / 2
        else: lines.append(p)
    pitch = float(np.median(np.diff(lines))) if len(lines) > 1 else 112.0
    for c in comps:
        d = np.abs(np.array(lines) - (c['y0'] + c['y1']) / 2)
        k = int(np.argmin(d)); c['line'] = k if d[k] < pitch * 0.55 else -1
    tokens = []
    for k in range(len(lines)):
        cs = sorted([c for c in comps if c['line'] == k], key=lambda c: c['x0'])
        merged = []
        for c in cs:
            if merged:
                m = merged[-1]
                ov = min(m['x1'], c['x1']) - max(m['x0'], c['x0'])
                wmin = min(m['x1'] - m['x0'], c['x1'] - c['x0'])
                if ov > 0.5 * wmin:
                    m['x0'] = min(m['x0'], c['x0']); m['x1'] = max(m['x1'], c['x1'])
                    m['y0'] = min(m['y0'], c['y0']); m['y1'] = max(m['y1'], c['y1']); m['ids'].append(c['id']); m['s'] += c['s']
                    continue
            merged.append(dict(x0=c['x0'], x1=c['x1'], y0=c['y0'], y1=c['y1'], s=c['s'], ids=[c['id']], line=k, page=name))
        tokens.extend(merged)
    print(name, 'comps', len(comps), 'lines', len(lines), 'pitch', round(pitch), 'tokens', len(tokens))
    for t in tokens:
        m = np.isin(lab[t['y0']:t['y1'], t['x0']:t['x1']], t['ids']).astype(float)
        h, w = m.shape; sc = SZ / max(h, w)
        pm = Image.fromarray((m * 255).astype(np.uint8)).resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.BILINEAR)
        canvas = Image.new('L', (SZ, SZ), 0); canvas.paste(pm, ((SZ - pm.width) // 2, (SZ - pm.height) // 2))
        a = gaussian_filter(np.array(canvas).astype(float) / 255.0, 1.0).ravel()
        lc = lines[t['line']]
        geo = np.array([(t['y0'] - lc) / pitch, (t['y1'] - lc) / pitch, (t['x1'] - t['x0']) / pitch, (t['y1'] - t['y0']) / pitch]) * 6.0
        feats.append(np.concatenate([a, geo]))
        t.pop('ids')
    alltoks.extend(tokens)
    regs[name] = dict(lines=[float(l) for l in lines], pitch=pitch, x0=x0, y0=y0, img=img)
X = np.array(feats)
Z = linkage(X, 'ward')
cl = fcluster(Z, NCL, criterion='maxclust')
for t, c in zip(alltoks, cl): t['cl'] = int(c)
json.dump(dict(regions=regs, tokens=alltoks), open(f'{OUT}_tokens.json', 'w'))
# cipher file
with open(f'{OUT}_cipher.txt', 'w') as f:
    f.write('# Raince fr.2984 cluster ids\n')
    for name in regs:
        nl = len(regs[name]['lines'])
        for k in range(nl):
            f.write(';'.join(f'{t["cl"]:02d}' for t in alltoks if t['page'] == name and t['line'] == k) + '\n')
# montages
imgs = {name: Image.open(regs[name]['img']).convert('RGB') for name in regs}
font = ImageFont.truetype('arial.ttf', 28)
cell = 70; ncol = 20; per = 6
ids = list(range(1, NCL + 1))
for s in range(0, NCL, per):
    sheet = Image.new('RGB', (ncol * cell + 80, per * 240), (255, 255, 255)); d = ImageDraw.Draw(sheet)
    for i, c in enumerate(ids[s:s + per]):
        ts = [t for t in alltoks if t['cl'] == c][:ncol * 3]
        for j, t in enumerate(ts):
            r = regs[t['page']]; cx = r['x0'] + (t['x0'] + t['x1']) // 2; cy = int(r['y0'] + r['lines'][t['line']])
            patch = imgs[t['page']].crop((cx - 32, cy - 45, cx + 32, cy + 25)).resize((cell, cell))
            sheet.paste(patch, (80 + (j % ncol) * cell, i * 240 + (j // ncol) * cell))
        d.text((5, i * 240 + 80), f'{c:02d}', fill=(255, 0, 0), font=font)
    sheet.save(f'{OUT}_sheet_{s // per:02d}.png')
sizes = sorted([(int((cl == c).sum()), c) for c in range(1, NCL + 1)], reverse=True)
print('total tokens', len(alltoks)); print(sizes)
