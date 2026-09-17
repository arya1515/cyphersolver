"""Cluster->letter map: each cluster is restricted to the letters its glyph shape allows
(read off img/z70_sheet_*.png against the measured key), then hill-climbed on a space-free
period-French 6-gram LM with restarts."""
import json, pickle, random
D=pickle.load(open('frns6.pkl','rb')); N=D['n']; P=D['p']; BACK=D['back']
PEN=-2.9
def score(s):
    t=0.0
    for i in range(len(s)-N+1):
        d=P.get(s[i:i+N-1]); t+=(d.get(s[i+N-1],BACK) if d else BACK)
    return t
d=json.load(open('raince_tokens.json'))
streams={}
for page in d['regions']:
    ts=[t for t in d['tokens'] if t['page']==page]
    n=len(d['regions'][page]['lines'])
    streams[page]=[t['cl'] for k in range(n) for t in sorted([x for x in ts if x['line']==k],key=lambda x:x['x0'])]

ALLOW = {
 1:'a', 2:'a', 3:'b', 4:'adl', 5:'adl', 6:'q', 7:'c', 8:'c', 9:'ca',
 10:'su', 11:'s', 12:'su', 13:'sui', 14:'t', 15:'t', 16:'t', 17:'u', 18:'tl',
 19:'tl', 20:'aoy', 21:'u', 22:'u', 23:'u', 24:'hu', 25:'pme', 26:'e', 27:'e',
 28:'n', 29:'e', 30:'eng', 31:'e', 32:'', 33:'mi', 34:'tl', 35:'tl', 36:'d',
 37:'i', 38:'er', 39:'ne', 40:'e', 41:'d', 42:'n', 43:'pm', 44:'y', 45:'m',
 46:'tor', 47:'f', 48:'i', 49:'mi', 50:'r', 51:'r', 52:'zr', 53:'e', 54:'l',
 55:'e', 56:'e', 57:'i', 58:'p', 59:'p', 60:'s', 61:'s', 62:'s', 63:'o',
 64:'o', 65:'oa', 66:'s', 67:'', 68:'dl', 69:'i', 70:'i',
}
# every cluster may also be read as a null (fragment / true null)
NULLABLE = {4,5,9,10,12,13,18,19,20,24,25,30,31,32,33,35,37,38,39,40,43,46,48,49,52,65,66,67,68}
CH = {c: (list(v) + ([''] if (c in NULLABLE or v=='') else [])) or [''] for c,v in ALLOW.items()}
FREE=[c for c in CH if len(CH[c])>1]
def total(m):
    tot=0.0
    for st in streams.values(): tot+=score(''.join(m.get(c,'') for c in st))
    nd=sum(1 for st in streams.values() for c in st if m.get(c,'')=='')
    return tot+nd*PEN
CTRL=[60,32,6,23,70,56,62,14,63,57,46,53,25,43,5,8,63,10,50,15,36,56,62,1,17,63,44,38,67,11,33,53,60,16,58,1,51,14,44,59,64,21,50,17,56,42,70,51,49,8,44]
TRUTH='s_quiestoit en la court de savoye _ est party pour venir icy'
best=None;bv=-1e18
for r in range(8):
    rng=random.Random(r)
    m={c: (CH[c][0] if r==0 else rng.choice(CH[c])) for c in CH}
    cur=total(m)
    for it in range(25):
        imp=False; order=FREE[:]; rng.shuffle(order)
        for c in order:
            old=m[c]; bl,bs=old,cur
            for L in CH[c]:
                if L==old: continue
                m[c]=L; s=total(m)
                if s>bs: bs,bl=s,L
            m[c]=bl
            if bl!=old: cur=bs; imp=True
        if not imp: break
    out=''.join(m.get(c,'') for c in CTRL)
    print(f'r{r}: {round(cur,1)} {out}')
    if cur>bv: bv,best=cur,dict(m)
json.dump({str(k):v for k,v in best.items()},open('map_lm.json','w'))
print('BEST',round(bv,1)); print('ctrl ',''.join(best.get(c,'') for c in CTRL)); print('truth',TRUTH)
print({k:best[k] for k in sorted(best)})
