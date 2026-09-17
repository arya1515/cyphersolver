import sys, collections; sys.stdout.reconfigure(encoding='utf-8')
key={int(l.split('\t')[0]):l.split('\t')[1].strip() for l in open('key_partial.txt',encoding='utf-8') if l.strip()}
def parse(p): return [int(x) for l in open(p,encoding='utf-8') if not l.startswith('#') for x in l.split()]
T={'H':parse('herleville.txt'),'F':parse('ciphertext.txt')}
cnt=collections.Counter(T['H']+T['F'])
unknown=sorted((g for g in cnt if g not in key), key=lambda g:-cnt[g])
def r(g): return key.get(g,'[%d]'%g)
for g in unknown[:int(sys.argv[1]) if len(sys.argv)>1 else 40]:
    print('== %d (x%d)'%(g,cnt[g]))
    for n,t in T.items():
        for i,x in enumerate(t):
            if x==g: print('   %s%3d: '%(n,i+1)+' '.join(r(y) for y in t[max(0,i-7):i])+'  <'+str(g)+'>  '+' '.join(r(y) for y in t[i+1:i+8]))
