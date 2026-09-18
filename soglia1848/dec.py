import json,sys,re
key=json.load(open('key.json'))
s=open('ct2.txt').read().strip()
out=[]
for r in s.split('5'):
    i=0;w=[]
    while i<len(r):
        if r[i]=='8' and i+4<=len(r):
            c=r[i:i+4]; w.append(key.get(c,'['+c+']')); i+=4
        elif i+2<=len(r):
            c=r[i:i+2]; w.append(key.get(c,'<'+c+'>')); i+=2
        else:
            w.append('{'+r[i]+'}'); i+=1
    out.append(''.join(w))
txt=' '.join(x for x in out)
print(re.sub(' +',' ',txt))
if len(sys.argv)>1:
    for r in s.split('5'):
        pass
