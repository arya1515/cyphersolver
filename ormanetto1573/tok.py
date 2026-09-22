import re,collections,sys
def load(path='decode/DOC_R116_D2580_2580.txt'):
    pages=[];cur=None
    for line in open(path,encoding='utf-8'):
        if line.startswith('#IMAGE'):
            cur=[];pages.append(cur);continue
        if line.startswith('#') or cur is None: continue
        line=re.sub(r'<[^>]*>',' ',line).replace('—',' ').replace('/',' ')
        for t in re.findall(r'[0-9?]\^?\.?(?:__)?',line):
            cur.append((t[0],'^' in t,'__' in t))
    return pages
if __name__=='__main__':
    P=load()
    for p in P:
        print(len(p))
    allt=[x for p in P for x in p]
    c=collections.Counter(x[0] for x in allt);print(sorted(c.items()))
    pre=collections.Counter(allt[i-1][0] for i in range(1,len(allt)) if allt[i][0]=='1');print('before1',pre)
    post=collections.Counter(allt[i+1][0] for i in range(len(allt)-1) if allt[i][0]=='1');print('after1',post)
    d=collections.Counter(x[0] for x in allt if x[1]);print('dotted',sorted(d.items()))
