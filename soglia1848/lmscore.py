import numpy as np
from lm import enc,A
class LM:
    def __init__(self,fn): self.lp=np.load(fn)
    def score(self,x):
        # x int array; score all 5-gram windows with padding of spaces
        x=np.concatenate([np.zeros(4,dtype=np.int64),x])
        idx=x[:-4]*A**4+x[1:-3]*A**3+x[2:-2]*A**2+x[3:-1]*A+x[4:]
        return float(self.lp[idx].sum())
if __name__=='__main__':
    import random
    L=LM('lm5sp.npy')
    s='la santita di nostro signore ha approvato il modo col quale ella ha saputo mantenere le buone relazioni colla corte imperiale'
    print(L.score(enc(s))/len(s))
    l=list(s);random.shuffle(l);print(L.score(enc(''.join(l)))/len(s))
    N=LM('lm5ns.npy'); s2=s.replace(' ','');print(N.score(enc(s2)[0:])/len(s2))
