import wordtable as W, os
src=open('r2237_assign.txt',encoding='utf8').read()+open('r2237_inferred.txt',encoding='utf8').read()
P='_all.tmp';open(P,'w',encoding='utf8').write(src)
L,Ln,c=W.build(P); os.remove(P)
if c: print('CONFLICTS',c)
for ln in open('r2239_groups.txt',encoding='utf8'):
    if ln.startswith('#') or not ln.strip(): continue
    out=[]
    for g in ln.split():
        d=W.decode_group(g,L,Ln)
        out.append(d if (d and '.' not in d and '~' not in d) or W.parse(g) is None else f'[{g}:{d}]')
    print(' '.join(out))
