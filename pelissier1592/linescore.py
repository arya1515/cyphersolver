import re,glob,beam
rows=[]
for f in ['t46r','t46v','t47r','t47v','t48r','t48v','t49r','t49v','t50r']:
    for l in open(f+'.txt',encoding='utf-8'):
        m=re.match(r'(C\d+[a-z]?):\s*(.*)',l)
        if m:
            toks=m.group(2).split()
            if len(toks)<8: continue
            sc,_,txt=beam.decode(toks,B=120)
            n=sum(c.isalpha() for c in txt)
            rows.append((sc/max(n,1),f,m.group(1),len(toks),txt))
rows.sort()
good=sum(1 for r in rows if r[0]>-0.62)
print('rows',len(rows),'good(>-0.62)',good)
for r in rows: print(f'{r[0]:.2f} {r[1]} {r[2]} {r[3]} {r[4][:90]}')
