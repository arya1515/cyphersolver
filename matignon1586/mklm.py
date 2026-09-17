import re, unicodedata, pickle, glob, collections, math
def norm(t):
    t=unicodedata.normalize('NFD',t)
    t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    t=t.lower()
    t=t.replace('v','u').replace('j','i').replace('w','u').replace('k','c')
    t=re.sub(r'[^a-z]+',' ',t)
    return re.sub(r'\s+',' ',t).strip()
txt=[]
for f in glob.glob('../bethune/xivrey/*.txt'):
    txt.append(norm(open(f,encoding='utf-8',errors='ignore').read()))
s=' '.join(txt)
print('chars',len(s))
words=collections.Counter(s.split())
print('words',len(words), sum(words.values()))
open('corpus_words.txt','w',encoding='utf-8').write('\n'.join(f'{w}\t{c}' for w,c in words.most_common()))
flat=s.replace(' ','')
print('flat',len(flat))
N=6
cnt=[collections.Counter() for _ in range(N+1)]
for n in range(1,N+1):
    c=cnt[n]
    for i in range(len(flat)-n+1):
        c[flat[i:i+n]]+=1
with open('lm.pkl','wb') as fh: pickle.dump({'cnt':cnt,'N':N,'flat_len':len(flat)},fh)
print('lm sizes',[len(c) for c in cnt])
