"""Score images for faint pencil annotations: mid-gray pixels that are NOT adjacent to dark ink."""
import sys, glob, os
import numpy as np
from PIL import Image, ImageFilter
def score(p):
    im = Image.open(p).convert('L'); im.thumbnail((1600, 1600))
    a = np.asarray(im)
    dark = Image.fromarray(((a < 100) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(9))
    near = np.asarray(dark) > 0
    pencil = (a >= 110) & (a < 200) & ~near
    paper = (a >= 200).mean()
    return pencil.mean(), paper
if __name__ == '__main__':
    rows = []
    for p in sorted(glob.glob(sys.argv[1] + '/*.jpg')):
        try: s, paper = score(p)
        except Exception: continue
        rows.append((s, paper, os.path.basename(p)))
    rows.sort(reverse=True)
    for r in rows[:int(sys.argv[2]) if len(sys.argv) > 2 else 40]:
        print(f"{r[2]} pencil {r[0]:.4f} paper {r[1]:.3f}")
    print('n', len(rows))
