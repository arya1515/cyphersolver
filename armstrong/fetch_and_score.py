"""Fetch every frame of M34 roll 13 from the NARA catalogue proxy, score it for faint pencil
(same score as pencil_score.py), keep only a 1600-px thumbnail, and write the full ranking.

Usage: python fetch_and_score.py img13/objects.json img13/thumbs pencil_ranking.tsv
Frames already present in img13/ are scored from there without downloading.
"""
import sys, os, json, time, io
import requests
import numpy as np
from PIL import Image, ImageFilter

def score_image(im):
    im = im.convert('L'); im.thumbnail((1600, 1600))
    a = np.asarray(im)
    dark = Image.fromarray(((a < 100) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(9))
    near = np.asarray(dark) > 0
    pencil = (a >= 110) & (a < 200) & ~near
    paper = (a >= 200).mean()
    return float(pencil.mean()), float(paper), im

def main(manifest, thumbdir, out):
    objs = json.load(open(manifest))
    os.makedirs(thumbdir, exist_ok=True)
    local = os.path.dirname(manifest)
    rows = []
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (research; pencil-score)'
    for size, url, name in objs:
        thumb = os.path.join(thumbdir, name.replace('.jpg', '.png'))
        try:
            if os.path.exists(thumb):
                im = Image.open(thumb)
            elif os.path.exists(os.path.join(local, name)):
                im = Image.open(os.path.join(local, name))
            else:
                for attempt in range(3):
                    r = s.get(url, timeout=120)
                    if r.status_code == 200 and len(r.content) > 10000:
                        break
                    time.sleep(3)
                else:
                    print('FAIL', name, r.status_code, flush=True); continue
                im = Image.open(io.BytesIO(r.content))
            sc, paper, small = score_image(im)
            if not os.path.exists(thumb):
                small.save(thumb)
            rows.append((sc, paper, name))
            print(f'{name}\t{sc:.5f}\t{paper:.3f}', flush=True)
        except Exception as e:
            print('ERR', name, e, flush=True)
    rows.sort(reverse=True)
    with open(out, 'w') as f:
        f.write('# frame\tpencil\tpaper\trank\n')
        for i, (sc, paper, name) in enumerate(rows, 1):
            f.write(f'{name}\t{sc:.5f}\t{paper:.3f}\t{i}\n')
    print('done', len(rows), 'of', len(objs))

if __name__ == '__main__':
    main(*sys.argv[1:4])
