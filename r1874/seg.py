import collections,math
from tok import toks
c=collections.Counter(t for _,t in toks)
units={t:n for t,n in c.items() if 3<=len(t)<=4 and n>=2}
def split(t):
    # DP: segment into known units (3-4 digits), maximise sum log count; unknown pieces penalised
    n=len(t);best=[(-1e9,None)]*(n+1);best[0]=(0,None)
    for i in range(1,n+1):
        for L in (2,3,4,5):
            j=i-L
            if j<0 or best[j][0]<-1e8: continue
            p=t[j:i]; s=math.log(units[p]) if p in units else -8
            if best[j][0]+s>best[i][0]: best[i]=(best[j][0]+s,j)
    out=[];i=n
    while i>0: j=best[i][1]; out.append(t[j:i]); i=j
    return out[::-1]
seq=[]
for pg,t in toks:
    if not t.isdigit() or len(t)<=4: seq.append((pg,t)); continue
    for u in split(t): seq.append((pg,u))
if __name__=='__main__':
    cc=collections.Counter(u for _,u in seq)
    print(len(seq),len(cc)); print(cc.most_common(60)); print([u for u,n in cc.items() if n==1][:80])
