import re,collections
s=open('ct.txt').read()
runs=[r for r in re.split('5',s)]
out=[]
C=collections.Counter()
for r in runs:
    if len(r)%2==0:
        g=[r[i:i+2] for i in range(0,len(r),2)]; C.update(g); out.append(' '.join(g))
    else: out.append('['+r+']')
print(' | '.join(out))
print(len(C),sum(C.values()))
print(sorted(C.items(),key=lambda x:-x[1]))
print('first digit',collections.Counter(k[0] for k in C.elements()))
print('second digit',collections.Counter(k[1] for k in C.elements()))
