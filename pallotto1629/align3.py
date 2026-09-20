from solve import load_doc, norm_plain
from collections import Counter, defaultdict
NEG=-1e9
LENBONUS={1:-1.0,2:0.0,3:-1.0}
def align_var(C,P,table,W=140,null_pen=6.0,del_pen=6.0,unk_pen=1.5,mis_pen=-5.0):
    n,m=len(C),len(P)
    def lo(i): return max(0,(i-W)//2)
    def hi(i): return min(m,(i+W)//2)
    dp=[dict() for _ in range(n+1)]; bk=[dict() for _ in range(n+1)]
    dp[0][0]=0.0
    for i in range(n+1):
        row=dp[i]
        for j in sorted(row):
            cur=row[j]
            def put(ii,jj,sc,e):
                if jj<lo(ii) or jj>hi(ii): return
                if sc>dp[ii].get(jj,NEG): dp[ii][jj]=sc; bk[ii][jj]=e
            for k in (1,2,3):
                if i+k<=n and j<m:
                    code=C[i:i+k]; ltr=P[j]; t=table.get(code)
                    base=LENBONUS[k]
                    sc=cur+base+(2.0 if t==ltr else (-unk_pen if t is None else mis_pen))
                    put(i+k,j+1,sc,(i,j,'S',code,ltr))
                if i+k<=n:
                    put(i+k,j,cur-null_pen,(i,j,'N',C[i:i+k],''))
            if j<m: put(i,j+1,cur-del_pen,(i,j,'D','',P[j]))
    best=NEG;bi=bj=None
    for i in range(max(0,n-2),n+1):
        for j,v in dp[i].items():
            if v>best: best=v;bi,bj=i,j
    ops=[];i,j=bi,bj
    while bk[i].get(j) is not None:
        pi,pj,kind,code,ltr=bk[i][j]; ops.append((kind,code,ltr)); i,j=pi,pj
    ops.reverse()
    return best,ops,bj
def votes_of(ops):
    v=defaultdict(Counter)
    for k,c,l in ops:
        if k=='S': v[c][l]+=1
    return v
