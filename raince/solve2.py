"""Cluster->letter map for the Raince stream. Clusters whose glyph is unambiguous on the
cluster sheets are clamped to the key's value; the rest are hill-climbed against a
space-free period-French 6-gram LM, with restarts."""
import json, pickle, random
D = pickle.load(open('frns6.pkl','rb')); N=D['n']; P=D['p']; BACK=D['back']
CHOICES = list('abcdefghilmnopqrstuy') + ['', 'z']
PEN = -2.9

def score(s):
    t=0.0
    for i in range(len(s)-N+1):
        d=P.get(s[i:i+N-1]); t += (d.get(s[i+N-1],BACK) if d else BACK)
    return t

d=json.load(open('raince_tokens.json'))
streams={}
for page in d['regions']:
    ts=[t for t in d['tokens'] if t['page']==page]
    n=len(d['regions'][page]['lines'])
    streams[page]=[t['cl'] for k in range(n) for t in sorted([x for x in ts if x['line']==k], key=lambda x:x['x0'])]

# clamped from the cluster sheets read against the measured key
CLAMP = {1:'a',2:'a',3:'b',6:'q',7:'c',8:'c',14:'t',15:'t',16:'t',17:'u',21:'u',22:'u',23:'u',
         24:'h',26:'e',27:'e',28:'n',29:'e',32:'',36:'d',41:'d',42:'n',44:'y',45:'m',47:'f',
         49:'m',50:'r',51:'r',58:'p',59:'p',60:'s',61:'s',62:'s',63:'o',64:'o',69:'i',70:'i'}
FREE = [c for c in sorted({c for st in streams.values() for c in st}) if c not in CLAMP]
INIT = {4:'a',5:'a',9:'c',10:'u',11:'s',12:'s',13:'s',18:'l',19:'t',20:'a',25:'n',30:'e',
        31:'',33:'s',34:'t',35:'l',37:'',38:'e',39:'n',40:'',43:'l',46:'t',48:'',52:'r',
        53:'e',54:'l',55:'e',56:'e',57:'i',65:'o',66:'s',67:'',68:''}

def total(m):
    tot=0.0; nd=0
    for st in streams.values():
        s=''.join(m.get(c,'') for c in st); tot+=score(s)
    nd=sum(1 for st in streams.values() for c in st if m.get(c,'')=='')
    return tot+nd*PEN

CTRL=[60,32,6,23,70,56,62,14,63,57,46,53,25,43,5,8,63,10,50,15,36,56,62,1,17,63,44,38,67,11,33,53,60,16,58,1,51,14,44,59,64,21,50,17,56,42,70,51,49,8,44]
TRUTH='squiestoitenlacourtdesavoyeestpartypourveniricy'.replace('v','u').replace('y','i')

bestm=None; bestv=-1e18
for r in range(6):
    rng=random.Random(r)
    m=dict(CLAMP); m.update(INIT)
    if r: 
        for c in FREE:
            if rng.random()<0.45: m[c]=rng.choice(CHOICES)
    cur=total(m)
    for it in range(30):
        imp=False
        order=FREE[:]; rng.shuffle(order)
        for c in order:
            old=m[c]; bl,bs=old,cur
            for L in CHOICES:
                if L==old: continue
                m[c]=L; s=total(m)
                if s>bs: bs,bl=s,L
            m[c]=bl
            if bl!=old: cur=bs; imp=True
        if not imp: break
    out=''.join(m.get(c,'') for c in CTRL)
    print(f'restart {r}: {round(cur,1)}  ctrl={out}')
    if cur>bestv: bestv,bestm=cur,dict(m)
json.dump({str(k):v for k,v in bestm.items()}, open('map_lm.json','w'))
print('best', round(bestv,1))
print('ctrl ', ''.join(bestm.get(c,'') for c in CTRL))
print('truth', TRUTH)
print('map  ', {k:bestm[k] for k in sorted(bestm)})
