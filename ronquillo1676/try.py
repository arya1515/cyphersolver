import re,glob,json,sys
sys.stdout.reconfigure(encoding='utf-8')
K=json.load(open('../balbases1677/key.json',encoding='utf8'))
K.update({'d':'que','N':'','N_':'','30':'p','6+':'o','4':'t','161':'resolucion','167':'suecia','os':'para','a':''})
K.update({'Infinity'+v:'c'+v for v in 'aeiou'}); K['Infinity']='c'
for f in sorted(glob.glob('img/DOC*.txt'),key=lambda x:int(re.search(r'R(\d+)',x).group(1))):
    C=[];M=[]
    mode='c'
    for line in open(f,encoding='utf8',errors='replace'):
        if 'margin' in line.lower() and line.startswith('#'): mode='m';continue
        if line.startswith('#IMAGE'): mode='c'
        if line.startswith('#'): continue
        if mode=='m': M.append(re.sub(r'<|>|(CLEAR|PLAIN)TEXT \w+','',line).strip());continue
        c=re.sub(r'<[^>]*>',' | ',line)
        dbl=bool(re.search(r'\S \S  \S',c)) or bool(re.search(r'\d \d',c))
        for seg in (re.split(r'\s{2,}|\|',c) if dbl else re.split(r'[\s|]+',c)):
            s=seg.replace(' ','').strip().strip('()=').rstrip('?')
            if s: C.append(s)
    out=[K.get(t,'['+t+']') for t in C]; kn=sum(t in K for t in C)
    name=re.search(r'R\d+',f).group(0)
    print(f'== {name} {len(C)} groups, key reads {kn/max(len(C),1):.0%}')
    print('  ',''.join(out)[:160]); print('   margin:',len(M),'lines')
