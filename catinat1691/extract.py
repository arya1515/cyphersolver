# Extract the Grand Chiffre 1691 letters printed in cipher in Memoires de Catinat (1819) t. II pp. 295-342
# (MDZ bsb10720287 scans 329-376) from the MDZ hOCR text, segment into letters, decode with Bazeries' table.
import re, json, os, sys, unicodedata
HERE=os.path.dirname(os.path.abspath(__file__))
FEU=os.path.join(HERE,'..','feuquieres')
t=open(os.path.join(FEU,'catinat1819_bsb10720287.txt'),encoding='utf-8').read()
pages=re.split(r'\n=====SCAN (\d+)=====\n',t)
d={int(pages[i]):pages[i+1] for i in range(1,len(pages),2)}
tab={}
for l in open(os.path.join(FEU,'grand_chiffre_1691.tsv'),encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    n,v=l.rstrip('\n').split('\t'); tab[int(n)]=v
FIRST,LAST=329,376
toks=[]   # (scan, kind, text)  kind: num | word | flag
for s in range(FIRST,LAST+1):
    x=d[s]
    x=re.sub(r'bsb\d+_\d+','',x)
    x=re.sub(r'^\s*(\d{3}\s+PI[EÈ]CES|JUSTIFICATIVES\s*\.\s*\d{3})','',x.strip())
    x=re.sub(r'T\.\s*II\s*\.\s*\d+\s*$','',x.strip())   # signature mark
    for m in re.finditer(r'\d+[a-z]+\d*|\d+|[^\s\d\.,;:]+',x):
        tok=m.group(0)
        if re.fullmatch(r'\d+',tok): toks.append((s,'num',tok))
        elif re.fullmatch(r'\d+[a-z]+\d*',tok): toks.append((s,'flag',tok))
        else: toks.append((s,'word',tok))
# segment letters at "( n ) Page NN"
letters=[]; cur=None
i=0
while i<len(toks):
    s,k,tx=toks[i]
    if k=='word' and tx=='(' and i+4<len(toks) and toks[i+1][1]=='num' and toks[i+2][2]==')' and toks[i+3][2].lower().startswith('page'):
        cur={'n':int(toks[i+1][2]),'ref_page':toks[i+4][2],'start_scan':s,'items':[]}
        letters.append(cur); i+=5; continue
    if cur is not None: cur['items'].append((s,k,tx))
    i+=1
def dec(n):
    v=tab.get(n)
    if v is None: return f'[{n}!]'
    if v=='?': return f'[{n}?]'
    return v
out=[]
summary=[]
for L in letters:
    nums=[it for it in L['items'] if it[1]=='num']
    flags=[it for it in L['items'] if it[1]=='flag']
    hi=[it for it in nums if int(it[2])>587]
    # header = leading words before first run of >=5 numbers
    head=[]; 
    for it in L['items'][:80]:
        if it[1]=='word': head.append(it[2])
        elif it[1]=='num' and len(head)>0 and sum(1 for j in L['items'][:80] if j[1]=='num')>5: pass
    summary.append((L['n'],L['ref_page'],L['start_scan'],L['start_scan']-34,len(nums),len(hi),len(flags),' '.join(head[:25])))
    lines=[f"### Letter ({L['n']}) ref. Page {L['ref_page']}  starts t. II p. {L['start_scan']-34} (scan {L['start_scan']}); {len(nums)} groups, {len(hi)} >587, {len(flags)} OCR-merged"]
    # render in order: words as <...>, numbers decoded; page breaks marked
    buf=[]; comp=[]; last=None
    for s,k,tx in L['items']:
        if s!=last:
            buf.append(f'\n[p.{s-34}]'); last=s
        if k=='word': buf.append(f'<{tx}>'); comp.append(f' <{tx}> ')
        elif k=='flag': buf.append(f'[{tx}!]'); comp.append(f'[{tx}!]')
        else:
            v=dec(int(tx)); buf.append(v)
            if v in ('NULL',): comp.append(' | ')
            elif v=='CANCEL': comp.append(' <CANCEL> ')
            elif v.startswith('['): comp.append(v)
            elif len(re.sub(r'[^A-Za-z]','',v))<=3 and ' ' not in v: comp.append(v.lower())   # letter / syllable
            else: comp.append(' '+v+' ')
    lines.append('GROUPS+UNITS:'+' '.join(buf))
    lines.append('\nCOMPACT:'+re.sub(r'\s+',' ',''.join(comp)))
    out.append('\n'.join(lines))
open(os.path.join(HERE,'reading_raw.txt'),'w',encoding='utf-8').write('\n\n'.join(out))
json.dump([{k:(v if k!='items' else v) for k,v in L.items()} for L in letters],open(os.path.join(HERE,'letters.json'),'w',encoding='utf-8'))
print('letters',len(letters),'total groups',sum(x[4] for x in summary))
for x in summary: print(x)
