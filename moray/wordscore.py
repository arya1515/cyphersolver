import math,collections,re,pickle,os
from lm import clean
FILES=['corpus/diurnalofremarka00thom.txt','corpus/registerprivyco01coungoog.txt','corpus/csp_scots.txt','corpus/historiecronicle01lind.txt','corpus/historiecronicle03lind.txt']
def build():
    c=collections.Counter()
    for f in FILES:
        c.update(clean(open(f,encoding='utf-8',errors='ignore').read()).split())
    tot=sum(c.values())
    # keep words seen >=2 times
    lp={w:math.log(n/tot) for w,n in c.items() if n>=2 and len(w)>1}
    pickle.dump(lp,open('words.pkl','wb')); return lp
LP=pickle.load(open('words.pkl','rb')) if os.path.exists('words.pkl') else build()
UNK=-20.0  # per unmatched letter
MAXL=14
def score(s):
    n=len(s); best=[0.0]+[-1e9]*n
    for i in range(1,n+1):
        b=best[i-1]+UNK
        for L in range(2,min(MAXL,i)+1):
            w=s[i-L:i]
            if w in LP:
                v=best[i-L]+LP[w]
                if v>b: b=v
        best[i]=b
    return best[n]
def segment(s):
    n=len(s); best=[0.0]+[-1e9]*n; back=[0]*(n+1)
    for i in range(1,n+1):
        b=best[i-1]+UNK; bk=i-1
        for L in range(2,min(MAXL,i)+1):
            w=s[i-L:i]
            if w in LP:
                v=best[i-L]+LP[w]
                if v>b: b=v; bk=i-L
        best[i]=b; back[i]=bk
    out=[];i=n
    while i>0: out.append(s[back[i]:i]); i=back[i]
    return ' '.join(reversed(out))
if __name__=='__main__':
    import sys
    print(len(LP))
    for t in sys.argv[1:]: print(round(score(t),1),segment(t))
