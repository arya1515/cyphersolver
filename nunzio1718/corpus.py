import re,collections,json
SRC='decode/keep/lasry_decipherment_S364.txt'
L=open(SRC,encoding='utf-8',errors='replace').read().splitlines()
# key
known={}
for ln in open('decode/keep/lasry_key_S364.txt',encoding='utf-8',errors='replace'):
    m=re.match(r'^([\d|]+)\s*-\s*(.+)$',ln.strip())
    if m:
        for c in m.group(1).split('|'): known[c]=m.group(2).strip()
rows=[]   # (catalog, list of (cipher,plain))
cat=None; toks=[]
def cols(a):
    starts=[]; prev_end=-2
    for m in re.finditer(r'\S+',a):
        if m.start()>prev_end+1: starts.append(m.start())
        prev_end=m.end()-1
    starts.append(len(a)); return starts
seq=[]
for i in range(len(L)-1):
    m=re.match(r'#CATALOG NAME:\s*Segr\. Stato Spagna (364[CD]/\d+)',L[i])
    if m: cat=m.group(1)
    a,b=L[i],L[i+1]
    if not (a.rstrip().endswith('|') and b.rstrip().endswith('|')): continue
    if not re.match(r'^\s*\d',a): continue
    s=cols(a)
    for j in range(len(s)-1):
        ct=a[s[j]:s[j+1]].strip(); pt=b[s[j]:s[j+1]].strip() if s[j]<len(b) else ''
        if ct in ('|',''): continue
        seq.append((cat,ct,pt))
json.dump(seq,open('seq.json','w',encoding='utf-8'),ensure_ascii=False)
print('corpus tokens:',len(seq))
unk=collections.Counter()
for cat,ct,pt in seq:
    if re.fullmatch(r'4\d{3}',ct) and ct not in known: unk[ct]+=1
print('distinct 4xxx in corpus:',len({c for _,c,_ in seq if re.fullmatch(r'4\d{3}',c)}))
print('known 4xxx:',len([k for k in known if re.fullmatch(r'4\d{3}',k)]))
print('UNKNOWN 4xxx:',len(unk),'tokens',sum(unk.values()))
for g,n in unk.most_common(60): print('  %s %d'%(g,n))
