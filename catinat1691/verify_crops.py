# Find groups whose decode yields unsegmentable French (likely OCR misreads), crop them from the page images and
# build labelled contact sheets in crops/ for eyeballing. Output list in suspects.json.
import re, json, os, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segment
from extract3 import unit_text, tab   # noqa (re-runs extraction; cheap)
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, 'groups.json')))
suspects = []   # dict(letter, scan, idxs(list of indices into G), why)
# 1. runs of code groups -> segmentation -> unknown words >= 4 chars
i = 0
while i < len(G):
    if G[i]['kind'] != 'num' or G[i]['dec'] in (None, '?', 'NULL', 'CANCEL'):
        if G[i]['kind'] == 'bad' or (G[i]['kind'] == 'num' and G[i]['dec'] is None):
            suspects.append({'idxs': [i], 'why': 'OCR ' + G[i]['text']})
        i += 1; continue
    j = i; run = ''; owner = []
    while j < len(G) and G[j]['kind'] == 'num' and G[j]['dec'] not in (None, '?', 'NULL', 'CANCEL'):
        nrm, dsp = unit_text(G[j]['dec']); run += nrm; owner += [j] * len(nrm); j += 1
    if run:
        pos = 0
        for w in segment.seg(run):
            if len(w) >= 4 and segment.LEX.get(w) is None:
                idxs = sorted(set(owner[pos:pos + len(w)]))
                suspects.append({'idxs': idxs, 'why': 'unsegmentable ' + w})
            pos += len(w)
    i = j
# merge suspects that overlap / are adjacent
suspects.sort(key=lambda s: s['idxs'][0])
merged = []
for s in suspects:
    if merged and s['idxs'][0] <= merged[-1]['idxs'][-1] + 1:
        merged[-1]['idxs'] = sorted(set(merged[-1]['idxs'] + s['idxs'])); merged[-1]['why'] += '; ' + s['why']
    else:
        merged.append(dict(s))
print('suspect clusters', len(merged))
os.makedirs(os.path.join(HERE, 'crops'), exist_ok=True)
font = ImageFont.load_default()
sheet = []; sheetno = 0
imgs = {}


def img(scan):
    if scan not in imgs:
        imgs[scan] = Image.open(os.path.join(HERE, 'img', 't2_%04d.jpg' % scan)).convert('RGB')
    return imgs[scan]


out = []
for k, s in enumerate(merged):
    idxs = s['idxs']
    lo = max(0, idxs[0] - 2); hi = min(len(G) - 1, idxs[-1] + 2)
    ctx = [G[t] for t in range(lo, hi + 1) if G[t]['scan'] == G[idxs[0]]['scan']]
    scan = G[idxs[0]]['scan']
    bbs = [g['bbox'] for g in ctx]
    x0 = min(b[0] for b in bbs) - 12; y0 = min(b[1] for b in bbs) - 10; x1 = max(b[2] for b in bbs) + 12; y1 = max(b[3] for b in bbs) + 10
    im = img(scan)
    if y1 - y0 > 140:   # spans lines: take just the suspect groups' own line(s)
        bbs = [G[t]['bbox'] for t in idxs]
        x0 = min(b[0] for b in bbs) - 60; y0 = min(b[1] for b in bbs) - 10; x1 = max(b[2] for b in bbs) + 60; y1 = max(b[3] for b in bbs) + 10
    crop = im.crop((max(0, x0), max(0, y0), min(im.width, x1), min(im.height, y1)))
    # highlight suspect boxes
    dr = ImageDraw.Draw(crop)
    for t in idxs:
        b = G[t]['bbox']; dr.rectangle([b[0] - x0, b[1] - y0, b[2] - x0, b[3] - y0], outline=(255, 0, 0), width=3)
    label = '#%d p.%d %s | OCR: %s | dec: %s' % (k, scan - 34, s['why'][:60], ' '.join(G[t]['text'] for t in idxs), ' '.join(str(G[t]['dec']) for t in idxs))
    lab = Image.new('RGB', (max(crop.width, 900), crop.height + 22), (255, 255, 255)); lab.paste(crop, (0, 22))
    ImageDraw.Draw(lab).text((4, 4), label[:150], fill=(0, 0, 0), font=font)
    sheet.append(lab)
    out.append({'k': k, 'scan': scan, 'page': scan - 34, 'idxs': idxs, 'why': s['why'], 'ocr': [G[t]['text'] for t in idxs], 'bbox': [G[t]['bbox'] for t in idxs], 'dec': [G[t]['dec'] for t in idxs]})
    if len(sheet) == 10 or k == len(merged) - 1:
        W = max(x.width for x in sheet); H = sum(x.height for x in sheet)
        S = Image.new('RGB', (W, H), (255, 255, 255)); y = 0
        for x in sheet:
            S.paste(x, (0, y)); y += x.height
        S.save(os.path.join(HERE, 'crops', 'sheet_%02d.png' % sheetno)); sheetno += 1; sheet = []
json.dump(out, open(os.path.join(HERE, 'suspects.json'), 'w'), indent=0)
print('sheets', sheetno)
