from solve import *
NEG=-1e9
def align_band(C,P,table,W=150,ins_pen=5.0,del_pen=5.0,slip_pen=5.0,new_pen=1.2,mismatch=-4.0):
    """Banded DP: i digits vs j letters, |i-2j|<=W."""
    n,m=len(C),len(P)
    def lo(i): return max(0,(i-W)//2)
    def hi(i): return min(m,(i+W)//2)
    dp=[None]*(n+1); bk=[None]*(n+1)
    for i in range(n+1):
        a,b=lo(i),hi(i)
        dp[i]={}; bk[i]={}
    dp[0][0]=0.0
    for i in range(n+1):
        row=dp[i]
        for j in sorted(row):
            cur=row[j]
            def put(ii,jj,sc,e):
                if jj<lo(ii) or jj>hi(ii): return
                d=dp[ii]
                if sc>d.get(jj,NEG): d[jj]=sc; bk[ii][jj]=e
            if i+2<=n and j<m:
                code=C[i:i+2]; ltr=P[j]; t=table.get(code)
                sc=cur+(1.0 if t==ltr else (-new_pen if t is None else mismatch))
                put(i+2,j+1,sc,(i,j,'S',code,ltr))
            if i+2<=n: put(i+2,j,cur-ins_pen,(i,j,'N',C[i:i+2],''))
            for k in (1,3):
                if i+k<=n and j<m: put(i+k,j+1,cur-slip_pen,(i,j,'X',C[i:i+k],P[j]))
            if j<m: put(i,j+1,cur-del_pen,(i,j,'D','',P[j]))
    best=NEG;bi=bj=None
    for i in range(max(0,n-3),n+1):
        for j,v in dp[i].items():
            if v>best: best=v;bi,bj=i,j
    ops=[];i,j=bi,bj
    while bk[i].get(j) is not None:
        pi,pj,kind,code,ltr=bk[i][j]; ops.append((kind,code,ltr,pi)); i,j=pi,pj
    ops.reverse()
    return best,ops,bj
