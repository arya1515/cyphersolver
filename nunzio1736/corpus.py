import re,json
t=open('decode/keep/lasry_decipherment_S423.txt',encoding='utf-8',errors='replace').read().splitlines()
seq=[];item=None
for i,a in enumerate(t):
    m=re.match(r'#CATALOG NAME: .*423.(\d+)',a)
    if m: item=int(m.group(1)); continue
    if i+1<len(t) and a.strip() and re.match(r'^[\d ?X_|^,.*]+$',a.strip()) and not t[i+1].startswith('#'):
        b=t[i+1]
        ms=[m for m in re.finditer(r'\S+',a) if m.group()!='|']
        for k,m in enumerate(ms):
            end=ms[k+1].start() if k+1<len(ms) else len(b)
            p=b[m.start():end].strip().rstrip('|').strip()
            seq.append((item,m.group(),p))
json.dump(seq,open('seq.json','w'))
print(len(seq),'tokens; items',sorted(set(s[0] for s in seq)))
