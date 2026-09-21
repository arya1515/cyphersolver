import re,glob,sys,os
sys.stdout.reconfigure(encoding='utf-8')
exec(open('seg.py',encoding='utf8').read().split('import glob')[0])
os.makedirs('read',exist_ok=True)
tot=[0,0]
for r in [*range(966,985),1001]:
    f=glob.glob(f'img/DOC_R{r}_*.txt')[0]
    raw=open(f,encoding='utf8',errors='replace').read().lstrip('﻿')
    name=re.search(r'2559_(\S+)',raw).group(1)
    cl=[re.sub(r'<[^>]*>',' ',l) for l in raw.splitlines() if not l.startswith('#')]
    spaced=sum(bool(re.search(r'\S \S  \S',l)) for l in cl)<3
    C=[];M=[];mode='c'
    for line in raw.splitlines():
        if line.startswith('#') and 'margin' in line.lower(): mode='m';continue
        if line.startswith('#IMAGE'): mode='c'
        if line.startswith('#'): continue
        if mode=='m' and line.startswith('<'): M.append(re.sub(r'<|>|(CLEAR|PLAIN)TEXT \w+','',line).strip());continue
        c=re.sub(r'<[^>]*>',' | ',line)
        if spaced:
            for ch in c.split('|'):
                ch=re.sub(r'\s','',ch).replace('?','').replace('_','')
                if ch: C+=seg(ch)
        else:
            for sgm in re.split(r'\s{2,}|\|',c):
                s=sgm.replace(' ','').strip().strip('()=').rstrip('?')
                if s: C.append(s)
    kn=sum(t in K for t in C);tot[0]+=kn;tot[1]+=len(C)
    txt=''.join(K.get(t,'['+t+']') for t in C)
    open(f'read/R{r}.txt','w',encoding='utf8').write(f'# R{r} {name}: {len(C)} groups, key reads {kn/max(len(C),1):.1%}\n\n{txt}\n\n# margin (DECODE transcription)\n'+'\n'.join(m for m in M if m)+'\n')
    print(f'R{r} {name:40s} {len(C):5d} {kn/max(len(C),1):.0%} margin:{len([m for m in M if m])}')
print('total',tot[1],f'{tot[0]/tot[1]:.1%}')
