"""Test swapping each token's primary letter; keep swaps that raise total beam score over all pages."""
import sys,re,glob,collections
import beam
files=sorted(glob.glob('t4*.txt'))+sorted(glob.glob('t50*.txt'))
lines=[]
for f in files:
    for l in open(f,encoding='utf-8'):
        m=re.match(r'(C\d+):\s*(.*)',l)
        if m: lines.append(m.group(2).split())
cnt=collections.Counter(t for l in lines for t in l)
def total(B=60): return sum(beam.decode(l,B=B)[0] for l in lines)
base=total(); print('base',round(base,1),'tokens',sum(cnt.values()))
ALT='aeinorstuldcpmqy'
for t,n in cnt.most_common():
    if t not in beam.C or n<4 or beam.C[t][0][0]=='': continue
    orig=list(beam.C[t]); best=(base,None)
    for a in ALT:
        if a==orig[0][0]: continue
        beam.C[t]=[(a,0)]+[(x,p) for x,p in orig if x!=a]
        s=total()
        if s>best[0]+2: best=(s,a)
    if best[1]:
        beam.C[t]=[(best[1],0)]+[(x,p) for x,p in orig if x!=best[1]]
        print(f'{t} ({n}): {orig[0][0]} -> {best[1]}  gain {best[0]-base:.1f}',flush=True); base=best[0]
    else: beam.C[t]=orig
