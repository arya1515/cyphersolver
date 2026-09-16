"""Structural tests on the 1..52 permutation hidden in the Roosevelt 1935 number block."""
import random, itertools, collections
SEQ=[1,7,2,10,15,17,19,21,26,8,32,33,20,37, 16,27,12,34,38,28,22,39,40,41,42,48,44, 9,3,13, 18,4,23,24,46,29,35,51,5,43,47, 6,11,36,50,52,30,49,45,25,31,14]
GROUPS=[SEQ[0:14],SEQ[14:27],SEQ[27:30],SEQ[30:41],SEQ[41:52]]  # separated by 000000, 000000, 000, 000
assert sorted(SEQ)==list(range(1,53))
n=52
def rising_sequences(s):
    pos={v:i for i,v in enumerate(s)}
    return 1+sum(1 for v in range(1,n) if pos[v+1]<pos[v])
def stats(s):
    m=(n+1)/2
    rho=sum((i+1-m)*(v-m) for i,v in enumerate(s))/sum((i+1-m)**2 for i in range(n))
    plus1=sum(1 for a,b in zip(s,s[1:]) if b==a+1)
    comp=sum(1 for a,b in zip(s,s[1:]) if a+b==53)
    return rho,plus1,rising_sequences(s),comp
obs=stats(SEQ)
print('observed: rho=%.3f  +1 adjacencies=%d  rising sequences=%d  adjacent complement pairs (sum 53)=%d'%obs)
random.seed(7); N=200000; ge=[0]*4; le=[0]*4
for _ in range(N):
    s=SEQ[:]; random.shuffle(s); st=stats(s)
    for k in range(4):
        ge[k]+= st[k]>=obs[k]; le[k]+= st[k]<=obs[k]
print('p(>=obs) uniform shuffle:',[c/N for c in ge]); print('p(<=obs):',[c/N for c in le])
print('group boundaries (last, first, sum):',[(g[-1],h[0],g[-1]+h[0]) for g,h in zip(GROUPS,GROUPS[1:])])
print('all adjacent pairs summing to 53:',[(i,a,b) for i,(a,b) in enumerate(zip(SEQ,SEQ[1:])) if a+b==53])
pos={v:i for i,v in enumerate(SEQ)}
print('complement position pairs (pos v, pos 53-v, diff):')
print(sorted((pos[v],pos[53-v],pos[53-v]-pos[v]) for v in range(1,27)))
print('positions of singles 1..9:',[(v,pos[v]) for v in range(1,10)])
print('group sums:',[sum(g) for g in GROUPS],'group lens:',[len(g) for g in GROUPS])
# rising-sequence count vs riffle shuffles of an ordered deck (GSR model)
def gsr(deck):
    k=sum(random.random()<0.5 for _ in deck); a,b=deck[:k],deck[k:]; out=[]
    while a or b:
        if random.random()<len(a)/(len(a)+len(b)): out.append(a.pop(0))
        else: out.append(b.pop(0))
    return out
for r in range(1,8):
    c=collections.Counter()
    for _ in range(20000):
        d=list(range(1,53))
        for _ in range(r): d=gsr(d)
        c[rising_sequences(d)]+=1
    tot=sum(c.values()); mean=sum(k*v for k,v in c.items())/tot
    print('riffles',r,'mean rising seqs %.1f'%mean,'P(rs=%d)=%.3f'%(obs[2],c[obs[2]]/tot))

# joint check: under k GSR riffles of an ordered deck, how often do (rising sequences <= 16) AND (rho >= 0.387) AND (+1 adjacencies >= 5) hold?
random.seed(11)
for r in (3,4,5,6):
    hit=0; M=20000
    for _ in range(M):
        d=list(range(1,53))
        for _ in range(r): d=gsr(d)
        st=stats(d)
        hit+= st[2]<=obs[2] and st[0]>=obs[0] and st[1]>=obs[1]
    print('riffles',r,'P(rs<=16 & rho>=.387 & +1>=5) = %.3f'%(hit/M))
hit=0
for _ in range(200000):
    s=SEQ[:]; random.shuffle(s); st=stats(s); hit+= st[2]<=obs[2] and st[0]>=obs[0] and st[1]>=obs[1]
print('uniform  P(joint) =',hit/200000)
