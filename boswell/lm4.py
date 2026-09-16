"""English 4-gram model over the 24-letter alphabet (j->i, v->u), built from 17th-19th c. English editions in the repo."""
import re, math, collections, os, pickle
FILES = ['src/simpson_djvu.txt',
         '../charlesi/src/bim_eighteenth-century_a-new-correct-and-much_albin-john_1795.txt',
         '../charlesi/src/cu31924028050940.txt', '../charlesi/src/historyofisleofw00warniala.txt',
         '../charlesi/src/narrativeofattem00hilluoft.txt']
def clean(s):
    s = s.lower().replace('j','i').replace('v','u')
    s = re.sub(r'[^a-z]+',' ',s)
    return ' '.join(w for w in s.split() if len(w)<20 and not re.search(r'(.)\1\1',w))
def build():
    if os.path.exists('lm4.pkl'): return pickle.load(open('lm4.pkl','rb'))
    txt=' '.join(clean(open(f,encoding='utf-8',errors='ignore').read()) for f in FILES)
    txt=txt.replace(' ','')
    c=collections.Counter(txt[i:i+4] for i in range(len(txt)-3))
    tot=sum(c.values()); floor=math.log10(0.01/tot)
    lp={k:math.log10(v/tot) for k,v in c.items()}
    pickle.dump((lp,floor,len(txt)),open('lm4.pkl','wb'))
    return lp,floor,len(txt)
LP,FLOOR,N=build()
def score(s):
    s=s.replace('j','i').replace('v','u')
    return sum(LP.get(s[i:i+4],FLOOR) for i in range(len(s)-3))
if __name__=='__main__':
    print('chars in model:',N, 'distinct 4-grams:',len(LP))
