"""Per-token beam decode. Each token emits one letter from the set its glyph shape allows
(or nothing, at a penalty), scored by the space-free period-French 6-gram LM. Unlike a fixed
cluster->letter map this lets a mixed cluster (R/K, epsilon/Z, T/o-) decode differently in
different words, which is where most of the map's residual errors are."""
import json, pickle, collections, sys
D=pickle.load(open('frns6.pkl','rb')); N=D['n']; P=D['p']; BACK=D['back']
DELPEN=float(sys.argv[1]) if len(sys.argv)>1 else -6.0
BEAM=int(sys.argv[2]) if len(sys.argv)>2 else 900
DEVPEN=float(sys.argv[3]) if len(sys.argv)>3 else -3.0

a=json.load(open('raince_tokens.json')); b=json.load(open('raince140_tokens.json'))
ALLOW70 = {
 1:'a',2:'a',3:'b',4:'adl',5:'adl',6:'q',7:'c',8:'c',9:'ca',10:'su',11:'s',12:'su',13:'sui',
 14:'t',15:'t',16:'t',17:'u',18:'tl',19:'tl',20:'aoy',21:'u',22:'u',23:'u',24:'hu',25:'pme',
 26:'e',27:'e',28:'n',29:'e',30:'eng',31:'e',32:'',33:'mi',34:'tl',35:'tl',36:'d',37:'i',
 38:'er',39:'ne',40:'e',41:'d',42:'n',43:'pml',44:'y',45:'m',46:'tor',47:'f',48:'i',49:'mi',
 50:'r',51:'r',52:'zr',53:'e',54:'l',55:'e',56:'e',57:'i',58:'p',59:'p',60:'s',61:'s',62:'s',
 63:'o',64:'o',65:'oa',66:'s',67:'',68:'dl',69:'i',70:'i'}
pair=collections.defaultdict(collections.Counter)
for t70,t140 in zip(a['tokens'], b['tokens']): pair[t140['cl']][t70['cl']]+=1
CH={}
for c,cnt in pair.items():
    s=set(); tot=sum(cnt.values())
    for c70,k in cnt.items():
        if k>=max(1,0.12*tot): s|=set(ALLOW70[c70])
    CH[c]=sorted(s)          # '' (delete) always allowed, handled separately
MAP={int(k):v for k,v in json.load(open('map140.json')).items()}   # the fixed-map backbone

def lp(ctx, ch):
    d=P.get(ctx); return d.get(ch,BACK) if d else BACK

def decode(stream):
    # state: last N-1 chars ; value: (score, backpointer list index)
    beams={('', )[0:0] and '' or ' '*(N-1): (0.0, None)}
    beams={' '*(N-1): (0.0, ())}
    for i, c in enumerate(stream):
        nb={}
        base = '' if MAP[c]=='_' else MAP[c]
        opts=[(ch, 0.0 if ch==base else DEVPEN) for ch in CH[c]] + [('', 0.0 if base=='' else DELPEN)]
        for ctx,(sc,path) in beams.items():
            for ch,extra in opts:
                if ch=='':
                    k=ctx; s=sc+extra; p=path+('',)
                else:
                    s=sc+lp(ctx,ch)+extra; k=(ctx+ch)[-(N-1):]; p=path+(ch,)
                if k not in nb or nb[k][0]<s: nb[k]=(s,p)
        beams=dict(sorted(nb.items(), key=lambda kv:-kv[1][0])[:BEAM])
    ctx,(sc,path)=max(beams.items(), key=lambda kv: kv[1][0])
    return sc, path

out=[]; tot=0.0
for page in b['regions']:
    ts=[t for t in b['tokens'] if t['page']==page]
    n=len(b['regions'][page]['lines'])
    rows=[sorted([x for x in ts if x['line']==k],key=lambda x:x['x0']) for k in range(n)]
    stream=[t['cl'] for r in rows for t in r]
    sc,path=decode(stream)
    tot+=sc
    out.append('## '+page)
    j=0
    for k,r in enumerate(rows):
        out.append(f'{k+1:02d} '+''.join(path[j+i] for i in range(len(r)))); j+=len(r)
    print(page, 'score', round(sc,1), 'chars', sum(1 for x in path if x))
open('draft6.txt','w').write('\n'.join(out)+'\n')
print('total', round(tot,1))
