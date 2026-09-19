import sys,glob
import hsolve,solve as B
from parse import segs
S=[s.replace('5','').replace('8','') for f in sorted(glob.glob('decode/DOC*.txt')) for s in segs(f)]
segsT=[[s[i:i+2] for i in range(0,len(s)-1,2)] for s in S]
syms=sorted({t for sg in segsT for t in sg}); idx={t:i for i,t in enumerate(syms)}
segsI=[[idx[t] for t in sg] for sg in segsT if len(sg)>=4]
nt=sum(map(len,segsI))
sc,key=hsolve.run(segsI,len(syms),int(sys.argv[1]),int(sys.argv[2]))
print(round(sc/nt,3));print(' '.join(f'{s}={k}' for s,k in zip(syms,key)))
print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:2500])
