"""Compare partition results from tri_seed*.log: score, and pairwise agreement (fraction of letter pairs that are
co-grouped identically = Rand index) against the best-scoring partition."""
import glob, re, itertools
AL='abcdefghilmnopqrstuvz'
res=[]
for f in sorted(glob.glob('tri_seed*.log')):
    for ln in open(f):
        m=re.match(r'seed (\d+) trial (\d+): (-?[\d.]+)\s+(.*)',ln.strip())
        if m: res.append((float(m.group(3)),m.group(4),f))
res.sort(reverse=True)
def groups(s):
    g={}
    for part in s.split():
        d,ls=part.split('=')
        for c in ls: g[c]=d
    return g
def rand(a,b):
    ga,gb=groups(a),groups(b); same=0; tot=0
    for x,y in itertools.combinations(AL,2):
        if x not in ga or y not in ga or x not in gb or y not in gb: continue
        tot+=1; same+= (ga[x]==ga[y])==(gb[x]==gb[y])
    return same/tot
best=res[0][1]
for sc,s,f in res: print(f'{sc:9.1f}  rand_vs_best={rand(s,best):.2f}  {s}')
