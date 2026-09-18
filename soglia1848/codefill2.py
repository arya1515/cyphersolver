import re,numpy as np,bisect,collections,sys
sys.argv=['decode.py']
exec(open('decode.py',encoding='utf8').read().split("if __name__")[0])
from lmscore import LM
from lm import enc
L=LM('lm5sp.npy')
exec(open('windows2.py').read().split('for c in [')[0])
s=load()
fixed=dict(CODE,**CODE_GUESS)
unk=[8093,8102,8131,8136,8227,8413,8704,8734,8739,8760,8904]
cand={}
for c in unk:
    p=int(pred(c)); cand[c]=V[max(0,p-14):p+14] or ['?']
cur={c:cand[c][len(cand[c])//2] for c in unk}
def txt(cur):
    code=dict(fixed,**{str(k):v for k,v in cur.items()})
    words=[]
    for r in s.split('5'):
        i,w=0,''
        while i<len(r):
            if r[i]=='8' and i+4<=len(r): w+=' '+code.get(r[i:i+4],'')+' '; i+=4
            elif i+2<=len(r): w+=DIN.get(r[i:i+2],''); i+=2
            else: w+=' '; i+=1
        words.append(w)
    t=' '.join(words).lower().replace('è','e').replace('v','v')
    return re.sub(' +',' ',re.sub('[^a-z ]',' ',t))
for rnd in range(3):
    for c in unk:
        sc=[]
        for wd in cand[c]:
            cur2=dict(cur); cur2[c]=wd; sc.append((L.score(enc(txt(cur2))),wd))
        sc.sort(reverse=True); cur[c]=sc[0][1]
        if rnd==2: print(c,[w for _,w in sc[:6]])
print(txt(cur))
