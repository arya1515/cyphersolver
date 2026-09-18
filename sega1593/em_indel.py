# EM decipherment robust to segmentation noise: each token is either emitted by the current letter (prob 1-pi-pd),
# an insertion (junk, no letter advance, prob pi), or emitted after skipping one unobserved letter (deletion, prob pd).
# usage: em_indel.py clusters.json page_key|- "junk" iters restarts seed [maxlines]   env PI PD
import sys, json, math, numpy as np, os, time
sys.path.insert(0,'sega1593'); sys.path.insert(0,'sp53')
from em_poly import build_trigram, ALPHA, K
PI=float(os.environ.get('PI','0.08')); PD=float(os.environ.get('PD','0.08'))
def lse(a,axis):
    m=a.max(axis=axis,keepdims=True); return (m+np.log(np.exp(a-m).sum(axis=axis,keepdims=True))).squeeze(axis)
def fb(tokens, logE, logT, logT2):
    n=len(tokens); ncl=logE.shape[0]
    ljunk=-math.log(ncl)
    lnorm=math.log(1-PI-PD); lpi=math.log(PI); lpd=math.log(PD)
    alpha=np.full((n,K,K),-np.inf)
    alpha[0]=-2*math.log(K)+logE[tokens[0]][None,:]
    for t in range(1,n):
        e=logE[tokens[t]]
        a=alpha[t-1]
        m1=lse(a[:,:,None]+logT,0)+e[None,:]+lnorm          # normal advance: (a,b)->(b,c)
        m2=lse(a[:,:,None]+logT2,0)+e[None,:]+lpd           # skip one letter: (a,b)->(b,d) via unobserved c
        m3=a+ljunk+lpi                                       # insertion: state unchanged
        alpha[t]=np.logaddexp(np.logaddexp(m1,m2),m3)
    beta=np.zeros((n,K,K))
    for t in range(n-2,-1,-1):
        e=logE[tokens[t+1]]; b=beta[t+1]
        x1=lse(logT+(b+e[None,:])[None,:,:],2)+lnorm        # over c: (a,b)->(b,c)
        x2=lse(logT2+(b+e[None,:])[None,:,:],2)+lpd
        x3=b+ljunk+lpi
        beta[t]=np.logaddexp(np.logaddexp(x1,x2),x3)
    ll=lse(alpha[n-1].ravel(),0)
    # posterior that token t was emitted by letter c in state (b,c) (normal or skip), vs insertion
    post_letter=np.zeros((n,K)); post_ins=np.zeros(n)
    post_letter[0]=np.exp(lse(alpha[0]+beta[0],0)-ll)
    for t in range(1,n):
        e=logE[tokens[t]]; a=alpha[t-1]; b=beta[t]
        m1=lse(a[:,:,None]+logT,0)+e[None,:]+lnorm+b
        m2=lse(a[:,:,None]+logT2,0)+e[None,:]+lpd+b
        m3=a+ljunk+lpi+b
        pl=np.exp(np.logaddexp(m1,m2)-ll).sum(0)   # over b -> letter c
        post_letter[t]=pl; post_ins[t]=np.exp(m3-ll).sum()
    return post_letter, post_ins, ll
def em(tokens, ncl, iters, rnd, verbose=False):
    logT,logB,logU=build_trigram()
    T=np.exp(logT); T2=np.einsum('abc,bcd->abd',T,T); logT2=np.log(T2+1e-30)
    E=rnd.random((ncl,K))+0.5; E/=E.sum(0,keepdims=True)
    for it in range(iters):
        pl,pi_,ll=fb(tokens,np.log(E+1e-12),logT,logT2)
        counts=np.zeros((ncl,K)); np.add.at(counts,tokens,pl)
        E=(counts+0.01)/(counts.sum(0,keepdims=True)+0.01*ncl)
        if verbose and it%10==0: print(f'  it {it} ll {ll:.1f} ins {pi_.mean():.3f}',flush=True)
    return E,ll
if __name__=='__main__':
    cl=json.load(open(sys.argv[1]))
    if sys.argv[2]!='-': cl=cl[sys.argv[2]]
    junk=set(int(x) for x in sys.argv[3].split(',') if x)
    iters=int(sys.argv[4]); restarts=int(sys.argv[5]); seed=int(sys.argv[6]); maxl=int(sys.argv[7]) if len(sys.argv)>7 else 10**6
    toks=[]
    for k in sorted(cl,key=int)[:maxl]: toks+=[c for c in cl[k] if c not in junk]
    ids=sorted(set(toks)); rid={c:i for i,c in enumerate(ids)}
    tokens=np.array([rid[c] for c in toks]); ncl=len(ids)
    rnd=np.random.default_rng(seed); best=None
    for r in range(restarts):
        t0=time.time(); E,ll=em(tokens,ncl,iters,rnd,verbose=(r==0))
        print(f'restart {r} ll {ll:.1f} {time.time()-t0:.0f}s',flush=True)
        if best is None or ll>best[0]: best=(ll,E)
    ll,E=best
    PAIRS=['an','bo','cp','dq','er','fs','gt','hu','ix','ly','mz']
    logT,logB,logU=build_trigram(); pl0=np.exp(logU); out={}
    for i,c in enumerate(ids):
        p=E[i]*pl0; p/=p.sum(); top=np.argsort(-p)[:3]
        ps={pr:p[ALPHA.index(pr[0])]+p[ALPHA.index(pr[1])] for pr in PAIRS}; bp=max(ps,key=ps.get); out[c]=bp
        print(c,'n=%d'%(tokens==i).sum(),' '.join(f'{ALPHA[j]}:{p[j]:.2f}' for j in top),'pair',bp,round(ps[bp],2))
    print('MAP',out)
    np.save(sys.argv[1].replace('.json','')+'_E.npy',E); json.dump(ids,open(sys.argv[1].replace('.json','')+'_ids.json','w'))
    T=np.exp(logT); logT2=np.log(np.einsum('abc,bcd->abd',T,T)+1e-30)
    pl,pi_,ll=fb(tokens,np.log(E+1e-12),logT,logT2)
    dec=''.join(('.' if pi_[t]>0.5 else ALPHA[pl[t].argmax()]) for t in range(len(tokens)))
    pos=0
    for k in sorted(cl,key=int)[:maxl]:
        n=len([c for c in cl[k] if c not in junk]); print('L%s'%k, dec[pos:pos+n]); pos+=n
