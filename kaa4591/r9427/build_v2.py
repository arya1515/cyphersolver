import re
B=chr(92)
M={'4':'4','Q':'q','w':'w','E':'E','y':'y',B+'x':'x','5':'5','m':'m','H':'#','9':'9','3':'3','v':'v','p':'n','7':'7','8':'8','q':'Q?','T':'Q','^':'t','b':'b','D':'D','6':'6','r':'c','d':'d','g':'g','L':'L','P':'p','n':'m?','o':'o','+':'+','e':'a','e+':'a+','e-':'a','0':'o','X':'X','K':'J','z':'j','r+':'c+?','@':'A','x':'x','.H':'?','A':'{A}',B:'','-':''}
# gloss-proven H=u/v: (line, occurrence index of H)
HU={(1,0),(2,1),(5,1)}
EDIT={ # (page,line):[(sign,occ,new)]
('P1',11):[('#',0,'U')],('P1',12):[('#',0,'U'),('d',1,'K')],('P1',13):[('#',1,'U')],
('P1',17):[('d',-1,'K')],('P1',22):[('#',0,'#U?')],('P1',23):[('#',0,'U'),('#',1,'U?')],
('P1',24):[('8?',0,'b'),('#',1,'U')],('P1',25):[('d',1,'K')],('P1',27):[('d?',0,'K')],('P1',30):[('d',-1,'K?')],
('P2',2):[('#',1,'U')],('P2',3):[('#',0,'U')],('P2',8):[('#',0,'U')],('P2',9):[('#',0,'U?')],
('P2',11):[('d',0,'K')],('P2',18):[('#',1,'U?')],('P2',24):[('b?',0,'K'),('d',1,'b')]}
def join(toks): return ''.join(toks)
def seg(s):
    # split into bracket/brace chunks and tokens
    return re.findall(r'\[[^\]]*\]|\{[^}]*\}|\S+',s)
out=['R9427 KAA 4591 f.287, transcription v2, ALL IN R9410 CODES (sysA/signs_r9410.md; new codes K, U per sysA/r9410_split.md).',
'Lines P1.01-10 converted from R9427 codes via key_full.tsv; H split by the interlinear gloss (H=u/v -> U). {A} = R9427 sign A, no R9410 equivalent.',
'? after a sign = doubtful. See split.md.','','== P1 ==']
lines=open('transcription.txt',encoding='utf-8').read().splitlines()
for L in lines:
    m=re.match(r'P1\.(\d\d) (.*)',L)
    if m:
        n=int(m.group(1)); hi=0; res=[]
        for t in seg(m.group(2)):
            if t[0] in '[{': 
                if t.startswith('{') : continue
                res.append(t); continue
            if t=='H':
                res.append('U' if (n,hi) in HU else '#'); hi+=1; continue
            res.append(M.get(t,t+'?'))
        out.append('%02d %s'%(n,join(res)))
page=None
for L in lines:
    if L.startswith('== P1'): page='P1'; continue
    if L.startswith('== P2 =='): page='P2'; out+=['','== P2 ==']; continue
    if L.startswith('== P2 postscript'): out+=['','== P2 postscript ==']; continue
    m=re.match(r'(\d\d) (.*)',L)
    if not page or not m: continue
    n=int(m.group(1)); toks=seg(m.group(2))
    for sign,occ,new in EDIT.get((page,n),[]):
        idx=[i for i,t in enumerate(toks) if t==sign]
        if len(idx)<=occ: print("MISS",page,n,sign,occ,toks); continue
        toks[idx[occ]]=new
    out.append('%02d %s'%(n,join(t if not t.startswith('{') or 'margin' in t or 'signature' in t else '' for t in toks)))
open('transcription_v2.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
