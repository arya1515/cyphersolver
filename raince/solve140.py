"""Same solver on the 140-cluster segmentation. Each 140-cluster inherits its allowed letter
set from the 70-clusters its tokens fall in, so the shape evidence carries over while the finer
clusters separate glyphs the 70-way run had merged (R/K, eps/Z, T/o-)."""
import json, pickle, random, collections
D=pickle.load(open('frns6.pkl','rb')); N=D['n']; P=D['p']; BACK=D['back']; PEN=-2.9
def score(s):
    t=0.0
    for i in range(len(s)-N+1):
        d=P.get(s[i:i+N-1]); t+=(d.get(s[i+N-1],BACK) if d else BACK)
    return t
a=json.load(open('raince_tokens.json')); b=json.load(open('raince140_tokens.json'))
ALLOW70 = {
 1:'a',2:'a',3:'b',4:'adl',5:'adl',6:'q',7:'c',8:'c',9:'ca',10:'su',11:'s',12:'su',13:'sui',
 14:'t',15:'t',16:'t',17:'u_',18:'tl',19:'tl',20:'aoy_',21:'u',22:'u',23:'u',24:'hu',25:'pme_',
 26:'e',27:'e',28:'n',29:'e',30:'eng_',31:'e_',32:'_',33:'mi_',34:'tl',35:'tl',36:'d',37:'i_',
 38:'er',39:'ne',40:'e_',41:'d',42:'n',43:'pml_',44:'y',45:'m',46:'tor',47:'f',48:'i_',49:'mi',
 50:'r',51:'r',52:'zr',53:'e',54:'l',55:'e',56:'e',57:'i',58:'p',59:'p',60:'s',61:'s',62:'s',
 63:'o',64:'o',65:'oa',66:'s',67:'_',68:'dl_',69:'i',70:'i'}
pair=collections.defaultdict(collections.Counter)
for t70,t140 in zip(a['tokens'], b['tokens']):
    pair[t140['cl']][t70['cl']] += 1
CH={}
for c140,cnt in pair.items():
    s=set()
    for c70,k in cnt.items():
        if k >= max(1, 0.12*sum(cnt.values())): s |= set(ALLOW70[c70])
    s.add('_')
    CH[c140]=sorted(s)
streams={}
for page in b['regions']:
    ts=[t for t in b['tokens'] if t['page']==page]
    n=len(b['regions'][page]['lines'])
    streams[page]=[t['cl'] for k in range(n) for t in sorted([x for x in ts if x['line']==k],key=lambda x:x['x0'])]
def dec(m,st): return ''.join('' if m[c]=='_' else m[c] for c in st)
def total(m):
    tot=0.0; nd=0
    for st in streams.values():
        tot+=score(dec(m,st)); nd+=sum(1 for c in st if m[c]=='_')
    return tot+nd*PEN
FREE=[c for c in CH if len(CH[c])>1]
print('clusters',len(CH),'free',len(FREE))
CTRL=[t['cl'] for t in sorted([x for x in b['tokens'] if x['page']=='f29r' and x['line']==19],key=lambda x:x['x0'])]
best=None;bv=-1e18
for r in range(5):
    rng=random.Random(r)
    m={c:(CH[c][0] if r==0 else rng.choice(CH[c])) for c in CH}
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
    print(f'r{r} {round(cur,1)} ctrl={dec(m,CTRL)}')
    if cur>bv: bv,best=cur,dict(m)
json.dump({str(k):v for k,v in best.items()},open('map140.json','w'))
print('BEST',round(bv,1)); print('ctrl ',dec(best,CTRL))
print('truth squiestoitenlacourtdesavoyeestpartypourveniricy')
