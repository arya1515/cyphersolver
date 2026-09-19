import sys, numpy as np
from PIL import Image, ImageOps
def peaks(im,x0,x1,y0,y1,mind=28,half=24):
    g=np.asarray(ImageOps.grayscale(im).crop((x0,y0,x1,y1)),dtype=float)
    ink=(g<120).mean(axis=1)
    k=np.ones(9)/9; sm=np.convolve(ink,k,'same')
    idx=[i for i in range(1,len(sm)-1) if sm[i]>=sm[i-1] and sm[i]>=sm[i+1] and sm[i]>0.05]
    # suppress close peaks
    idx.sort(key=lambda i:-sm[i]); kept=[]
    for i in idx:
        if all(abs(i-j)>=mind for j in kept): kept.append(i)
    kept.sort()
    return [(y0+i-half,y0+i+half) for i in kept]
if __name__=='__main__':
    f=sys.argv[1]; x0,x1,y0,y1=map(int,sys.argv[2:6]); scale=int(sys.argv[6]) if len(sys.argv)>6 else 4
    im=Image.open(f"img/{f}.jpg")
    bs=peaks(im,x0,x1,y0,y1)
    print(f,len(bs),bs)
    segw=2000//scale
    import glob,os
    for p in glob.glob(f"crops/{f}_line*"): os.remove(p)
    for i,(a,b) in enumerate(bs):
        n=0
        for sx in range(x0,x1,segw-40):
            box=(sx,a,min(sx+segw,x1),b)
            if box[2]-box[0]<60: break
            c=im.crop(box); c=c.resize((c.width*scale,c.height*scale),Image.LANCZOS)
            c.save(f"crops/{f}_line{i+1:02d}_{n}.png"); n+=1
