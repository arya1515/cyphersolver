import re,os,io
src=open('decode/keep/lasry_decipherment_S364.txt',encoding='utf-8',errors='replace').read().splitlines()
os.makedirs('lasry',exist_ok=True)
blocks={}; cur=None
for ln in src:
    m=re.match(r'#CATALOG NAME:\s*Segr\. Stato Spagna 364([CD])/(\d+)',ln)
    if m:
        cur='364%s-%s'%(m.group(1),m.group(2)); blocks.setdefault(cur,[])
    if cur: blocks[cur].append(ln)
for k,v in blocks.items():
    if k.startswith('364D'):
        open('lasry/%s.txt'%k,'w',encoding='utf-8').write('\n'.join(v))
print(len([k for k in blocks if k.startswith('364D')]),'364D blocks')
print(sum(len(v) for k,v in blocks.items() if k.startswith('364D')),'lines')
