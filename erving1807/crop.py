"""crop.py frame x0 y0 x1 y1 out  (fractions of full image), saves at full res (max 1800 wide)"""
import sys
from PIL import Image
f, a, b, c, d, out = sys.argv[1], *map(float, sys.argv[2:6]), sys.argv[6]
im = Image.open(f).convert('L'); W, H = im.size
im = im.crop((int(a*W), int(b*H), int(c*W), int(d*H)))
if im.width > 1800: im = im.resize((1800, int(im.height*1800/im.width)))
im.save(out)
