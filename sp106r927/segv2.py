import numpy as np, sys, json
from PIL import Image
from scipy import ndimage as ndi
src,pre=sys.argv[1],sys.argv[2]
box=tuple(map(int,sys.argv[3].split(',')))
im=Image.open(src).convert('L').crop(box); a=np.array(im).astype(float)
bg=ndi.median_filter(a[::4,::4],15); bg=np.kron(bg,np.ones((4,4)))[:a.shape[0],:a.shape[1]]
ink=(a<bg-40)
lab,n=ndi.label(ink); objs=ndi.find_objects(lab); sizes=ndi.sum(ink,lab,range(1,n+1))
D=[];Gc=[]
for i,(s,sz) in enumerate(zip(objs,sizes)):
    h=s[0].stop-s[0].start; w=s[1].stop-s[1].start
    if h<24 and w<24 and 18<=sz<=160: D.append([(s[0].start+s[0].stop)/2,(s[1].start+s[1].stop)/2, 2 if sz>=80 and max(h,w)>=13 else 1])
g=json.load(open(pre+'_glyphs.json'))
gl=[x for C in g for x in C]
for x in gl: x['nd']=0
for dy,dx,k in D:
    best=None
    for x in gl:
        if x['x1']-6<=dx<=x['x1']+40:
            cy=x['y']-4 if True else 0
            dist=0 if x['y']-10<=dy<=x['y1']+4 else min(abs(dy-x['y']),abs(dy-x['y1']))
            if dist<16 and (best is None or dist<best[0]): best=(dist,x)
    if best: best[1]['nd']+=k
json.dump(g,open(pre+'_glyphs2.json','w'))
K=dict(zip('ABCDEFGHI',['akt','blu','cmw','dnx','eoy','fpz','gq','hr','is']))
import collections
print(collections.Counter(x['sh']+str(x['nd']) for x in gl).most_common())
for C in g[:4]: print(' '.join(x['sh']+str(x['nd']) for x in C))
