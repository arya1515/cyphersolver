import random,re,sys,collections,numpy as np
from lm import clean
from solve4 import run
import ng5,wordscore
ho=open('corpus/historielifeofki00colvuoft.txt',encoding='utf-8',errors='ignore').read()
txt=re.sub(r' +','',clean(ho))
rnd=random.Random(int(sys.argv[1])); N=134
accs=[]
for trial in range(int(sys.argv[2])):
    while True:
        i=rnd.randrange(200000,len(txt)-N); p=txt[i:i+N]
        if len(set(p))>=17: break
    freq=collections.Counter(p); syms={}; sid=0
    for L in sorted(freq): syms[L]=[f's{sid}']; sid+=1
    top=[L for L,_ in freq.most_common(8)]
    while sid<32:
        L=rnd.choice(top); syms[L].append(f's{sid}'); sid+=1
    def enc(c):
        h=syms[c]
        if len(h)==1 or rnd.random()<0.6: return h[0]
        return rnd.choice(h[1:])
    ct=[enc(c) for c in p]
    res=run(ct,6,verbose=False)
    dec=res[0][1]; acc=sum(a==b for a,b in zip(dec,p))/N; accs.append(acc)
    pi=np.frombuffer(p.encode(),dtype=np.uint8).astype(np.int64)-97
    ts=ng5.score(ng5.load(),pi)+wordscore.score(p)
    print(f'trial {trial} distinct={len(set(ct))} acc={acc:.2f} score={res[0][0]:.1f} truescore={ts:.1f}\n  P {p}\n  D {dec}',flush=True)
print('mean acc',sum(accs)/len(accs),'n>=0.8:',sum(a>=0.8 for a in accs))
