import sys; sys.stdout.reconfigure(encoding='utf-8')
key={}
for l in open(sys.argv[1] if len(sys.argv)>1 else 'key_partial.txt',encoding='utf-8'):
    if l.strip() and not l.startswith('#'):
        g,u=l.rstrip('\n').split('\t'); key[int(g)]=u
def parse(p):
    paras=[[]]
    for l in open(p,encoding='utf-8'):
        if l.startswith('#'): continue
        if not l.strip():
            if paras[-1]: paras.append([])
            continue
        paras[-1]+=[int(x) for x in l.split()]
    return [p for p in paras if p]
for name,f in (('H','herleville.txt'),('F','ciphertext.txt')):
    for pi,p in enumerate(parse(f)):
        print('== %s P%d'%(name,pi+1))
        for i in range(0,len(p),12):
            chunk=p[i:i+12]
            print('%4d '%(i+1)+' '.join('%6d'%g for g in chunk))
            print('     '+' '.join('%6s'%(key.get(g,'.') if key.get(g,'.')!='' else '_') for g in chunk))
