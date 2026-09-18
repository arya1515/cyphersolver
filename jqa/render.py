import sys
tab={}
for l in open('pairs_jqa.txt',encoding='utf8'):
    if l.startswith('#') or not l.strip(): continue
    n,r,s,g=l.rstrip('\n').split('\t')
    r=r+('' if g=='H' else '?')
    tab.setdefault(int(n),[])
    if r not in tab[int(n)]: tab[int(n)].append(r)
tot=hit=0
for line in open(sys.argv[1],encoding='utf8'):
    out=[]
    for t in line.split():
        if t.isdigit():
            tot+=1
            if int(t) in tab: hit+=1; out.append('/'.join(tab[int(t)]))
            else: out.append('['+t+']')
        else: out.append(t.upper() if t!='|' else '|')
    print(' '.join(out))
print(hit,'of',tot)
