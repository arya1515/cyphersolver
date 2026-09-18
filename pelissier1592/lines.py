import sys, numpy as np
from PIL import Image
c=int(sys.argv[1])
im=np.asarray(Image.open(f'img/c{c}.jpg').convert('L')).astype(float)
H,W=im.shape
# text column: find page area
ink=(im<110)
cols=ink[:, :].sum(0)
x=np.where(cols>H*0.01)[0]
row=ink[:, int(W*0.1):int(W*0.9)].sum(1)
k=25; sm=np.convolve(row,np.ones(k)/k,'same')
thr=np.percentile(sm,60)*0.35+1
# find minima between lines
from scipy.signal import find_peaks
pk,_=find_peaks(sm,distance=70,prominence=sm.max()*0.08)
print(len(pk), list(pk))
