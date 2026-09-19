import sys, numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
from scipy import ndimage
def segment(im, box, thr=110, gap=6):
    g=np.asarray(ImageOps.grayscale(im).crop(box))
    b=g<thr
    b=ndimage.binary_closing(b,iterations=1)
    lab,n=ndimage.label(b)
    objs=ndimage.find_objects(lab)
    comps=[(s[1].start,s[1].stop,s[0].start,s[0].stop) for s in objs if (s[1].stop-s[1].start)*(s[0].stop-s[0].start)>=12]
    comps.sort()
    # merge horizontally overlapping components (dots over glyphs)
    merged=[]
    for c in comps:
        if merged and c[0] < merged[-1][1]-2:
            m=merged[-1]; merged[-1]=(min(m[0],c[0]),max(m[1],c[1]),min(m[2],c[2]),max(m[3],c[3]))
        else: merged.append(c)
    return merged
def sheet(im, box, out, scale=6, thr=110):
    comps=segment(im,box,thr)
    x0,y0=box[0],box[1]
    c=im.crop(box).resize(((box[2]-box[0])*scale,(box[3]-box[1])*scale),Image.LANCZOS)
    d=ImageDraw.Draw(c)
    try: font=ImageFont.truetype("arial.ttf",26)
    except: font=ImageFont.load_default()
    for i,(a,b,t,bt) in enumerate(comps):
        d.rectangle((a*scale,t*scale,b*scale,bt*scale),outline='red')
        d.text((a*scale,(box[3]-box[1])*scale-30 if i%2 else 0),str(i+1),fill='blue',font=font)
    c.save(out); print(out,len(comps),[ (a,b) for a,b,_,_ in comps])
if __name__=='__main__':
    f=sys.argv[1]; box=tuple(map(int,sys.argv[2:6])); out=sys.argv[6]
    sheet(Image.open(f"img/{f}.jpg"),box,out)
