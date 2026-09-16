# Enumerate all pairings (letters dropped, wavy inline, code groups of width<=2) and score by pair IC.
import sys,collections,json
g=open('ct2.txt').read().split()
items=[x for x in g if not x.isalpha()]
n=len(items)
def plain(j): return 0<=j<n and items[j][0].isdigit() and len(items[j])==1
marks=[i for i,x in enumerate(items) if x[0].isdigit() and len(x)>1]
cands={m:[(s,e) for (s,e) in [(m,m),(m,m+1),(m-1,m)] if all(plain(j) for j in range(s,e+1) if j!=m)] for m in marks}
sols=[]
def rec(i,par,toks,cur):
    if i==n:
        if par==0: sols.append(list(toks))
        return
    x=items[i]
    if x=='|': toks.append('|'); rec(i+1,par,toks,cur); toks.pop(); return
    if len(x)>1:
        if par: return
        for (s,e) in cands[i]:
            if s<i: continue
            grp='#'+''.join(items[j][0] for j in range(s,e+1))+x[1]
            toks.append(grp); rec(e+1,0,toks,cur); toks.pop()
        return
    # plain digit
    if par==0:
        # start a backward group with next mark?
        if i+1<n and len(items[i+1])>1 and items[i+1][0].isdigit() and (i,i+1) in cands[i+1]:
            grp='#'+x+items[i+1][0]+items[i+1][1]; toks.append(grp); rec(i+2,0,toks,cur); toks.pop()
        cur.append(x); rec(i+1,1,toks,cur); cur.pop()
    else:
        toks.append(cur[-1]+x); rec(i+1,0,toks,cur); toks.pop()
rec(0,0,[],[])
print('solutions',len(sols))
def ic(c):
    N=sum(c.values()); return sum(v*(v-1) for v in c.values())/(N*(N-1))
rows=[]
for s in sols:
    letters=[t for t in s if t[0].isdigit()]
    c=collections.Counter(letters); rows.append((ic(c),len(c),len(letters),s))
rows.sort(key=lambda r:-r[0])
for r in rows[:10]: print(round(r[0],4),r[1],r[2],' '.join(r[3])[:150])
print('...'); 
for r in rows[-3:]: print(round(r[0],4),r[1],r[2])
json.dump([r[3] for r in rows],open('pairings.json','w'))
# where do the solutions differ?
cols=set()
for s in rows: cols.add(tuple(t for t in s[3] if t[0]=='#'))
print('distinct code-group sets',len(cols))
print('code groups (best):',[t for t in rows[0][3] if t[0]=='#'])
