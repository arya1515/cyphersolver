"""zoom.py PAGE LINE FRAC0 FRAC1 [Z] -> img/zoom.png : crop a fraction of one line's x-extent."""
import json, sys
from PIL import Image
d = json.load(open('raince_tokens.json'))
page, ln = sys.argv[1], int(sys.argv[2])
f0, f1 = float(sys.argv[3]), float(sys.argv[4])
Z = float(sys.argv[5]) if len(sys.argv) > 5 else 3.5
r = d['regions'][page]; toks = [t for t in d['tokens'] if t['page'] == page]
x0 = r['x0'] + min(t['x0'] for t in toks) - 25; x1 = r['x0'] + max(t['x1'] for t in toks) + 25
W = x1 - x0; pitch = r['pitch']; y = int(r['y0'] + r['lines'][ln-1])
im = Image.open(r['img']).convert('L')
c = im.crop((int(x0 + f0*W), int(y - pitch*0.85), int(x0 + f1*W), int(y + pitch*0.55)))
c = c.resize((int(c.width*Z), int(c.height*Z)), Image.LANCZOS)
c.save('img/zoom.png'); print(c.size)
