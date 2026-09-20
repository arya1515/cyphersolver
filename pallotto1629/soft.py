import math
from collections import Counter, defaultdict
from solve import load_doc, norm_plain
NEG=-1e9
AL='ABCDEFGHILMNOPQRSTUVZ'
def make_score(counts, alpha=0.4):
    sc={}
    for c,cc in counts.items():
        N=sum(cc.values())
        for l in AL:
            p=(cc.get(l,0)+alpha)/(N+alpha*len(AL))
            sc[(c,l)]=3.0+1.6*math.log(p*len(AL))
    return sc
DEF=3.0+1.6*math.log(1.0)   # unseen code: uniform -> 3.0
def align_soft(C,P,sc,W=170,slip_pen=6.0,null_pen=8.0,del_pen=8.0,unseen=0.0):
    n,m=len(C),len(P)
    def lo(i): return max(0,(i-W)//2)
    def hi(i): return min(m,(i+W)//2)
    dp=[dict() for _ in range(n+1)]; bk=[dict() for _ in range(n+1)]
    dp[0][0]=0.0
    for i in range(n+1):
        for j in sorted(dp[i]):
            cur=dp[i][j]
            def put(ii,jj,s,e):
                if jj<lo(ii) or jj>hi(ii): return
                if s>dp[ii].get(jj,NEG): dp[ii][jj]=s; bk[ii][jj]=e
            if i+2<=n and j<m:
                code=C[i:i+2]; ltr=P[j]
                put(i+2,j+1,cur+sc.get((code,ltr),unseen),(i,j,'S',code,ltr))
            if i+2<=n: put(i+2,j,cur-null_pen,(i,j,'N',C[i:i+2],''))
            for k in (1,3):
                if i+k<=n and j<m: put(i+k,j+1,cur-slip_pen,(i,j,'X',C[i:i+k],P[j]))
            if j<m: put(i,j+1,cur-del_pen,(i,j,'D','',P[j]))
    best=NEG;bi=bj=None
    for i in range(max(0,n-3),n+1):
        for j,v in dp[i].items():
            if v>best: best=v;bi,bj=i,j
    ops=[];i,j=bi,bj
    while bk[i].get(j) is not None:
        pi,pj,kind,code,ltr=bk[i][j]; ops.append((kind,code,ltr)); i,j=pi,pj
    ops.reverse()
    return best,ops,bj
