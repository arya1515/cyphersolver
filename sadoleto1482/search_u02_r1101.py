"""Candidate-only U02 search in observed R1101 writing regions."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

ROOT=Path(__file__).resolve().parent
def ink(image):
    g=image.convert('L')
    return np.maximum(np.asarray(g.filter(ImageFilter.GaussianBlur(5)),float)-np.asarray(g,float),0)
ref=Image.open(ROOT/'img/IMG_R1102_I5657_P2.png').resize((1080,810))
base=ink(ref)[631:652,157:217]
jobs={
 'I5654':('IMG_R1101_I5654_P1.png',[(180,700,2130,2950),(2280,430,4040,1070),(2260,2200,4140,3020)]),
 'I5655':('IMG_R1101_I5655_P2.png',[(1090,215,3230,2300)])
}
result={}
for name,(filename,regions) in jobs.items():
    source=Image.open(ROOT/'img'/filename)
    a=ink(source.resize((1080,810)))
    candidates=[]
    for scale in (0.8,1.,1.2):
        t=np.asarray(Image.fromarray(base.astype('float32')).resize((round(60*scale),round(21*scale))),float)
        t-=t.mean()
        h,w=t.shape
        shape=(810+h-1,1080+w-1)
        c=np.fft.irfft2(np.fft.rfft2(a,s=shape)*np.fft.rfft2(t[::-1,::-1],s=shape),s=shape)[h-1:810,w-1:1080]
        def sums(v):
            s=np.pad(v,((1,0),(1,0))).cumsum(0).cumsum(1)
            return s[h:,w:]-s[:-h,w:]-s[h:,:-w]+s[:-h,:-w]
        v=np.maximum(sums(a*a)-sums(a)**2/(h*w),0)
        scores=c/np.maximum(np.sqrt(v*np.sum(t*t)),1e-8)
        mask=np.zeros(scores.shape,bool)
        for x0,y0,x1,y1 in regions:
            mask[y0//4:max(y0//4,y1//4-h),x0//4:max(x0//4,x1//4-w)]=True
        scores[~mask]=-1
        for _ in range(18):
            y,x=np.unravel_index(scores.argmax(),scores.shape)
            candidates.append(dict(score=round(float(scores[y,x]),4),scale=scale,box=[int(x*4),int(y*4),int((x+w)*4),int((y+h)*4)]))
            scores[max(0,y-h):y+h,max(0,x-w):x+w]=-1
    selected=[]
    for p in sorted(candidates,key=lambda p:-p['score']):
        if any(abs(p['box'][0]-q['box'][0])<120 and abs(p['box'][1]-q['box'][1])<60 for q in selected): continue
        selected.append(p)
        if len(selected)==18: break
    result[name]={'source':filename,'regions':regions,'candidates':selected}
    sheet=Image.new('RGB',(960,660),'white'); draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(selected):
        x,y=(i%3)*320,(i//3)*110
        sheet.paste(source.crop(p['box']).resize((310,80)),(x,y+25))
        draw.text((x+4,y+5),f"{name} {i+1}: {p['score']} scale {p['scale']}",fill='black')
    sheet.save(ROOT/f'img/u02_search_{name}.jpg')
(ROOT/'u02_r1101_candidates.json').write_text(json.dumps(result,indent=2)+'\n')
print('Saved 18 candidates per source; all require manual verification.')
