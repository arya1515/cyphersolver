import re,random,itertools
raw=[];GS=[]
for ln in open('desmarets1710/transcription.txt',encoding='utf-8'):
    if ln.startswith('G |'): raw.append(ln[3:])
    elif ln.startswith('C |'): GS.append(set(ln[3:].split()))
W=[set(w for w in re.sub(r"[^a-z ]"," ",r.lower().replace("'"," ")).split() if len(w)>=4) for r in raw]
n=len(W)
def score(off):
    s=c=0
    for a,b in itertools.combinations(range(n),2):
        if 0<=a+off<n and 0<=b+off<n:
            sh=len(W[a]&W[b]); 
            if sh: s+=len(GS[a+off]&GS[b+off])/sh; c+=1
    return s/max(c,1),c
base=[]
for off in range(-3,4): print(off,score(off))
# control: random pair overlap
tot=sum(len(GS[a]&GS[b]) for a,b in itertools.combinations(range(n),2))/ (n*(n-1)/2); print('mean overlap any pair',tot)
