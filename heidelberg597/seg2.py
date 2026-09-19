import sys, numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
from scipy import ndimage
def segment_nostrike(im, box, thr=130, mingap=3, minw=5):
    g=np.asarray(ImageOps.grayscale(im).crop(box)); b=g<thr
    # remove long horizontal runs (strike-through)
    horiz=ndimage.binary_opening(b,structure=np.ones((1,45)))
    horiz=ndimage.binary_dilation(horiz,structure=np.ones((3,1)))
    b2=b&~horiz
    col=b2.sum(axis=0)
    segs=[];s=None;gap=0
    for x,v in enumerate(col):
        if v>0:
            if s is None: s=x
            gap=0
        else:
            if s is not None:
                gap+=1
                if gap>=mingap:
                    if x-gap-s>=minw: segs.append((s,x-gap))
                    s=None;gap=0
    if s is not None: segs.append((s,len(col)))
    return segs,b2
def sheet(im,box,out,scale=6,thr=130,labels=None):
    segs,b2=segment_nostrike(im,box,thr)
    W=box[2]-box[0];H=box[3]-box[1]
    c=im.crop(box).resize((W*scale,H*scale),Image.LANCZOS)
    clean=Image.fromarray((~b2*255).astype('uint8')).resize((W*scale,H*scale),Image.NEAREST).convert('RGB')
    out_im=Image.new('RGB',(W*scale,H*scale*2+40),'white'); out_im.paste(c,(0,0)); out_im.paste(clean,(0,H*scale+40))
    d=ImageDraw.Draw(out_im); font=ImageFont.truetype("arial.ttf",26)
    for i,(a,b) in enumerate(segs):
        d.rectangle((a*scale,H*scale+40,b*scale,H*scale*2+40),outline='red')
        lab=str(i+1) if not labels else (labels[i] if i<len(labels) else '?')
        d.text((a*scale,H*scale+5),lab,fill='blue',font=font)
    out_im.save(out); print(out,len(segs),segs)
if __name__=='__main__':
    f=sys.argv[1]; box=tuple(map(int,sys.argv[2:6])); out=sys.argv[6]
    sheet(Image.open(f"img/{f}.jpg"),box,out)
