"""Period scan: for each period p (offset 20), anneal a 24-letter row over the core runs; is 24 singled out?"""
import key, lm4, random, math
runs=[]
for f in ['charles.txt','nicholas.txt']:
    for line in open(f,encoding='utf-8'):
        cur=[]
        for t in key.tokens(line):
            if t.isdigit() and 20<=int(t)<=115: cur.append(int(t))
            else:
                if len(cur)>=4: runs.append(cur)
                cur=[]
        if len(cur)>=4: runs.append(cur)
def anneal(p, restarts=8, iters=40000):
    best=-1e9
    for r in range(restarts):
        row=list(key.ALPHA24)+['e']*max(0,p-24); random.shuffle(row)
        def s(row): return sum(lm4.score(''.join(row[(n-20)%p] for n in r_)) for r_ in runs)
        cur=s(row); T=8.0
        for it in range(iters):
            i,j=random.sample(range(p),2); row[i],row[j]=row[j],row[i]
            ns=s(row); d=ns-cur
            if d>=0 or random.random()<math.exp(d/T): cur=ns
            else: row[i],row[j]=row[j],row[i]
            T=max(0.3, 8.0*(1-it/iters))
            best=max(best,cur)
    return best
random.seed(2)
print('runs',len(runs),'tokens',sum(map(len,runs)),'real row score', round(sum(lm4.score(''.join(key.ROW[(n-20)%24] for n in r)) for r in runs),1))
for p in [20,21,22,23,24,25,26,27,28,30,32,48]:
    print('period',p,'best annealed',round(anneal(p),1), flush=True)
