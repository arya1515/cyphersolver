"""Cut lines at given centres: python cutmanual.py <tag> <halfheight> y1 y2 ... (on img/<tag>_clean.png; refines each
centre to the local ink maximum within +-10 px). Writes img/lines/<tag>_lNN.png labelled full-width crops."""
import sys, os
from PIL import Image, ImageDraw
import numpy as np
tag = sys.argv[1]; hh = int(sys.argv[2]); ys = [int(v) for v in sys.argv[3:]]
im = Image.open('img/%s_clean.png' % tag); a = np.array(im.convert('L')); w = im.width
sm = np.convolve((a < 100).sum(1).astype(float), np.ones(15) / 15, mode='same')
for f in os.listdir('img/lines'):
    if f.startswith(tag + '_l'): os.remove(os.path.join('img/lines', f))
out = []
for i, y in enumerate(ys):
    y = int(max(y - 10, 0) + np.argmax(sm[max(y - 10, 0):y + 10])); out.append(y)
    c = im.crop((0, max(y - hh, 0), w, min(y + hh, im.height))); sc = 2000.0 / w
    cc = c.resize((int(w * sc), int(c.height * sc)), Image.LANCZOS).convert('RGB')
    d = ImageDraw.Draw(cc); d.rectangle([0, 0, 120, 22], fill=(255, 255, 255)); d.text((4, 4), '%s l%02d' % (tag, i + 1), fill=(200, 0, 0))
    cc.save('img/lines/%s_l%02d.png' % (tag, i + 1))
print(tag, out)
