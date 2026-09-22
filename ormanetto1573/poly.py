import sys,os
sys.path.insert(0,'..')
from lang import lm
from tok import load
LANG=os.environ.get('LANG_M','it-cinquecento')
M=lm.load(LANG,spaces=False); A,K=M.A,M.order; IDX=M.index; LP=M.lp.reshape(-1,A); MOD=A**(K-1)
def enc(s): return [IDX[c] for c in lm.norm(s,'early',False) if c in IDX]
def step(ctx,ch):
    s=0.0
    for x in ch: s+=float(LP[ctx,x]); ctx=(ctx*A+x)%MOD
    return ctx,s
POLY={'0':'an','6':'so','8':'ti','2':'re','4':'um','5':'pl','7':'bc','1':'fd','3':'gz'}
CODES={'19':'nostrosignore','29':'imperatore','39':'recatholico','49':'rechristianissimo','59':'regentedifrancia','69':'monsignordivandomo','79':'ducadi','89':'contedi','99':'monsignordi','13':'concilio','23':'vostrasignoriaillma','33':'che','43':'non','53':'per','63':'qua','73':'que','83':'qui','93':'marchesedi','15':'quest','25':'quell','35':'avis','45':'letter','55':'rispost','65':'signorivenetiani','75':'spagna','85':'francia','95':'germania',
'1.9':'italia','2.9':'elettordimperio','3.9':'havere','4.9':'havendo','5.9':'essere','6.9':'essendo','7.9':'translatione','8.9':'vostrasignoria','9.9':'suaeccellenza','1.1':'ambasciatoredi','2.1':'come','3.1':'quando','4.1':'trento','5.1':'redibohemia','6.1':"reginadinghilterra",'7.1':'reginadiscotia','8.1':'principessadispagna','9.1':'regentedifiandra'}
def items(p): return [(d,dot) for d,dot,u in p]
def moves(it,p):
    d,dot=it[p]; r=[]
    if d=='0' and dot: r+= [(1,'et',0),(1,'con',0)]
    if not dot and d in POLY: r+=[(1,c,0) for c in POLY[d]]
    if p+1<len(it):
        e,d2=it[p+1]
        k=d+('.' if d2 else '')+e if False else d+e
        if not dot and not d2 and k in CODES: r.append((2,'['+CODES[k]+']',0.5))
        k2=d+'.'+e
        if d2 and not dot and (d+'.'+e) in CODES: r.append((2,'['+CODES[d+'.'+e]+']',0.5))
    if not r: r.append((1,'{%s%s}'%(d,'.' if dot else ''),-5))
    return r
def decode(it,beam=400):
    n=len(it); st=[dict() for _ in range(n+1)]; st[0][0]=(0.0,None)
    for p in range(n):
        for ctx,(sc,_) in sorted(st[p].items(),key=lambda kv:-kv[1][0])[:beam]:
            for ln,txt,pen in moves(it,p):
                t=txt.strip('[]') if txt[0]=='[' else ('' if txt[0]=='{' else txt)
                nc,s=step(ctx,enc(t)); v=sc+s+pen
                o=st[p+ln].get(nc)
                if o is None or v>o[0]: st[p+ln][nc]=(v,(p,ctx,txt))
    ctx=max(st[n],key=lambda c:st[n][c][0]); q=n; out=[]; tot=st[n][ctx][0]
    while st[q][ctx][1]:
        p,pc,txt=st[q][ctx][1]; out.append(txt); q,ctx=p,pc
    return ''.join(reversed(out)),tot/n
for p in load():
    if p: s,sc=decode(items(p)); print(round(sc,3)); print(s[:700]); print()
