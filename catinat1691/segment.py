# French word segmenter for the joined decode stream (17th-c. spelling tolerated via corpus lexicon).
import re, os, math, collections, unicodedata, pickle
HERE=os.path.dirname(os.path.abspath(__file__)); FEU=os.path.join(HERE,'..','feuquieres')
def norm(w):
    w=unicodedata.normalize('NFD',w.lower()); w=''.join(c for c in w if unicodedata.category(c)!='Mn')
    return w.replace('j','i').replace('v','u')
def build():
    cnt=collections.Counter()
    for f in ['catinat1819_bsb10720286.txt','catinat1819_bsb10720287.txt','catinat1819_bsb10720288.txt','rousset4.txt','feuq5.txt','masque_de_fer_1893.txt']:
        t=open(os.path.join(FEU,f),encoding='utf-8',errors='replace').read()
        for w in re.findall(r"[A-Za-zÀ-ÿ]+",t):
            if len(w)>1 or w.lower() in 'ay': cnt[norm(w)]+=1
    # drop hapax OCR junk longer than 3
    lex={w:c for w,c in cnt.items() if c>=2 or len(w)<=3}
    for w in ['a','y','o']: lex.setdefault(w,50)
    return lex
P=os.path.join(HERE,'lex.pkl')
if os.path.exists(P): LEX=pickle.load(open(P,'rb'))
else:
    LEX=build(); pickle.dump(LEX,open(P,'wb'))
TOT=sum(LEX.values()); MAXW=18
def cost(w):
    c=LEX.get(w)
    if c: return 3.0-math.log(c/TOT)
    return 14+3*len(w)   # unknown
def seg(s):
    """s: lowercase string without spaces (i/j->i, u/v->u already). returns list of words"""
    n=len(s); best=[0.0]+[float('inf')]*n; bp=[0]*(n+1)
    for i in range(1,n+1):
        for j in range(max(0,i-MAXW),i):
            c=best[j]+cost(s[j:i])
            if c<best[i]: best[i]=c; bp[i]=j
    out=[]; i=n
    while i>0: out.append(s[bp[i]:i]); i=bp[i]
    return out[::-1]
if __name__=='__main__':
    print(len(LEX)); print(' '.join(seg('lesquelleleroyaestesurprisdeuoirqueuousnayezpointenuoieparuncourrierexpreslesmauuaisescommelesbonnesnouuelles')))
