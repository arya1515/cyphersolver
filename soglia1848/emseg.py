import collections,math,sys
s=open('ct.txt').read()
N=len(s); L=int(sys.argv[1]) if len(sys.argv)>1 else 4
# init: all substrings
p=collections.Counter()
for n in range(1,L+1):
    for i in range(N-n+1): p[s[i:i+n]]+=1
tot=sum(p.values()); p={k:v/tot for k,v in p.items()}
lenpen=float(sys.argv[2]) if len(sys.argv)>2 else 0.0
for it in range(60):
    # forward-backward
    a=[0.0]*(N+1); a[0]=1.0
    for i in range(N):
        if a[i]==0: continue
        for n in range(1,L+1):
            if i+n<=N:
                w=s[i:i+n]
                if w in p: a[i+n]+=a[i]*p[w]
        # scale not needed? use logs if underflow
    # use log-space instead
    la=[-1e300]*(N+1); la[0]=0
    def lse(x,y):
        if x<y: x,y=y,x
        return x+math.log1p(math.exp(y-x)) if y>-1e299 else x
    for i in range(N):
        for n in range(1,L+1):
            if i+n<=N and s[i:i+n] in p:
                la[i+n]=lse(la[i+n],la[i]+math.log(p[s[i:i+n]])+lenpen)
    lb=[-1e300]*(N+1); lb[N]=0
    for i in range(N-1,-1,-1):
        for n in range(1,L+1):
            if i+n<=N and s[i:i+n] in p:
                lb[i]=lse(lb[i],lb[i+n]+math.log(p[s[i:i+n]])+lenpen)
    Z=la[N]
    c=collections.Counter()
    for i in range(N):
        for n in range(1,L+1):
            if i+n<=N and s[i:i+n] in p:
                c[s[i:i+n]]+=math.exp(la[i]+math.log(p[s[i:i+n]])+lenpen+lb[i+n]-Z)
    tot=sum(c.values())
    p={k:v/tot for k,v in c.items() if v/tot>1e-6}
print('logL',Z,'types',len(p))
# viterbi
best=[(-1e300,None)]*(N+1); best[0]=(0,None)
for i in range(N):
    for n in range(1,L+1):
        w=s[i:i+n]
        if i+n<=N and w in p:
            v=best[i][0]+math.log(p[w])
            if v>best[i+n][0]: best[i+n]=(v,i)
seg=[];j=N
while j>0:
    i=best[j][1]; seg.append(s[i:j]); j=i
seg=seg[::-1]
print(' '.join(seg))
C=collections.Counter(seg)
print(len(seg),len(C))
print(sorted(C.items(),key=lambda x:-x[1])[:80])
print('length dist',collections.Counter(len(x) for x in seg))
