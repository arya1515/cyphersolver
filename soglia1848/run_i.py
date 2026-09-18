import sys,os,subprocess
import os
if os.environ.get("PARSE")=="pairs":
    import drive as D
else:
    import drive8 as D
tag=sys.argv[1]; cand=sys.argv[2]; it,R,T0,T1,lam,n,pl=sys.argv[3:10]
lm=sys.argv[10] if len(sys.argv)>10 else 'lm5sp.bin'
f=open(f'runs/{tag}.seq','w'); f.write(f'{len(D.types)}\n'+' '.join(map(str,D.seq))+'\n'); f.close()
ps=[subprocess.Popen([os.path.abspath('native/isa.exe'),lm,f'runs/{tag}.seq',cand,str(sd),it,R,T0,T1,lam,f'runs/{tag}_{sd}.out',pl]) for sd in range(int(n))]
for p in ps: p.wait()
C=[l.strip() for l in open(cand) if l.strip()]
Rs=D.results(f'runs/{tag}_*.out')
for sc,m in Rs[:5]: print(f'{sc:.1f}',''.join(' ' if k<0 else C[m[k]] for k in D.seq)[:300])
sc,m=Rs[0]; print({t:C[m[i]] for i,t in enumerate(D.types)})
