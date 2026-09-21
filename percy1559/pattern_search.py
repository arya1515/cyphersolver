"""Word-pattern search: each shape+mark is one symbol; find vocab words fitting all cipher words consistently."""
import re, collections, sys, itertools
L=[["F","B_","E_","I_","E","H^"],["C","G:"],["C","E","B","G.","E"],["E","F","Y","X"],["I_","E_","C:","A:","B","E","6"]]
L2=[["E","Ii","Y"],["C:","B","h","E","A:","C_","A","C","E"]]
L3=[["C_","E_","B_","G","E","Y","X"],["F_","B_","G.","h_","B_","P","6"]]
L4=[["C_","E_","B_","G","E","P"],["F_","B_","G.","E_","B_","Y","X"]]
lines={'1':L,'2':L2,'3':L3,'4':L4}
txt=open('../burghley1559/sadler1.txt',encoding='utf-8',errors='ignore').read()+open('../throckmorton/sources/forbes1.txt',encoding='utf-8',errors='ignore').read().replace('ſ','s')
cnt=collections.Counter(w for w in re.findall(r'[a-z]+',txt.lower()))
names="knox knoxe prior priour lord lorde laird lairde whitlaw whitlawe whitelawe kirkaldy kirkaldye grange james hume dowager congregation croftes croft cecil percy hathington merse tivdale lordes".split()
for n in names: cnt[n]+=1000
vocab=[w for w,c in cnt.items() if c>=3 and len(w)<=10]
def pat(ws): 
    m={};return tuple(m.setdefault(s,len(m)) for s in ws)
bypat=collections.defaultdict(list)
for w in vocab: bypat[pat(w)].append(w)
for k,words in lines.items():
    for cw in words:
        c=bypat[pat(cw)]; c.sort(key=lambda w:-cnt[w])
        print(k,' '.join(cw),len(c),c[:25])
