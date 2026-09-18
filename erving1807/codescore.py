"""Score frames for 'numeric code' texture: many small, isolated, compact ink blobs.
python codescore.py imgdir out.tsv"""
import sys, glob, os
import numpy as np
from PIL import Image
from scipy import ndimage
def score(f):
    im = Image.open(f).convert('L'); im.thumbnail((1400, 1400))
    a = np.asarray(im).astype(float)
    bg = ndimage.uniform_filter(a, 41)
    ink = (a < bg - 35)
    ink = ndimage.binary_opening(ink, iterations=1)
    lab, n = ndimage.label(ink)
    if n == 0: return 0, 0, 0
    sl = ndimage.find_objects(lab)
    sizes = ndimage.sum(ink, lab, range(1, n+1))
    small = 0; big = 0
    for s, sz in zip(sl, sizes):
        h = s[0].stop - s[0].start; w = s[1].stop - s[1].start
        if 25 <= sz <= 400 and 6 <= h <= 30 and w <= 30: small += 1
        elif sz > 400: big += 1
    tot = ink.sum()
    return small, big, small / (big + 1)
out = open(sys.argv[2], 'w')
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.jpg'))):
    s, b, r = score(f)
    out.write(f'{os.path.basename(f)}\t{s}\t{b}\t{r:.2f}\n'); out.flush()
