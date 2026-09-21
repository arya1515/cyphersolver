import re,glob
for f in sorted(glob.glob('img/DOC*.txt')):
    rec=re.search(r'R(\d+)',f).group(1)
    img=None;part={}
    mode='c'
    for line in open(f,encoding='utf8',errors='replace'):
        line=line.rstrip('\n')
        m=re.match(r'#IMAGE NAME: (\d+)\.png\s*$',line)
        if m: img=m.group(1);mode='c';part.setdefault(img,([],[]));continue
        if 'left margin' in line: mode='m';continue
        if line.startswith('#') or img is None: continue
        if mode=='m':
            part[img][1].append(re.sub(r'<|>|(CLEAR|PLAIN)TEXT ES','',line).strip())
        else:
            c=re.sub(r'<[^>]*>',' | ',line)
            for seg in re.split(r'\s{2,}|\|',c):
                s=seg.replace(' ','').strip()
                if s and s not in '()=': part[img][0].append(s)
    for img,(c,m) in part.items():
        if c: open(f'tx/R{rec}.txt','a',encoding='utf8').write('C: '+' '.join(c)+'\n'+''.join('M: '+x+'\n' for x in m))
