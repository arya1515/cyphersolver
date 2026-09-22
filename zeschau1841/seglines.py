# Cut each page image into text-line strips (for transcription)
import sys, numpy as np
from PIL import Image
f, x0, x1, y0, y1, tag = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
im = Image.open(f).convert('L').crop((x0, y0, x1, y1))
a = np.asarray(im).astype(float)
ink = (a < 110).sum(1)
sm = np.convolve(ink, np.ones(25)/25, 'same')
on = sm > max(8, sm.max()*0.12)
runs=[]; i=0
while i < len(on):
    if on[i]:
        j=i
        while j < len(on) and on[j]: j+=1
        if j-i > 40: runs.append((i,j))
        i=j
    else: i+=1
for k,(i,j) in enumerate(runs):
    s=im.crop((0,max(0,i-60),im.width,min(im.height,j+60)))
    s.thumbnail((2400,400)); s.save(f'img/lines/{tag}_{k:02d}.png')
print(tag, len(runs), [ (i+y0,j+y0) for i,j in runs])
