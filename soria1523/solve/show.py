import sys,re; sys.path.insert(0,'solve'); import hc
K=dict(x.split('=') for x in sys.argv[2].split(','))
for l in open(sys.argv[1],encoding='utf-8'):
    m=re.match(r'\s*(L\d+):(.*)',l)
    if not m: continue
    out=[]
    for w in m.group(2).split():
        if w in hc.CODES: out.append('['+w+']'); continue
        v=w.replace('cT','D'); out.append(''.join(K.get(c,c.upper() if c.islower() else '_'+c) for c in v if c!='?'))
    print(m.group(1),' '.join(out))
