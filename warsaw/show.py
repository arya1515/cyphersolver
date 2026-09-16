import sys,json
toks=open('ct.txt').read().split()
key=json.load(open(sys.argv[1]))
out=[]
for t in toks:
    if t.isdigit():
        out.append('['+t+']' if len(t)==3 else key.get(t,'?'))
    else: out.append({'a':' ','m':'_'}.get(t,'<'+t+'>'))
print(''.join(out))
