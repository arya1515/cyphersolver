# Flag openings of BnF fr. 3251 with figure-string lines. Calibrated on view 120: at threshold 170 the seven cipher lines have
# >= 50 components of median width <= 0.43 x line height and no word-long components; the letter's text lines do not.
import sys,glob,numpy as np
from PIL import Image
from scipy import ndimage
def digit_lines(sub):
    ink=sub<170; rows=ink.sum(1); base=np.percentile(rows,30); on=rows>base+8
    lines=[];s=None
    for i,v in enumerate(on):
        if v and s is None: s=i
        if not v and s is not None:
            if i-s>8: lines.append((s,i))
            s=None
    hits=[]
    for (y0,y1) in lines:
        lab,n=ndimage.label(ink[y0:y1]); objs=ndimage.find_objects(lab); h=y1-y0
        if n<50: continue
        ws=np.array([o[1].stop-o[1].start for o in objs]); hs=np.array([o[0].stop-o[0].start for o in objs]); big=hs>0.35*h
        if big.sum()<50: continue
        medw=np.median(ws[big])/h; wide=float((ws[big]>2.0*h).mean())
        if medw<=0.43 and wide<=0.01: hits.append((y0,y1,int(big.sum()),round(float(medw),2)))
    return hits
if __name__=='__main__':
    files=sorted(glob.glob(sys.argv[1] if len(sys.argv)>1 else 'scan/v*.jpg'))
    for f in files:
        try: a=np.array(Image.open(f).convert('L'))
        except Exception: print(f,'unreadable'); continue
        W=a.shape[1]; res=[]
        for half,(x0,x1) in enumerate(((int(0.10*W),int(0.45*W)),(int(0.56*W),int(0.92*W)))):
            for h in digit_lines(a[:,x0:x1]): res.append((half,)+h)
        if res: print(f,len(res),'figure-like lines',res[:8],flush=True)
    print('scanned',len(files))
