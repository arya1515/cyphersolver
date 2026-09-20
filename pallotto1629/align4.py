from solve import load_doc, norm_plain
from collections import Counter, defaultdict
NEG=-1e9
def align2r(C,P,table,W=140,null_pen=7.0,del_pen=7.0,unk_pen=1.5,mis_pen=-5.0,slip_pen=7.0,hit=2.0):
    """2-digit codes; 1/3-digit 'resync' ops model transcription slips (not learned)."""
    n,m=len(C),len(P)
    def lo(i): return max(0,(i-W)//2)
    def hi(i): return min(m,(i+W)//2)
    dp=[dict() for _ in range(n+1)]; bk=[dict() for _ in range(n+1)]
    dp[0][0]=0.0
    for i in range(n+1):
        for j in sorted(dp[i]):
            cur=dp[i][j]
            def put(ii,jj,sc,e):
                if jj<lo(ii) or jj>hi(ii): return
                if sc>dp[ii].get(jj,NEG): dp[ii][jj]=sc; bk[ii][jj]=e
            if i+2<=n and j<m:
                code=C[i:i+2]; ltr=P[j]; t=table.get(code)
                sc=cur+(hit if t==ltr else (-unk_pen if t is None else mis_pen))
                put(i+2,j+1,sc,(i,j,'S',code,ltr))
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
def clean_votes(ops,table,run=5):
    """Only count S ops inside runs of >=run consecutive S ops that agree with table."""
    v=defaultdict(Counter); buf=[]
    def flush():
        if len(buf)>=run:
            for c,l in buf: v[c][l]+=1
        buf.clear()
    for k,c,l in ops:
        if k=='S' and (table.get(c) is None or table.get(c)==l): buf.append((c,l))
        else: flush()
    flush()
    return v
