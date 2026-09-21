import sys,collections
from corpus import C,OTHER
from apply import K,norm
seqs=[[norm(t) for t in ts] for r,ts in C.items() if r not in OTHER]
cnt=collections.Counter(t for s in seqs for t in s)
def show(t,w=4,n=12):
    k=0
    for s in seqs:
        for i,x in enumerate(s):
            if x==t:
                L=[K.get(y,'['+y+']') for y in s[max(0,i-w):i]]; R=[K.get(y,'['+y+']') for y in s[i+1:i+1+w]]
                print('   ',' '.join(L),' <<',t,'>> ',' '.join(R)); k+=1
                if k>=n: return
if __name__=='__main__':
    if sys.argv[1]=='top':
        for t,c in cnt.most_common(int(sys.argv[2])):
            if t not in K: print(t,c)
    else:
        for t in sys.argv[1:]: print('==',t,cnt[t]); show(t)
