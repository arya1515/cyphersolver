import sys,glob,collections,hs3
from parse import segs
FILES=sorted(glob.glob('decode/DOC*.txt'))+sorted(glob.glob('trans/R*.txt'))
def load(drop='58'):
  out=[]
  for f in FILES:
    for s in segs(f):
      s=''.join(c for c in s if c not in drop)
      out.append((f,s))
  return out
if __name__=='__main__':
  S=load()
  segsT=[[s[i:i+2] for i in range(0,len(s)-1,2)] for f,s in S]
  syms=sorted({t for sg in segsT for t in sg}); idx={t:i for i,t in enumerate(syms)}
  segsI=[[idx[t] for t in sg] for sg in segsT if len(sg)>=3]
  sc,key=hs3.run(segsI,len(syms),restarts=int(sys.argv[1]),W=float(sys.argv[2]),seed=int(sys.argv[3]))
  print(sc/sum(map(len,segsI)))
  print(' '.join(f'{s}={k}' for s,k in zip(syms,key)))
  print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:3000])
