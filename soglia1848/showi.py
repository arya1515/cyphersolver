import sys
import os
if os.environ.get("PARSE")=="pairs":
    import drive as D
else:
    import drive8 as D
tag=sys.argv[1]; cand=sys.argv[2]; top=int(sys.argv[3]) if len(sys.argv)>3 else 8
C=[l.strip() for l in open(cand) if l.strip()]
Rs=D.results(f'runs/{tag}_*.out')
# stability of each type across top runs
import collections
for i,t in enumerate(D.types):
    c=collections.Counter(C[m[i]] for sc,m in Rs[:top])
    print(t, c.most_common(3), end=' | ')
print()
sc,m=Rs[0]
U=D.U
words=[];cur=[]
for u in U:
    if u=='_':
        if cur: words.append(cur); cur=[]
    else: cur.append(u)
if cur: words.append(cur)
line=[]
for w in words:
    line.append(''.join(C[m[D.ti[u]]] for u in w)+'('+'.'.join(w)+')')
print(' '.join(line))
