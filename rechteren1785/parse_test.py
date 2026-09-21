import re,csv,sys
t=open('decode/DOC_R1039_D3590_3590.txt',encoding='utf-8').read()
parts=re.split(r'#?IMAGE NAME: ',t)
body=[p for p in parts if p.startswith('5451') or p.startswith('5452')]
groups=[]
for p in body:
    for line in p.splitlines():
        if line.startswith('<') or line.startswith('#') or not re.search(r'\d',line) or 'COMMENTS' in line: continue
        if line.startswith('5451') or line.startswith('5452'): continue
        for g in re.split(r'[,—]',line):
            raw=g.strip()
            if not raw: continue
            base=re.sub(r'[^0-9]','',re.sub(r'\^(\.\.|\.|_)','',raw))
            marks=''.join(re.findall(r'\^(\.\.|\.|_)',raw))
            groups.append((raw,base,marks))
print(len(groups),'groups')
keys={}
for f in ['R2052','R2051']:
    k={}
    for r in csv.DictReader(open(f'../deswart1782/{f}_reconstructed_key.tsv',encoding='utf-8'),delimiter='\t'):
        b=re.sub(r'\D','',r['normalized_group']); k.setdefault(b,r['plaintext'])
    keys[f]=k
for f,k in keys.items():
    hit=sum(1 for _,b,_ in groups if b in k)
    print(f,hit, ' '.join(k.get(b,'['+b+']') for _,b,_ in groups[:80]))
from collections import Counter
c=Counter(m for *_,m in groups); print(c.most_common(8))
open('R1039_groups.tsv','w',encoding='utf-8').write('\n'.join('\t'.join(g) for g in groups))
