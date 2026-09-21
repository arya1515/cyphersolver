import sys,random,math
sys.path.insert(0,'..')
from lang import lm
M=lm.load('fr-1530-despatches',order=5,spaces=False)
rows=[l.split()[1:] for l in open('guiche_ct.txt') if l.startswith('L')]
toks=[s for r in rows for s in r]
key=dict(x.split('=') for x in "3=e t=r #=i e=u Q=t B=s r=a f=d d=n 4=o p=c W=l F=q D=m o=o P=y A=v g=f 8=p X=g c=z 5=x".split())
fixed=set('3 t # e Q B r d 4 W D P A g 8'.split())
S=list(key); A='abcdefghilmnopqrstuxyz'
def dec(k): return ''.join(k[s] for s in toks)
def sc(k): return M.score_idx(M.encode(dec(k)))
best=(sc(key),dict(key))
for run in range(6):
    k=dict(best[1]); s=sc(k); T=0.5
    for it in range(20000):
        k2=dict(k); x=random.choice([s_ for s_ in S if s_ not in fixed]); k2[x]=random.choice(A)
        s2=sc(k2)
        if s2>s or random.random()<math.exp((s2-s)/T): k,s=k2,s2
        T=max(0.02,T*0.9997)
    if s>best[0]: best=(s,k)
s,k=best; print(s/len(toks)); print(' '.join(f'{a}={b}' for a,b in k.items()))
for r in rows: print(''.join(k[x] for x in r))
