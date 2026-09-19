import re,glob,collections,json
def groups(f):
    out=[]
    for line in open(f,encoding='utf8',errors='replace'):
        if line.startswith('#') or line.startswith('<') or re.search(r'[A-Za-z]',line): continue
        s=line.replace(' ','')
        for tok in s.split('.'):
            t=re.sub(r'[^0-9?/]','',tok)
            if not t: continue
            d=re.sub(r'\?','',t.split('/')[0])
            if d: out.append((d,'?' in t or '/' in t))
    return out
if __name__=='__main__':
    C=collections.Counter(); tot=0
    for f in sorted(glob.glob('decode/DOC_*.txt')):
        g=groups(f); tot+=len(g); C.update(int(x) for x,_ in g)
        print(f[11:16],len(g),sum(u for _,u in g))
    print('total',tot,'distinct',len(C),'max',max(C))
    print(C.most_common(40))
