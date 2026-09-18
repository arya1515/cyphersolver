import random,collections,sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
txt=open('corpus/pg75829.txt',encoding='utf8',errors='ignore').read()
import unicodedata,re
t=unicodedata.normalize('NFD',txt.lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
t=re.sub(r"[^a-z]+",' ',t.replace("'",' '))
st=random.randint(20000,300000); words=t[st:].split()[1:]
w=[];n=0
while n<404:
    x=words.pop(0); w.append(x); n+=len(x)
plain=' '.join(w)
# homophones: 68 symbols distributed ~ proportional to sqrt freq
f=collections.Counter(plain.replace(' ',''))
letters=sorted(f,key=lambda c:-f[c])
alloc={c:1 for c in letters}
while sum(alloc.values())<68:
    c=max(letters,key=lambda c:f[c]/alloc[c]); alloc[c]+=1
codes=[f'{a}{b}' for a in '012346789' for b in '01234679']; random.shuffle(codes)
key={};i=0
for c in letters:
    key[c]=codes[i:i+alloc[c]]; i+=alloc[c]
ct='5'.join(''.join(random.choice(key[c]) for c in wd) for wd in w)
open('synth_ct.txt','w').write(ct); open('synth_pt.txt','w').write(plain)
print(plain[:200]); print(len(plain.replace(' ','')),len(set(ct[i:i+2] for i in range(0,1))))
