import wordtable as W, os, sys
src=open('r2237_assign.txt',encoding='utf8').read()+open('r2237_inferred.txt',encoding='utf8').read()
open('_a','w',encoding='utf8').write(src); L,Ln,c=W.build('_a'); os.remove('_a')
if c: print('CONFLICTS',c)
n=0
for ln in open('r2239_groups.txt',encoding='utf8'):
    if ln.startswith('#') or not ln.strip(): continue
    n+=1
    out=[]
    for g in ln.split():
        d=W.decode_group(g,L,Ln)
        out.append(g if W.parse(g) is None else (d if d and '.' not in d and '~' not in d else f'{g}:{d}'))
    print(f'L{n}:',' | '.join(out))
