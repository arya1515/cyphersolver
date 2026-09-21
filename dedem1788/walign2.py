# leave-one-out hard EM (ICM) word aligner with random restarts
import sys,math,collections,random,json
import walign as W, align as A
sys.stdout.reconfigure(encoding='utf-8')
SKIP=6.0
def run(DATA,iters,seed):
    rnd=random.Random(seed)
    cnt=collections.defaultdict(collections.Counter); prev={}
    for it in range(iters):
        noise=2.0*(1-it/iters)
        for n,t,w in DATA:
            # remove this letter's contribution
            for (i,ph) in prev.get(n,{}).items(): cnt[t[i]][ph]-=1
            def cost(i,tok,ph):
                if tok=='*': return 1.0*len(ph)
                if tok[0]=='=':
                    if len(ph)!=1: return 99
                    return 0 if ph[0]==tok[1:] else 2.0*A.lev(ph[0],tok[1:])+1
                key=' '.join(ph); c=cnt[tok]; m=sum(c.values())
                pr={0:.04,1:.8,2:.13,3:.03}[len(ph)]/80.
                return -math.log((c[key]+0.5*pr)/(m+0.5))+noise*rnd.random()
            I,J=len(t),len(w);INF=1e18
            D=[dict() for _ in range(I+1)];B=[dict() for _ in range(I+1)];D[0][0]=0
            band=max(40,int(.12*J))
            for i in range(I+1):
                c0=i*J/max(I,1)
                for j in sorted(k for k in D[i] if abs(k-c0)<=band or i==I):
                    d=D[i][j]
                    if j<J and d+SKIP<D[i].get(j+1,INF): D[i][j+1]=d+SKIP;B[i][j+1]=(i,j,None)
                    if i<I:
                        tok=t[i]; mx=12 if tok=='*' else 3
                        for k in range(0,min(mx,J-j)+1):
                            ph=tuple(w[j:j+k]); v=d+cost(i,tok,ph)
                            if v<D[i+1].get(j+k,INF): D[i+1][j+k]=v;B[i+1][j+k]=(i,j,ph)
            i,j=I,J;path={}
            while (i,j)!=(0,0):
                pi,pj,ph=B[i][j]
                if ph is not None and t[pi][0] not in '=*': path[pi]=' '.join(ph)
                i,j=pi,pj
            prev[n]=path
            for i,ph in path.items(): cnt[t[i]][ph]+=1
    # objective: description length of the key
    tot=0
    for tok,c in cnt.items():
        m=sum(c.values())
        for k,v in c.items():
            if v>0: tot-=v*math.log(v/m)
        tot+=3*len([k for k,v in c.items() if v>0])
    return tot,cnt,prev
if __name__=='__main__':
    DATA=list(W.DATA)
    for x in sys.argv[3:]:
        n,cf,pf=x.split(':'); DATA.append((n,A.read_cipher(cf),W.words(pf)))
    best=None
    for s in range(int(sys.argv[2])):
        r=run(DATA,int(sys.argv[1]),s); print('seed',s,round(r[0]),flush=True)
        if best is None or r[0]<best[0]: best=r
    tot,cnt,prev=best
    json.dump({k:{a:b for a,b in v.items() if b>0} for k,v in cnt.items()},open('key_counts.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    for n,t,w in DATA:
        print('\n##',n); print(' | '.join(f'{tok}={prev[n].get(i,"")}' if tok[0] not in '=*' else tok for i,tok in enumerate(t)))
