import re,sys,subprocess,os,glob,collections
CT=os.environ.get('CT','ct2.txt')
def units8(fn=CT,codesp=True):
    s=open(fn).read().strip()
    out=[]
    for r in s.split('5'):
        i=0
        while i<len(r):
            if r[i]=='8' and i+4<=len(r):
                out.append('_' if codesp else 'C'+r[i:i+4]); 
                if codesp: out.append('_')
                i+=4
            elif i+2<=len(r): out.append(r[i:i+2]); i+=2
            else: out.append('L'+r[i]); i+=1
        out.append('_')
    o=[]
    for u in out:
        if u=='_' and (not o or o[-1]=='_'): continue
        o.append(u)
    return o
U=units8()
types=sorted(set(u for u in U if u!='_'))
ti={t:i for i,t in enumerate(types)}
seq=[-1 if u=='_' else ti[u] for u in U]
def results(pat):
    R=[]
    for f in glob.glob(pat):
        for l in open(f):
            sc,k=l.split('\t'); R.append((float(sc),list(map(int,k.split()))))
    return sorted(R,reverse=True)
def run_h(tag,iters,R,T0,T1,n,lm='lm5sp.bin',allowed='abcdefghilmnopqrstuvz',fixed=None):
    f=open(f'runs/{tag}.seq','w'); f.write(f'{len(types)}\n'+' '.join(map(str,seq))+'\n')
    if fixed: f.write(' '.join(str(fixed.get(t,0)) for t in types)+'\n')
    f.close()
    ps=[subprocess.Popen([os.path.abspath('native/hsa.exe'),lm,f'runs/{tag}.seq',str(sd),str(iters),str(R),str(T0),str(T1),f'runs/{tag}_{sd}.out',allowed]) for sd in range(n)]
    for p in ps: p.wait()
def show(m): return ''.join(' ' if k<0 else chr(96+m[k]) for k in seq)
if __name__=='__main__':
    tag=sys.argv[1]
    if len(sys.argv)>2: run_h(tag,*sys.argv[2:6],int(sys.argv[6]))
    Rs=results(f'runs/{tag}_*.out')
    for sc,m in Rs[:6]: print(f'{sc:.1f}',show(m)[:250])
    sc,m=Rs[0]; print({t:chr(96+m[i]) for i,t in enumerate(types)})
    print(len(types),'types', sum(1 for k in seq if k>=0),'tokens')
