import wordtable as W, sys, collections
import os
src=open('r2237_assign.txt',encoding='utf8').read()+open('r2237_inferred.txt',encoding='utf8').read()
P=os.path.join(os.environ.get('TMPD','.'),'_all.txt');open(P,'w',encoding='utf8').write(src)
letters,length,_=W.build(P)
toks=[]
for ln in open('r2239_groups.txt',encoding='utf8'):
    if ln.startswith('#') or not ln.strip(): continue
    toks+=ln.split()
dec=[W.decode_group(t,letters,length) for t in toks]
occ=collections.defaultdict(list)
for i,t in enumerate(toks):
    r=W.parse(t)
    if r: occ[r[0]].append(i)
want=[int(a) for a in sys.argv[1:]] or sorted(n for n in occ if n not in length)
for n in want:
    print(f'== {n} ({len(occ[n])}x) known:', W.show(n,letters,length))
    for i in occ[n]:
        print('   ', ' '.join(dec[max(0,i-4):i]), f'[{toks[i]}]', ' '.join(dec[i+1:i+5]))
