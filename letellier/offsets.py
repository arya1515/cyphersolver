"""Test the hypothesis that each diacritic class of the 1657 Le Tellier cipher is an alphabetical CV syllabary at
consecutive numbers (like Le Tellier-Colbert ciphers 1 and 1A). Search offsets per class, score with French quadgrams."""
import re, json, math, itertools
LM=json.load(open('../richelieu/fr_quadgrams.json')); tot=sum(LM.values()); floor=math.log10(0.01/tot)
LMl={k:math.log10(v/tot) for k,v in LM.items()}
def score(s):
    s=re.sub('[^a-z]','',s)
    return sum(LMl.get(s[i:i+4],floor) for i in range(len(s)-3))/max(1,len(s)-3)
V='aeiou'; C='bcdfghjlmnpqrstvxz'
syl=[c+v for c in C for v in V]            # 90 CV syllables alphabetical
txt=open('LeTellier_Castelnau1657.txt',encoding='utf-8').read().split('estant',1)[1]
toks=txt.split()
cls=[]; 
for t in toks:
    m=re.fullmatch(r'~(\d+)',t) or re.fullmatch(r'(\d+)~',t)
    if m: cls.append(('M',int(m.group(1)))); continue
    m=re.fullmatch(r'"(\d+)',t)
    if m: cls.append(('D',int(m.group(1)))); continue
    if t.isdigit(): cls.append(('P',int(t))); continue
    cls.append(('L',t))
best=[]
letters={}  # letter tokens kept as their first letter
for oP in range(-20,80):
  for oM in range(-20,80):
    for oD in range(-20,80):
        out=[]
        for c,v in cls:
            if c=='L': out.append(v[0].lower() if v[0].isalpha() else ''); continue
            o={'P':oP,'M':oM,'D':oD}[c]; i=v-o
            out.append(syl[i] if 0<=i<len(syl) else 'x')
        s=''.join(out); sc=score(s)
        best.append((sc,oP,oM,oD,s))
best.sort(reverse=True)
for b in best[:8]: print(round(b[0],3),b[1:4],b[4][:120])
