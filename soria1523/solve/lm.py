import re, math, collections, unicodedata, pickle, os
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()); t=''.join(ch for ch in t if not unicodedata.combining(ch))
    t=t.replace('ç','z')
    t=re.sub(r'[^a-z]+',' ',t); return re.sub(' +',' ',t)
def build(path, n=4):
    t=' '+norm(open(path,encoding='utf-8',errors='ignore').read())+' '
    c=collections.Counter(t[i:i+n] for i in range(len(t)-n+1))
    tot=sum(c.values()); fl=math.log(0.01/tot)
    return {k:math.log(v/tot) for k,v in c.items()}, fl
P='solve/lm4.pkl'
def load():
    if os.path.exists(P): return pickle.load(open(P,'rb'))
    m=build('../adrian1521/danvila/mhe37.txt'); pickle.dump(m,open(P,'wb')); return m
