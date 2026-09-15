"""Make reduced copies / crops of the manuscript images.
usage: python imgprep.py small            -> img/small_NN.jpg (width 1400)
       python imgprep.py crop NN x0 y0 x1 y1 [scale]  (fractions 0-1) -> img/crop_NN_<x0>_<y0>.jpg
"""
import sys, os
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
mode = sys.argv[1]
if mode == "small":
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 1400
    for i in range(1, 9):
        im = Image.open(f"img/stepney_{i:02d}.jpg")
        print(i, im.size)
        r = w / im.size[0]
        im2 = im.resize((w, int(im.size[1] * r)), Image.LANCZOS)
        im2.save(f"img/small_{i:02d}.jpg", quality=80)
elif mode == "crop":
    n = int(sys.argv[2]); x0, y0, x1, y1 = map(float, sys.argv[3:7])
    scale = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
    im = Image.open(f"img/stepney_{n:02d}.jpg")
    W, H = im.size
    box = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
    c = im.crop(box)
    if scale != 1.0:
        c = c.resize((int(c.size[0] * scale), int(c.size[1] * scale)), Image.LANCZOS)
    out = f"img/crop_{n:02d}_{int(x0*100)}_{int(y0*100)}_{int(x1*100)}_{int(y1*100)}.jpg"
    c.save(out, quality=85)
    print(out, c.size)
