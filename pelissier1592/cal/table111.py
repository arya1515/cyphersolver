import re, collections, sys
L=open('align_111.txt',encoding='utf-8').read().splitlines()
R={};P={}
for l in L:
    m=re.match(r'^([RP])(\d+):\s*(.*)$',l)
    if not m: continue
    toks=[t for t in m.group(3).split() if t!='|']
    (R if m.group(1)=='R' else P)[int(m.group(2))]=toks
cnt=collections.defaultdict(collections.Counter); refs=collections.defaultdict(list)
bad=[]
for n in sorted(R):
    r,p=R[n],P.get(n,[])
    if len(r)!=len(p): bad.append((n,len(r),len(p)))
    for i,(a,b) in enumerate(zip(r,p)):
        cnt[a][b]+=1; refs[(a,b)].append(f'R{n}.{i+1}')
if bad: print('LENGTH MISMATCH',bad,file=sys.stderr)
tot=sum(len(r) for r in R.values())
print('total tokens',tot, file=sys.stderr)
out=[]
for a in sorted(cnt,key=lambda k:-sum(cnt[k].values())):
    out.append(f'{a:6s} {sum(cnt[a].values()):4d}  '+'  '.join(f'{b}:{c}' for b,c in cnt[a].most_common()))
print('\n'.join(out))
import json; json.dump({f'{a}|{b}':v for (a,b),v in refs.items()},open('refs111.json','w'))
