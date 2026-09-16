"""Permutation control for the core alphabet: score the maximal runs of 20-115 tokens under Pitt's row
against random rows (same periodic structure, letter identities permuted)."""
import key, lm4, random, statistics
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
print('runs of >=4 core tokens:',len(runs),'tokens',sum(map(len,runs)))
def sc(row):
    return sum(lm4.score(''.join(row[(n-20)%24] for n in r)) for r in runs)
real=sc(key.ROW)
random.seed(1)
null=[]
for i in range(20000):
    row=list(key.ROW); random.shuffle(row); null.append(sc(row))
mu=statistics.mean(null); sd=statistics.pstdev(null)
print(f'real {real:.1f}  null mean {mu:.1f} sd {sd:.1f}  z={(real-mu)/sd:.1f}  max null {max(null):.1f}  #null>=real {sum(1 for x in null if x>=real)}')
# alternative periods: best-of-hillclimb for each period p, offset 20, 24-letter alphabet cycled
def climb(p, iters=3000):
    best=None
    for restart in range(3):
        row=list(key.ROW); random.shuffle(row)
        def s(row): return sum(lm4.score(''.join(row[(n-20)%p] if (n-20)%p<24 else 'e' for n in r)) for r in runs)
        cur=s(row)
        for it in range(iters):
            i,j=random.sample(range(24),2); row[i],row[j]=row[j],row[i]
            ns=s(row)
            if ns>=cur: cur=ns
            else: row[i],row[j]=row[j],row[i]
        if best is None or cur>best: best=cur
    return best
for p in [22,23,24,25,26]:
    print('period',p,'best climbed score',round(climb(p),1))
