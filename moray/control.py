# matched synthetic controls: 134-char Scots plaintext, 32 symbols (26 letters present? no: mimic ciphertext profile)
import random,re,sys,collections
from lm import clean
from solve import anneal,decode,AL
ho=open('corpus/historielifeofki00colvuoft.txt',encoding='utf-8',errors='ignore').read()
# held-out text: Historie of James the Sext (not in LM)
txt=re.sub(r' +','',clean(ho))
rnd=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 1)
N=134
results=[]
for trial in range(int(sys.argv[2]) if len(sys.argv)>2 else 6):
    while True:
        i=rnd.randrange(200000,len(txt)-N)
        p=txt[i:i+N]
        if len(set(p))>=17: break
    # key: each letter one symbol, plus 6 extra homophones on the most frequent letters -> ~32 symbols total among those present
    freq=collections.Counter(p)
    syms={}
    letters=sorted(freq)
    sid=0
    for L in letters:
        syms[L]=[f's{sid}']; sid+=1
    for L,_ in freq.most_common(6):
        syms[L].append(f's{sid}'); sid+=1
    ct=[rnd.choice(syms[c]) for c in p]
    S=sorted(set(ct))
    best=None
    for r in range(12):
        b,k=anneal(ct,S,seed=r)
        if best is None or b>best[0]: best=(b,k)
    dec=decode(ct,best[1])
    acc=sum(a==b for a,b in zip(dec,p))/N
    results.append(acc)
    print(f'trial {trial} distinct={len(S)} acc={acc:.2f}\n  P {p}\n  D {dec}',flush=True)
print('mean acc',sum(results)/len(results))
