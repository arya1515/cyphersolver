import sys,json,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as nd
def otsu(a):
    h,_=np.histogram(a,256,(0,256)); p=h/h.sum(); w=np.cumsum(p); m=np.cumsum(p*np.arange(256)); mt=m[-1]
    s=(mt*w-m)**2/(w*(1-w)+1e-12); return int(np.argmax(s))
def segment(c,box,scale=0.5):
    im=Image.open(f'hi/c{c}.jpg').convert('L'); W=im.width; s=W/1000
    x0,y0,x1,y1=[int(v*s) for v in box]
    im=im.crop((x0,y0,x1,y1)); im=im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS)
    a=np.asarray(im,dtype=float)
    bg=nd.uniform_filter(a,61); a2=a-bg+200
    t=otsu(np.clip(a2,0,255)); bw=a2<t-15
    bw=nd.binary_opening(bw,np.ones((2,2)))
    lab,n=nd.label(bw,np.ones((3,3)))
    objs=nd.find_objects(lab)
    comps=[]
    for i,sl in enumerate(objs):
        ys,xs=sl; area=(lab[sl]==i+1).sum()
        if area<12: continue
        comps.append(dict(id=i+1,x0=xs.start,x1=xs.stop,y0=ys.start,y1=ys.stop,area=int(area)))
    return im,bw,lab,comps
if __name__=='__main__':
    c=sys.argv[1]; box=[int(v) for v in sys.argv[2:6]]
    im,bw,lab,comps=segment(c,box)
    print(len(comps), np.median([d['y1']-d['y0'] for d in comps]), np.median([d['x1']-d['x0'] for d in comps]))
    ov=im.convert('RGB'); d=ImageDraw.Draw(ov)
    for q in comps: d.rectangle((q['x0'],q['y0'],q['x1'],q['y1']),outline='red')
    ov.save(f'ov_{c}.jpg')
