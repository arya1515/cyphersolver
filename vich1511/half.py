import sys, os
from PIL import Image, ImageOps
from lines import peaks
import numpy as np
fn, tag = sys.argv[1], sys.argv[2]; y0 = int(sys.argv[3]); y1 = int(sys.argv[4]) if len(sys.argv) > 4 else None
im = ImageOps.autocontrast(Image.open(fn).convert('L'), cutoff=1); a = np.asarray(im); W, H = im.size
P = peaks(a, 32, 125, W-60, y0, y1 or H-80)
os.makedirs('half', exist_ok=True)
for n, p in enumerate(P):
    c = im.crop((85, p-24, W-15, p+22)); w = c.width//2 + 25
    for h, (x, y) in enumerate([(0, w), (c.width-w, c.width)]):
        d = c.crop((x, 0, y, c.height)); d = d.resize((d.width*3, d.height*3), Image.LANCZOS)
        d.save(f'half/{tag}_{n+1:02d}{"ab"[h]}.png')
print(len(P))
