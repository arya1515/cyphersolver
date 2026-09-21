import re,collections
def groups(f):
    out=[]
    for line in open(f,encoding='utf-8'):
        if line.startswith('#'): continue
        line=re.sub(r'<[^>]*>','',line)
        line=re.sub(r'\^.|_','',line)
        for tok in re.split(r'[.,:;]',line):
            d=tok.replace(' ','')
            if re.fullmatch(r'\d{1,4}',d): out.append(int(d))
    return out
G={r:groups(__import__('os').path.dirname(__file__)+f'/decode/DOC_R{r}_D{d}_{d}.txt') for r,d in ((1469,1863),(1470,1864))}
if __name__=='__main__':
    for r,g in G.items():
        c=collections.Counter(g); print(r,len(g),len(c),max(g)); print(c.most_common(30))
    a=G[1469]+G[1470]; c=collections.Counter(a)
    print('all',len(a),len(c))
    # top groups sorted by value
    print(sorted(k for k,v in c.most_common(40)))
