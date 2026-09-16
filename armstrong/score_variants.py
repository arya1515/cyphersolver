"""Compare pencil-score variants on the roll 13 thumbnails: which one ranks the frames with
interlinear pencil decodes at the top?  Writes score_variants.tsv (frame, variant scores) and prints
the rank of each known annotated frame under each variant.

Variants
  v1  original pencil_score.py: mid-grey (110-200) pixels not within 4 px of ink, whole frame
  v3b same, grey defined relative to the page background, bright pages only (bg >= 215)
  v5  grey relative to background, counted only in the interlinear band (4-20 px from ink), as a fraction of the band
  v6  v5 restricted to rows that contain ink (the text block), bright pages only
"""
import glob, os, sys
import numpy as np
from PIL import Image, ImageFilter

ANN = {'0149', '0190', '0192', '0193', '0194', '0195', '0196', '0197', '0198', '0199', '0200', '0201'}

def feats(p):
    im = Image.open(p).convert('L'); im.thumbnail((800, 800))
    a = np.asarray(im).astype(np.int16)
    ink = a < 100
    inkimg = Image.fromarray((ink * 255).astype('uint8'))
    near = np.asarray(inkimg.filter(ImageFilter.MaxFilter(5))) > 0
    wide = np.asarray(inkimg.filter(ImageFilter.MaxFilter(21))) > 0
    band = wide & ~near
    bg = float(np.median(a[~near])) if (~near).any() else 255.0
    v1 = float(((a >= 110) & (a < 200) & ~near).mean())
    grey = (a >= bg - 90) & (a < bg - 25)
    v3 = float((grey & ~near).mean())
    v3b = v3 if bg >= 215 else 0.0
    v5 = float((grey & band).sum() / max(band.sum(), 1))
    rows = ink.mean(axis=1) > 0.01
    region = np.zeros_like(ink); region[rows, :] = True
    v6 = float((grey & band & region).sum() / max((band & region).sum(), 1))
    v6 = v6 if bg >= 215 else 0.0
    return bg, v1, v3b, v5, v6

names = ['bg', 'v1', 'v3b', 'v5', 'v6']
rows = []
for p in sorted(glob.glob('img13/thumbs/M34-013-*.png')):
    rows.append((os.path.basename(p)[8:12],) + feats(p))
    print('.', end='', flush=True)
print()
with open('score_variants.tsv', 'w') as f:
    f.write('frame\t' + '\t'.join(names) + '\n')
    for r in rows:
        f.write(r[0] + '\t' + '\t'.join(f'{x:.5f}' for x in r[1:]) + '\n')
for i, name in enumerate(names[1:], start=2):
    order = sorted(rows, key=lambda r: -r[i])
    ranks = {r[0]: k for k, r in enumerate(order, 1)}
    print(f'{name:4s} annotated ranks {sorted(ranks[a] for a in ANN if a in ranks)}')
    print('     top 20', [(r[0], round(r[i], 3)) for r in order[:20]])
