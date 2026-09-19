# vote a key out of align/*.tsv: weight H=3 M=1 ?=0
import glob,collections,json,unicodedata,re
def n(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r"[^a-z.]","",s)
V=collections.defaultdict(collections.Counter);src=collections.defaultdict(set)
for f in glob.glob('align/*.tsv'):
    for line in open(f,encoding='utf8'):
        p=line.rstrip('\n').split('\t')
        if len(p)<4 or not p[1].strip().isdigit(): continue
        g=int(p[1]);v=n(p[2]);w={'H':3,'M':1}.get(p[3].strip()[:1],0)
        if v and w: V[g][v]+=w; src[g].add(f[6:11])
for f in glob.glob('read/*_new.tsv'):
    for line in open(f,encoding='utf8'):
        p=line.rstrip(chr(10)).split(chr(9))
        if len(p)<3 or not p[0].strip().isdigit(): continue
        g=int(p[0]);v=n(p[1]);w={'H':2,'M':1}.get(p[2].strip()[:1],0)
        if v and w: V[g][v]+=w
key={};amb={}
for g,c in V.items():
    (v,s),*rest=c.most_common()
    tot=sum(c.values())
    if s/tot>=0.6: key[str(g)]=v
    else: amb[str(g)]=c.most_common(4)
key.update(json.load(open('overrides.json')))
json.dump(key,open('key_M.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
json.dump(amb,open('amb_M.json','w',encoding='utf8'),ensure_ascii=False)
print('groups',len(key),'ambiguous',len(amb))
