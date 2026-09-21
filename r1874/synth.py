import sys,random,collections
sys.path.insert(0,'..'); from lang import lm
import seg
rng=random.Random(5)
src=open('prior/pp354-368.txt',encoding='utf8').read()
# use an Italian corpus file from the model cache if present
import glob
f=[p for p in glob.glob('../lang/corpora/*') ]; f=['../lang/corpora/it-renaissance.txt']
t=lm.norm(open(f[0],encoding='utf8',errors='ignore').read()[200000:260000],'early',spaces=False)[:2260]
F=collections.Counter(t); hom={}
nid=1000
for c,n in F.items():
    k=max(1,round(n/2260*120)); hom[c]=[str(nid+i) for i in range(k)]; nid+=k
seq=[('p',rng.choice(hom[c])) for c in t]
seg.seq[:]=seq
print(f[0],len(set(u for _,u in seq)))
open('synth_plain.txt','w').write(t)
