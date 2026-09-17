# Parse the MDZ hOCR of scans 329-376 and list numeric words with low OCR confidence (x_wconf), with their
# bounding boxes, so the doubtful groups can be checked against the page images in img/.
import re, os, html, json
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for s in range(329, 377):
    fn = os.path.join(HERE, 'hocr', '%d.html' % s)
    if not os.path.exists(fn):
        continue
    t = open(fn, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r"<span class=['\"]ocrx_word['\"][^>]*title=['\"]bbox (\d+) (\d+) (\d+) (\d+); x_wconf (\d+)['\"][^>]*>(.*?)</span>", t, re.S):
        x0, y0, x1, y1, conf, inner = m.groups()
        w = html.unescape(re.sub(r'<[^>]+>', '', inner)).strip()
        if re.search(r'\d', w):
            rows.append({'scan': s, 'page': s - 34, 'word': w, 'conf': int(conf), 'bbox': [int(x0), int(y0), int(x1), int(y1)]})
json.dump(rows, open(os.path.join(HERE, 'hocr_numwords.json'), 'w'))
print('numeric words', len(rows))
import collections
c = collections.Counter()
for r in rows:
    c[r['conf'] // 10 * 10] += 1
print('confidence histogram', sorted(c.items()))
low = [r for r in rows if r['conf'] < 70]
print('below 70:', len(low))
for r in low[:40]:
    print(r)
