import sys,os,subprocess
from drive import types,seq,results
import drive
# no-space: drop -1 tokens
seq2=[k for k in seq if k>=0]
tag=sys.argv[1]; lm=sys.argv[2]
f=open(f'runs/{tag}.seq','w'); f.write(f'{len(types)}\n'+' '.join(map(str,seq2))+'\n'); f.close()
n=int(sys.argv[3])
ps=[subprocess.Popen([os.path.abspath('native/hsa.exe'),lm,f'runs/{tag}.seq',str(sd),'3000000','2','12','0.3',f'runs/{tag}_{sd}.out']) for sd in range(n)]
for p in ps: p.wait()
R=results(f'runs/{tag}_*.out')
for sc,m in R[:4]: print(f'{sc:.1f}',''.join(chr(96+m[k]) for k in seq2)[:250])
