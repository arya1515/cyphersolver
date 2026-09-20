import re,sys,unicodedata
DE=set('der die das und dass er nicht sich vom dem den ist wurde auch wegen sie ihn ihm als bei nach von zu ein eine einen mit für ohne noch war wird haben hat hatte machen dass, wie aber schrieb Empfang Schreiben Antwort Vgl Arch Bibl Nunz fol pag Anm Orig'.split())
def germanish(s):
    w=re.findall(r"[A-Za-zÀ-ÿ]+", s)
    if not w: return True
    d=sum(1 for x in w if x in DE or x.lower() in DE)
    return d/len(w) > 0.10
lines=open('ed/pallotto_bd2_1629.txt',encoding='utf-8').read().split('\n')
a,b=int(sys.argv[1]),int(sys.argv[2])
out=[]
for s in lines[a-1:b]:
    t=s.strip()
    if not t or t.startswith('Digitized by') or t.startswith('Nr.'): continue
    if re.match(r'^\d{1,4}$',t) or re.match(r'^(1629|1620|1689|Aug|Ang|Aog|An[gk])\b',t): continue
    out.append(t)
txt=' '.join(out)
txt=txt.replace('¬ ','').replace('- ','')
txt=re.sub(r'\s+',' ',txt)
# OCR repairs
txt=re.sub(r'\bk\b','a',txt); txt=re.sub(r'\b[6ö]\b','o',txt); txt=re.sub(r'\b4\b','e',txt)
txt=re.sub(r'\bm[kä]\b','ma',txt); txt=re.sub(r'\bpi[uüù]\b','piu',txt)
txt=txt.replace('qa','qu').replace('sao','suo').replace('daca','duca').replace('qn','qu')
parts=re.split(r'(?<=[.!?])\s+', txt)
keep=[p for p in parts if not germanish(p)]
print(' '.join(keep))
