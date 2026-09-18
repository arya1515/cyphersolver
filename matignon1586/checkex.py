"""Audit the labelled exemplars: does any single figure shape carry two different letters?

The labels come from the plaintext, so they are right by construction. What can go wrong is the
segmentation - a box holding two figures, or one figure split across two boxes - and that shows up
as two exemplars that look alike but carry different letters. This compares every pair by
normalised correlation and reports the look-alikes that disagree.
"""
import json, itertools
import numpy as np
from PIL import Image, ImageFilter

S = 26
def vec(path):
    g = Image.open(path).convert('L')
    a = np.asarray(g, dtype=np.float32)
    a = 255 - a
    if a.max() > 0: a = a / a.max()
    h, w = a.shape
    sc = (S - 4) / max(h, w)
    g = Image.fromarray((a * 255).astype(np.uint8)).resize(
        (max(1, int(w * sc)), max(1, int(h * sc))), Image.BILINEAR)
    canv = Image.new('L', (S, S), 0)
    canv.paste(g, ((S - g.width) // 2, (S - g.height) // 2))
    canv = canv.filter(ImageFilter.GaussianBlur(1.1))
    v = np.asarray(canv, dtype=np.float32).ravel()
    v -= v.mean()
    n = np.linalg.norm(v)
    return v / (n or 1.0)

if __name__ == '__main__':
    man = json.load(open('exemplars/manifest.json'))
    V = {m['file']: vec(m['file']) for m in man}
    L = {m['file']: m['letter'] for m in man}
    rows = []
    for a, b in itertools.combinations(sorted(V), 2):
        s = float(V[a] @ V[b])
        rows.append((s, a, b))
    rows.sort(reverse=True)
    print('most similar pairs:')
    bad = 0
    for s, a, b in rows[:14]:
        same = L[a] == L[b]
        flag = '' if same else '   <-- same shape, different letters'
        if not same and s > 0.80: bad += 1
        print(f'  {s:.3f}  {L[a]:>2} {a.split("/")[-1]:<28} {L[b]:>2} {b.split("/")[-1]:<28}{flag}')
    print()
    print('look-alike pairs above 0.80 that disagree on the letter:', bad)
