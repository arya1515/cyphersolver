# Iterated coordinate ascent for the cluster -> polyphonic class assignment (objective as in anneal_poly).
# usage: climb_poly.py clusters.json seps junk rounds seed [maxlines] [page_key]
import sys, json, random, numpy as np, os, time
sys.path.insert(0,'sega1593')
import anneal_poly as A
cl=json.load(open(sys.argv[1]))
if len(sys.argv)>7: cl=cl[sys.argv[7]]
seps=set(int(x) for x in sys.argv[2].split(',') if x); junk=set(int(x) for x in sys.argv[3].split(',') if x)
rounds=int(sys.argv[4]); seed=int(sys.argv[5]); maxl=int(sys.argv[6]) if len(sys.argv)>6 else 10**6
toks=[]
for k in sorted(cl,key=int)[:maxl]: toks+=[c for c in cl[k] if c not in junk]
tokens=np.array(toks,np.int64); ncl=int(tokens.max())+1
present=set(toks); free=[c for c in range(ncl) if c not in seps and c in present]
counts=np.bincount(tokens,minlength=ncl).astype(float); nonsep=sum(counts[c] for c in free)
EXP=np.array([0.1524,0.064,0.064,0.057,0.2301,0.0913,0.0824,0.088,0.082,0.0574,0.0315,0.012,0.005,0.006]); EXP=EXP/EXP.sum()
LAM=float(os.environ.get('LAM','4.0')); B=int(os.environ.get('BEAM','48'))
names=A.PAIRS+A.CODES+['SEP']
from wordscore import WordScorer
WS=WordScorer(); MU=float(os.environ.get('MU','0'))
def score(mp):
    if MU>0:
        s,seq=A.beam_text(tokens,mp,A.tab,A.opt_n,A.opt_len,A.opt_seq,B)
        txt=''.join(A.ALPHA[i] for i in seq)
        s+=MU*len(txt)*WS.score(txt)
    else:
        s,nl=A.beam(tokens,mp,A.tab,A.opt_n,A.opt_len,A.opt_seq,B)
    f=np.zeros(A.NCLS+1)
    for c in free: f[mp[c]]+=counts[c]
    fp=f[:14]/max(1.0,f[:14].sum())
    return s-LAM*nonsep*np.abs(fp-EXP).sum()
def freq_init(rnd):
    mp=np.full(ncl,A.NCLS,np.int64)
    order=sorted(free,key=lambda c:-counts[c])
    if rnd: rnd.shuffle(order)
    NC=int(os.environ.get('NCLASS','11')); mass=np.zeros(14); target=EXP*nonsep; target[NC:]=-1e9
    for c in order:
        # assign to the pair with the largest remaining deficit
        p=int(np.argmax(target-mass)); mp[c]=p; mass[p]+=counts[c]
    return mp
def climb(mp,cur):
    improved=True; sweeps=0
    while improved and sweeps<6:
        improved=False; sweeps+=1
        for c in sorted(free,key=lambda c:-counts[c]):
            best=cur; bestv=mp[c]
            for v in range(int(os.environ.get("NCLASS","11"))):
                if v==mp[c]: continue
                old=mp[c]; mp[c]=v; s=score(mp); mp[c]=old
                if s>best+1e-6: best=s; bestv=v
            if bestv!=mp[c]: mp[c]=bestv; cur=best; improved=True
        # pair swaps
        for i in range(len(free)):
            for j in range(i+1,len(free)):
                a,b=free[i],free[j]
                if mp[a]==mp[b]: continue
                mp[a],mp[b]=mp[b],mp[a]; s=score(mp)
                if s>cur+1e-6: cur=s; improved=True
                else: mp[a],mp[b]=mp[b],mp[a]
        print(f'  sweep {sweeps} score {cur:.1f}',flush=True)
    return mp,cur
rnd=random.Random(seed)
t0=time.time()
mp=freq_init(None); cur=score(mp); print('init',round(cur,1),flush=True)
mp,cur=climb(mp,cur); best=(cur,mp.copy())
NR=int(os.environ.get('RANDSTARTS','0'))
for r in range(NR):
    mp2=freq_init(rnd); s=score(mp2); mp2,s=climb(mp2,s)
    print(f'randstart {r} {s:.1f} best {best[0]:.1f} {time.time()-t0:.0f}s',flush=True)
    if s>best[0]: best=(s,mp2.copy())
for r in range(rounds):
    mp2=best[1].copy()
    for _ in range(rnd.randint(2,4)):
        c=rnd.choice(free); mp2[c]=rnd.randrange(int(os.environ.get("NCLASS","11")))
    mp2,s=climb(mp2,score(mp2))
    print(f'round {r} {s:.1f} best {best[0]:.1f} {time.time()-t0:.0f}s',flush=True)
    if s>best[0]: best=(s,mp2.copy())
cur,mp=best
txt,sc=A.decode_text(tokens,mp,400)
print('BEST',round(cur,1)); print(txt)
print('MAP',{c:names[mp[c]] for c in free})
