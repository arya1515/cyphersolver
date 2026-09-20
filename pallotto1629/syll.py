from solve import load_doc, norm_plain
from collections import Counter, defaultdict
NEG=-1e9
def align_syll(C,P,table,maxlen=4,W=None,unk=-0.6,mis=-6.0,hit=1.0,null_pen=5.0):
    """2-digit codes -> plaintext spans of 1..maxlen letters."""
    n2=len(C)//2; m=len(P)
    # band: letters per code roughly m/n2
    rate=m/n2; BW=max(60,int(0.06*m))
    dp=[dict() for _ in range(n2+1)]; bk=[dict() for _ in range(n2+1)]
    dp[0][0]=0.0
    for i in range(n2+1):
        ctr=int(i*rate)
        for j in sorted(dp[i]):
            cur=dp[i][j]
            def put(ii,jj,s,e):
                if abs(jj-int(ii*rate))>BW: return
                if s>dp[ii].get(jj,NEG): dp[ii][jj]=s; bk[ii][jj]=e
            if i<n2:
                code=C[2*i:2*i+2]
                for L in range(1,maxlen+1):
                    if j+L>m: break
                    sp=P[j:j+L]; t=table.get(code)
                    if t is None: s=cur+unk+0.25*L
                    elif t==sp: s=cur+hit*len(sp)
                    else: s=cur+mis
                    put(i+1,j+L,s,(i,j,'S',code,sp))
                put(i+1,j,cur-null_pen,(i,j,'N',code,''))
    best=NEG;bi=bj=None
    for j,v in dp[n2].items():
        if v>best: best=v;bi,bj=n2,j
    ops=[];i,j=bi,bj
    while bk[i].get(j) is not None:
        pi,pj,k,code,sp=bk[i][j]; ops.append((k,code,sp)); i,j=pi,pj
    ops.reverse(); return best,ops,bj
