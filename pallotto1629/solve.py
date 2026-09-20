import re, sys, json
from collections import defaultdict, Counter

def load_doc(path):
    """Return (digits, meta_lines). Strips uncertainty markers, keeps first alternative."""
    out=[]; meta=[]
    for line in open(path, encoding='utf-8', errors='replace'):
        s=line.rstrip('\n')
        if s.startswith('#') or s.startswith('<'):
            meta.append(s); continue
        # tokens like  "6/9?"  "2/7?"  "0?^5?"
        s=s.replace('^',' ')
        toks=s.split()
        for t in toks:
            t=t.replace('?','')
            if '/' in t: t=t.split('/')[0]
            for ch in t:
                if ch.isdigit(): out.append(ch)
    return ''.join(out), meta

def norm_plain(t):
    t=t.lower()
    repl={'à':'a','è':'e','é':'e','ì':'i','ò':'o','ù':'u','’':"'",'“':'','”':''}
    for k,v in repl.items(): t=t.replace(k,v)
    t=re.sub(r"[^a-z]", "", t)
    t=t.replace('v','u') if False else t
    return t.upper()

def align(C, P, table, ins_pen=6.0, del_pen=8.0, slip_pen=6.0, new_pen=1.5):
    """DP: align digit string C to plaintext P. Returns (score, ops)."""
    n,m=len(C),len(P)
    NEG=-1e9
    import array
    prev=[NEG]*(m+1); prev[0]=0.0
    bt={}
    # dp over i (digits consumed) and j (letters consumed) -- do full 2D
    dp=[[NEG]*(m+1) for _ in range(n+1)]
    bk=[[None]*(m+1) for _ in range(n+1)]
    dp[0][0]=0.0
    for i in range(n+1):
        row=dp[i]
        for j in range(m+1):
            cur=row[j]
            if cur==NEG: continue
            # normal: 2 digits -> 1 letter
            if i+2<=n and j<m:
                code=C[i:i+2]; ltr=P[j]
                t=table.get(code)
                if t is None: sc=cur-new_pen
                elif t==ltr: sc=cur+1.0
                else: sc=cur-4.0
                if sc>dp[i+2][j+1]: dp[i+2][j+1]=sc; bk[i+2][j+1]=(i,j,'S',code,ltr)
            # null: 2 digits -> 0 letters
            if i+2<=n:
                sc=cur-ins_pen
                if sc>dp[i+2][j]: dp[i+2][j]=sc; bk[i+2][j]=(i,j,'N',C[i:i+2],'')
            # slip: 1 or 3 digits -> 1 letter
            for k in (1,3):
                if i+k<=n and j<m:
                    sc=cur-slip_pen
                    if sc>dp[i+k][j+1]: dp[i+k][j+1]=sc; bk[i+k][j+1]=(i,j,'X',C[i:i+k],P[j])
            # deletion: 0 digits -> 1 letter
            if j<m:
                sc=cur-del_pen
                if sc>row[j+1]: row[j+1]=sc; bk[i][j+1]=(i,j,'D','',P[j])
    # find best end: consumed all plaintext, as many digits as possible
    best=None
    for i in range(n+1):
        if dp[i][m]>NEG and (best is None or dp[i][m]>dp[best][m]): best=i
    ops=[]; i,j=best,m
    while (i,j)!=(0,0):
        e=bk[i][j]
        if e is None: break
        pi,pj,kind,code,ltr=e
        ops.append((kind,code,ltr,pi))
        i,j=pi,pj
    ops.reverse()
    return dp[best][m], ops, best

def build_table(ops):
    votes=defaultdict(Counter)
    for kind,code,ltr,_ in ops:
        if kind=='S': votes[code][ltr]+=1
    tbl={}; conf={}
    for code,c in votes.items():
        ltr,n=c.most_common(1)[0]
        tbl[code]=ltr; conf[code]=(n,sum(c.values()),dict(c))
    return tbl, conf
