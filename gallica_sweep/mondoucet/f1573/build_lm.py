# Dense 24^5 char LM (log P(e|abcd)) over period French, interpolated absolute discounting. -> fr5.npy
import re, glob, unicodedata, numpy as np, os
ALPHA='abcdefghiklmnopqrstuxyz'
ALPHA='abcdefghiklmnopqrstuvxyz'
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..')
def norm(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    t=t.lower().replace('j','i').replace('v','u').replace('w','u')
    t=re.sub('[^a-z]+','',t); return ''.join(c for c in t if c in ALPHA)
files=(glob.glob(R+'/dubellay/ref/legrand3_*.txt')+glob.glob(R+'/nevers1593/*.txt')+glob.glob(R+'/debosnys/corpus/fr*.txt')
       +glob.glob(R+'/gallica_sweep/src/*.txt'))
T=''.join(norm(open(f,encoding='utf-8',errors='ignore').read()) for f in files)
print('chars',len(T),'files',len(files))
K=len(ALPHA); idx=np.array([ALPHA.index(c) for c in T],dtype=np.int64)
C=[None]*6
for n in range(1,6):
    code=np.zeros(len(idx)-n+1,dtype=np.int64)
    for j in range(n): code=code*K+idx[j:len(idx)-n+1+j]
    C[n]=np.bincount(code,minlength=K**n).astype(np.float64).reshape((K,)*n)
D=0.75
P=(C[1]+1)/(C[1].sum()+K)
for n in range(2,6):
    c=C[n]; ctx=c.sum(-1,keepdims=True); nz=(c>0).sum(-1,keepdims=True)
    lam=np.where(ctx>0,D*nz/np.maximum(ctx,1),1.0)
    Pn=np.where(ctx>0,np.maximum(c-D,0)/np.maximum(ctx,1),0)+lam*np.broadcast_to(P,c.shape)
    P=Pn
np.save('fr5.npy',np.log(P).astype(np.float32)); print('ok',P.shape)
