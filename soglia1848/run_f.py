import sys,os,subprocess,collections
if os.environ.get("PARSE")=="pairs":
    import drive as D
else:
    import drive8 as D
tag=sys.argv[1]; cand=sys.argv[2]; it,R,T0,T1,lam,n,pl=sys.argv[3:10]
fix=dict(x.split('=') for x in sys.argv[10].split(','))
C=[l.strip() for l in open(cand) if l.strip()]
# for fixed, find candidate index; letters may repeat: pick distinct copies
used=collections.Counter()
fixed={}
for t,v in fix.items():
    idxs=[i for i,c in enumerate(C) if c==v]
    if not idxs: C.append(v); idxs=[len(C)-1]
    j=idxs[min(used[v],len(idxs)-1)]; used[v]+=1
    fixed[t]=j
cand2=f'runs/{tag}.cand'; open(cand2,'w').write('\n'.join(C)+'\n')
f=open(f'runs/{tag}.seq','w'); f.write(f'{len(D.types)}\n'+' '.join(map(str,D.seq))+'\n'+' '.join(str(fixed.get(t,-1)) for t in D.types)+'\n'); f.close()
ps=[subprocess.Popen([os.path.abspath('native/isa.exe'),'lm5sp.bin',f'runs/{tag}.seq',cand2,str(sd),it,R,T0,T1,lam,f'runs/{tag}_{sd}.out',pl]) for sd in range(int(n))]
for p in ps: p.wait()
Rs=D.results(f'runs/{tag}_*.out')
for sc,m in Rs[:3]: print(f'{sc:.1f}',''.join(' ' if k<0 else C[m[k]] for k in D.seq)[:200])
top=Rs[:12]
print(' | '.join(f"{t}:{'/'.join(f'{a}{b}' for a,b in collections.Counter(C[m[i]] for sc,m in top).most_common(3))}" for i,t in enumerate(D.types) if t not in fix))
sc,m=Rs[0]
words=[];cur=[]
for u in D.U:
    if u=='_':
        if cur: words.append(cur); cur=[]
    else: cur.append(u)
if cur: words.append(cur)
print(' '.join(''.join(C[m[D.ti[u]]] if u in D.ti else '#' for u in w)+'('+'.'.join(w)+')' for w in words))
