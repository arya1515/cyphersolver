# EM decipherment (noisy channel): letters ~ trigram LM (24-letter alphabet), clusters emitted from letters.
# usage: em_poly.py clusters.json page_key|- "junk" iters restarts seed [maxlines]
import sys, json, pickle, math, numpy as np, os, time
sys.path.insert(0,'sp53'); sys.path.insert(0,'sega1593')
from homo import ALPHA
K=len(ALPHA)
def build_trigram():
    N,cnts,total=pickle.load(open('sp53/fr6.pkl','rb'))
    idx={ch:i for i,ch in enumerate(ALPHA)}
    uni=np.ones(K)
    for ch,c in cnts[1].items():
        if ch in idx: uni[idx[ch]]+=c
    uni/=uni.sum()
    bi=np.zeros((K,K))
    for s,c in cnts[2].items():
        if s[0] in idx and s[1] in idx: bi[idx[s[0]],idx[s[1]]]+=c
    bip=(bi+0.5*uni[None,:]*K)/(bi.sum(1,keepdims=True)+0.5*K)
    tri=np.zeros((K,K,K))
    for s,c in cnts[3].items():
        if all(ch in idx for ch in s): tri[idx[s[0]],idx[s[1]],idx[s[2]]]+=c
    trip=(tri+1.0*bip[None,:,:]*K*0.2)/(tri.sum(2,keepdims=True)+1.0*K*0.2)
    return np.log(trip), np.log(bip), np.log(uni)
def forward_backward(tokens, logE, logT):
    # states = (prev letter, cur letter) pairs; logE[c,l] = log P(cluster c | letter l)
    n=len(tokens); S=K*K
    # transition from state (a,b) to (b,c): logT[a,b,c]
    alpha=np.full((n,K,K),-np.inf); beta=np.full((n,K,K),-np.inf)
    # position 0,1 init: uniform over first letter, bigram for second
    e0=logE[tokens[0]]; e1=logE[tokens[1]]
    alpha[1]=(np.log(1.0/K)+e0)[:,None]+logT[K//2][:, :]*0  # placeholder
    alpha[1]=(np.log(1.0/K)+e0)[:,None]+e1[None,:]-math.log(K)
    for t in range(2,n):
        e=logE[tokens[t]]
        # alpha[t][b,c] = logsumexp_a alpha[t-1][a,b] + logT[a,b,c] + e[c]
        m=alpha[t-1][:,:,None]+logT  # a,b,c
        mx=m.max(0); alpha[t]=mx+np.log(np.exp(m-mx[None]).sum(0))+e[None,:]
    beta[n-1]=0.0
    for t in range(n-2,0,-1):
        e=logE[tokens[t+1]]
        m=logT+(beta[t+1]+e[None,:])[None,:,:]  # a,b,c
        mx=m.max(2); beta[t]=mx+np.log(np.exp(m-mx[:,:,None]).sum(2))
    post=alpha+beta  # over (prev,cur) at t
    ll=post[n-1].max()+np.log(np.exp(post[n-1]-post[n-1].max()).sum())
    gamma=np.exp(post-ll)  # posterior of state
    letter_post=gamma.sum(1)  # posterior of cur letter at t: sum over prev
    letter_post[0]=np.exp(alpha[1]+beta[1]-ll).sum(1)
    return letter_post, ll
def em(tokens, ncl, iters, rnd, verbose=False):
    logT,logB,logU=build_trigram()
    E=rnd.random((ncl,K))+0.5; E/=E.sum(0,keepdims=True)  # P(c|l) columns sum to 1
    for it in range(iters):
        logE=np.log(E+1e-12)
        lp,ll=forward_backward(tokens,logE,logT)
        counts=np.zeros((ncl,K))
        np.add.at(counts,tokens,lp)
        E=(counts+0.01)/(counts.sum(0,keepdims=True)+0.01*ncl)
        if verbose and it%10==0: print(f'  it {it} ll {ll:.1f}',flush=True)
    return E,ll
if __name__=='__main__':
    cl=json.load(open(sys.argv[1]))
    if sys.argv[2]!='-': cl=cl[sys.argv[2]]
    junk=set(int(x) for x in sys.argv[3].split(',') if x)
    iters=int(sys.argv[4]); restarts=int(sys.argv[5]); seed=int(sys.argv[6]); maxl=int(sys.argv[7]) if len(sys.argv)>7 else 10**6
    toks=[]
    for k in sorted(cl,key=int)[:maxl]: toks+=[c for c in cl[k] if c not in junk]
    # remap cluster ids to dense
    ids=sorted(set(toks)); rid={c:i for i,c in enumerate(ids)}
    tokens=np.array([rid[c] for c in toks]); ncl=len(ids)
    rnd=np.random.default_rng(seed)
    best=None
    for r in range(restarts):
        t0=time.time(); E,ll=em(tokens,ncl,iters,rnd,verbose=(r==0))
        print(f'restart {r} ll {ll:.1f} {time.time()-t0:.0f}s',flush=True)
        if best is None or ll>best[0]: best=(ll,E)
    ll,E=best
    # report: for each cluster, top letters by P(l|c) ~ E[c,l]*P(l)
    PAIRS=['an','bo','cp','dq','er','fs','gt','hu','ix','ly','mz']
    logT,logB,logU=build_trigram(); pl=np.exp(logU)
    out={}
    for i,c in enumerate(ids):
        p=E[i]*pl; p/=p.sum(); top=np.argsort(-p)[:3]
        letters=''.join(ALPHA[j] for j in top)
        # best pair
        ps={pr:p[ALPHA.index(pr[0])]+p[ALPHA.index(pr[1])] for pr in PAIRS}
        bp=max(ps,key=ps.get)
        out[c]=bp
        print(c, 'n=%d'%(tokens==i).sum(), letters, ' '.join(f'{ALPHA[j]}:{p[j]:.2f}' for j in top), 'pair',bp,round(ps[bp],2))
    print('MAP',out)
    # posterior decoding per line
    logT,logB,logU=build_trigram()
    lp,ll=forward_backward(tokens,np.log(E+1e-12),logT)
    dec=''.join(ALPHA[j] for j in lp.argmax(1))
    pos=0
    for k in sorted(cl,key=int)[:maxl]:
        n=len([c for c in cl[k] if c not in junk]); print('L%s'%k, dec[pos:pos+n]); pos+=n
