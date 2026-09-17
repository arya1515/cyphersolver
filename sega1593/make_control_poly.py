# Synthetic control: French text -> polyphonic classes -> pseudo-clusters (each class split 1-3 ways, 3% noise tokens)
import sys, re, json, random
sys.path.insert(0,'sega1593')
from poly_decode import INV
rnd=random.Random(int(sys.argv[3]))
text=open(sys.argv[1],encoding='utf-8').read()
text=re.sub(r'[^a-zA-Z ]',' ',text).lower(); words=text.split()[int(sys.argv[2]):int(sys.argv[2])+700]
PAIRS=['an','bo','cp','dq','er','fs','gt','hu','ix','ly','mz']; CODES=['que','qui','pour']
def cls(ch):
    ch=ch.replace('j','i').replace('v','u').replace('w','u').replace('k','c')
    return [p[0] for p in PAIRS].index(INV[ch]) if ch in INV else None
seq=[]
for w in words:
    if w in CODES: seq.append(11+CODES.index(w))
    else:
        for ch in w:
            c=cls(ch)
            if c is not None: seq.append(c)
    seq.append(14)
# pseudo-clusters
split={c:rnd.choice([1,1,2,2,3]) for c in range(15)}
cid={}; nxt=0; truth={}
for c in range(15):
    for s in range(split[c]): cid[(c,s)]=nxt; truth[nxt]=(PAIRS+CODES+['SEP'])[c]; nxt+=1
toks=[cid[(c,rnd.randrange(split[c]))] for c in seq]
junk=nxt
IMP=float(__import__('os').environ.get('IMPURITY','0'))
toks=[t if rnd.random()>0.03 else junk for t in toks]
toks=[t if rnd.random()>IMP or t==junk else rnd.randrange(nxt) for t in toks]
OUT=__import__('os').environ.get('OUT','control_poly')
DEL=float(__import__('os').environ.get('DEL','0')); INS=float(__import__('os').environ.get('INS','0'))
t2=[]
for t in toks:
    if rnd.random()<DEL: continue
    t2.append(t)
    if rnd.random()<INS: t2.append(rnd.randrange(nxt))
toks=t2
lines={}; per=60
for i in range(0,len(toks),per): lines[str(i//per+1)]=toks[i:i+per]
json.dump(lines,open(f'sega1593/{OUT}_clusters.json','w'))
json.dump({'truth':truth,'junk':junk,'seps':[cid[(14,s)] for s in range(split[14])]},open(f'sega1593/{OUT}_truth.json','w'))
print(len(toks),'tokens', nxt,'clusters', 'seps',[cid[(14,s)] for s in range(split[14])],'junk',junk)
print(truth)
