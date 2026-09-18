"""Build a French character n-gram model with stupid backoff from the Montaigne corpus.
Spaces are stripped: the cipher of fr. 3621 no. 97 has no word division."""
import re, json, collections, math, sys

AL='abcdefghilmnopqrstuxyz'
keep=set(AL)

def load(path):
    t=open(path,encoding='utf-8',errors='replace').read().lower()
    t=re.sub(r'[^a-z]',' ',t)
    # 16th-c orthography: fold v/w onto u, j onto i, k onto c
    t=t.translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
    # strip roman-numeral tokens: they wrecked the earlier model
    t=' '.join(w for w in t.split() if not re.fullmatch(r'[ivxlcdm]+',w))
    # collapse runs of 3+ identical letters
    t=re.sub(r'(.)\1{2,}', r'\1\1', t)
    return t.replace(' ','')

txt=load('src/corpus_fr.txt')
print('corpus chars', len(txt), file=sys.stderr)
cnt=[collections.Counter() for _ in range(5)]
for n in (1,2,3,4):
    c=cnt[n]
    for i in range(len(txt)-n+1):
        g=txt[i:i+n]
        c[g]+=1
tot=sum(cnt[1].values())
model={'al':AL,
       'uni':{k:v/tot for k,v in cnt[1].items()},
       'n1':dict(cnt[1]),'n2':dict(cnt[2]),'n3':dict(cnt[3]),'n4':dict(cnt[4])}
json.dump(model, open('src/fr_lm.json','w'))
print('sizes', {k:len(model[k]) for k in ('n1','n2','n3','n4')}, file=sys.stderr)
