import re,unicodedata,math,collections,json
t=open('memoriasparalah00villgoog.txt',encoding='utf8').read()+open('memoriasparalah00goog.txt',encoding='utf8').read()
t=unicodedata.normalize('NFD',t.lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
t=t.replace('ñ','n')
t=re.sub(r'[^a-z]+',' ',t)
# 16c spelling normalisation for cipher alphabet: v->u? keep; k,w rare
words=t.split()
# drop junk: keep words with a vowel
words=[w for w in words if re.search('[aeiouy]',w)]
text=' '+' '.join(words)+' '
open('lm_text.txt','w').write(text)
N=5
cnt=collections.Counter(text[i:i+N] for i in range(len(text)-N))
print(len(text),len(cnt))
wc=collections.Counter(words); print(wc.most_common(40))
