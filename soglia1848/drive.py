import re,sys,subprocess,os,glob
def load_units(fn='ct2.txt'):
    s=open(fn).read().strip()
    out=[]
    for r in re.split('5',s):
        if len(r)%2==0: out+=[r[i:i+2] for i in range(0,len(r),2)]
        else: out+=[r[i:i+2] for i in range(0,len(r)-1,2)]+['L'+r[-1]]
        out.append('_')
    o=[]
    for u in out:
        if u=='_' and (not o or o[-1]=='_'): continue
        o.append(u)
    return o
U=load_units(os.environ.get('CT','ct2.txt'))
types=sorted(set(u for u in U if u!='_'))
ti={t:i for i,t in enumerate(types)}
seq=[-1 if u=='_' else ti[u] for u in U]
def write_seq(fn,fixed=None):
    f=open(fn,'w'); f.write(f'{len(types)}\n'+' '.join(map(str,seq))+'\n')
    if fixed: f.write(' '.join(str(fixed.get(t,0)) for t in types)+'\n')
    f.close()
def show(m):
    return ''.join(' ' if k<0 else chr(96+m[k]) for k in seq)
def results(pat):
    R=[]
    for f in glob.glob(pat):
        for l in open(f):
            sc,k=l.split('\t'); R.append((float(sc),list(map(int,k.split()))))
    return sorted(R,reverse=True)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='run':
        tag,lm,iters,R,T0,T1,n=sys.argv[2:9]
        write_seq(f'runs/{tag}.seq')
        ps=[subprocess.Popen([os.path.abspath('native/hsa.exe'),lm,f'runs/{tag}.seq',str(sd),iters,R,T0,T1,f'runs/{tag}_{sd}.out']) for sd in range(int(n))]
        for p in ps: p.wait()
    R=results(f'runs/{sys.argv[2]}_*.out')
    for sc,m in R[:int(sys.argv[-1]) if mode=='show' else 6]:
        print(f'{sc:.1f}', show(m)[:220])

def run_nsa(tag,cand,iters,R,T0,T1,lam,n,pl='0.7',lm='lm5sp.bin',fixed=None):
    f=open(f'runs/{tag}.seq','w'); f.write(f'{len(types)}\n'+' '.join(map(str,seq))+'\n')
    if fixed: f.write(' '.join(str(fixed.get(t,-1)) for t in types)+'\n')
    f.close()
    ps=[subprocess.Popen([os.path.abspath('native/nsa.exe'),lm,f'runs/{tag}.seq',cand,str(sd),str(iters),str(R),str(T0),str(T1),str(lam),f'runs/{tag}_{sd}.out',str(pl)]) for sd in range(n)]
    for p in ps: p.wait()
def show_n(m,cands):
    return ''.join(' ' if k<0 else cands[m[k]] for k in seq)
