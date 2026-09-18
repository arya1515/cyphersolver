# Dense 25^5 char LM with word space ('_' index 24), period French. -> fr5sp.npy
import re, glob, unicodedata, numpy as np, os
ALPHA='abcdefghiklmnopqrstuvxyz_'
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..')
def norm(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    t=t.lower().replace('j','i').replace('v','u').replace('w','u')
    t=re.sub("[^a-z]+",' ',t); t=re.sub('[^abcdefghiklmnopqrstuxyz ]','',t.replace('v','u'))
    return re.sub(' +','_',t)
files=(glob.glob(R+'/dubellay/ref/legrand3_*.txt')+glob.glob(R+'/nevers1593/*.txt')+glob.glob(R+'/debosnys/corpus/fr*.txt')
       +glob.glob(R+'/gallica_sweep/src/*.txt'))
T=''.join(norm(open(f,encoding='utf-8',errors='ignore').read()) for f in files)
print('chars',len(T))
K=len(ALPHA); idx=np.array([ALPHA.index(c) for c in T],dtype=np.int64)
C=[None]*6
for n in range(1,6):
    code=np.zeros(len(idx)-n+1,dtype=np.int64)
    for j in range(n): code=code*K+idx[j:len(idx)-n+1+j]
    C[n]=np.bincount(code,minlength=K**n).astype(np.float64).reshape((K,)*n)
D=0.75; P=(C[1]+1)/(C[1].sum()+K)
for n in range(2,6):
    c=C[n]; ctx=c.sum(-1,keepdims=True); nz=(c>0).sum(-1,keepdims=True)
    lam=np.where(ctx>0,D*nz/np.maximum(ctx,1),1.0)
    P=np.where(ctx>0,np.maximum(c-D,0)/np.maximum(ctx,1),0)+lam*np.broadcast_to(P,c.shape)
np.save('fr5sp.npy',np.log(P).astype(np.float32)); print('ok')
