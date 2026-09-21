"""Test graphic template retrieval on two known K occurrences; no decoding."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

ROOT = Path(__file__).resolve().parent
source = Image.open(ROOT/'img/IMG_R1102_I5657_P2.png').convert('L')
small = source.resize((1080,810))
a = np.asarray(small, dtype=float)
background = np.asarray(small.filter(ImageFilter.GaussianBlur(5)), dtype=float)
a = np.maximum(background-a, 0)
x0,y0,x1,y1 = 421,618,490,638
t = a[y0:y1,x0:x1].copy()
t -= t.mean()
h,w = t.shape
shape = (a.shape[0]+h-1,a.shape[1]+w-1)
c = np.fft.irfft2(np.fft.rfft2(a,s=shape)*np.fft.rfft2(t[::-1,::-1],s=shape),s=shape)
c = c[h-1:a.shape[0],w-1:a.shape[1]]
def window_sum(v):
    s=np.pad(v,((1,0),(1,0))).cumsum(0).cumsum(1)
    return s[h:,w:]-s[:-h,w:]-s[h:,:-w]+s[:-h,:-w]
variance=np.maximum(window_sum(a*a)-window_sum(a)**2/(h*w),0)
scores=c/np.maximum(np.sqrt(variance*np.sum(t*t)),1e-8)
peaks=[]
for _ in range(30):
    y,x=np.unravel_index(np.argmax(scores),scores.shape)
    peaks.append({'score':round(float(scores[y,x]),4),'box':[int(x*4),int(y*4),int((x+w)*4),int((y+h)*4)]})
    scores[max(0,y-h):y+h,max(0,x-w):x+w]=-1
target=(3565,1300,3840,1375)
hit=[(i+1,p) for i,p in enumerate(peaks) if abs(p['box'][0]-target[0])<80 and abs(p['box'][1]-target[1])<45]
result={'method':'quarter-resolution local-darkness normalized cross correlation, one scale, 30 suppressed peaks','template_box':[x0*4,y0*4,x1*4,y1*4],'known_second_box':list(target),'known_second_hits':hit,'peaks':peaks}
(ROOT/'k_template_test.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'known_second_hits':hit,'top_scores':[p['score'] for p in peaks[:5]]}))
