import sys,random,math
sys.path.insert(0,'..')
from lang import lm
M=lm.load('fr-1530-despatches',order=5,spaces=False)
rows=[l.split()[1:] for l in open('guiche_ct.txt') if l.startswith('L')]
toks=[s for r in rows for s in r]
S=sorted(set(toks),key=lambda s:-toks.count(s)); ix={s:i for i,s in enumerate(S)}
ct=[ix[s] for s in toks]
A=list('eatsinruolmdcpqfbghxyz')  # 22
def dec(k): return ''.join(k[c] for c in ct)
def sc(k): return M.score_idx(M.encode(dec(k)))
best=None
for run in range(int(sys.argv[1])):
    k=A[:]; random.shuffle(k); s=sc(k); T=2.0
    for it in range(30000):
        k2=k[:]; i,j=random.sample(range(22),2); k2[i],k2[j]=k2[j],k2[i]
        s2=sc(k2)
        if s2>s or random.random()<math.exp((s2-s)/T): k,s=k2,s2
        T=max(0.03,T*0.9998)
    if best is None or s>best[0]: best=(s,k[:])
    print(run,round(s/len(ct),3),dec(k)[:100],flush=True)
s,k=best
print('BEST',s/len(ct)); print(' '.join(f'{a}={b}' for a,b in zip(S,k)))
for r in rows: print(''.join(k[ix[x]] for x in r))
