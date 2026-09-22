"""Hypothesis: digit = base letter; dot adds vowel Vd; mark 't' adds vowel Vt (Spanish royal-cipher style)."""
import sys,os,math,random,numpy as np
sys.path.insert(0,'..')
from lang import lm
from tok import load
LANG=os.environ.get('LANG_M','es-golden-age')
M=lm.load(LANG,order=4,spaces=False); A=M.A; IX=M.index
LET='abcdefghilmnopqrstuxyz'; VOW='aeiou'
FREQ={'e':13.7,'a':12.5,'o':8.7,'s':8,'r':6.9,'n':6.7,'i':6.3,'d':5.9,'l':5,'c':4.7,'t':4.6,'u':3.9,'m':3.2,'p':2.5,'b':1.4,'g':1,'y':.9,'q':.9,'h':.7,'f':.7,'z':.5,'x':.2}
F=np.full(A,1e-3)
for c,v in FREQ.items(): F[IX[c]]=v
F/=F.sum()
# signs: (digit, dot, mark)
seqs=[]
for p in load():
    if not p: continue
    s=[]
    for d,dot,u in p:
        if d=='?': continue
        if d=='1' and not dot and s and s[-1][0] in '245' and not s[-1][2]:
            s[-1]=(s[-1][0],s[-1][1],True); continue
        s.append((d,dot,False))
    seqs.append(s)
def text(L,vd,vt):
    return [[IX[L[int(d)]]]+([IX[vd]] if dot else [])+([IX[vt]] if mk else []) for s in seqs for (d,dot,mk) in [()] ] if False else \
      [np.array([x for (d,dot,mk) in s for x in ([IX[L[int(d)]]]+([IX[vd]] if dot else [])+([IX[vt]] if mk else []))]) for s in seqs]
def score(L,vd,vt):
    T=text(L,vd,vt); tot=sum(M.score_idx(x) for x in T); n=sum(len(x) for x in T)
    obs=np.bincount(np.concatenate(T),minlength=A)/n; m=obs>0
    return tot-3*n*float((obs[m]*np.log(obs[m]/F[m])).sum()), n
rnd=random.Random(int(sys.argv[1]))
best=None
for r in range(int(sys.argv[2])):
    L=[rnd.choice(LET) for _ in range(10)]; vd=rnd.choice(VOW); vt=rnd.choice(VOW)
    cur,n=score(L,vd,vt); T=20
    for it in range(int(os.environ.get('NIT','6000'))):
        k=rnd.randrange(12); old=(L[:],vd,vt)
        if k<10: L[k]=rnd.choice(LET)
        elif k==10: vd=rnd.choice(VOW)
        else: vt=rnd.choice(VOW)
        v,n=score(L,vd,vt)
        if v>cur or rnd.random()<math.exp((v-cur)/T): cur=v
        else: L,vd,vt=old
        T=max(0.3,T*0.999)
    print(r,round(cur/n,3),''.join(L),vd,vt,flush=True)
    if best is None or cur>best[0]: best=(cur,L[:],vd,vt)
_,L,vd,vt=best
for x in text(L,vd,vt): print(''.join(M.alpha[i] for i in x)[:300])
