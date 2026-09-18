import numpy as np, os
A=27  # 0=space,1..26=a..z
def enc(s): return np.array([0 if c==' ' else ord(c)-96 for c in s],dtype=np.int64)
def build(text,n=5,d=0.75,fn=None):
    x=enc(text)
    tabs=[]
    # unigram
    c1=np.bincount(x,minlength=A).astype(np.float64)+0.5
    p=np.log(c1/c1.sum()); tabs.append(p)
    prev=c1/c1.sum()
    for k in range(2,n+1):
        idx=np.zeros(len(x)-k+1,dtype=np.int64)
        for j in range(k): idx=idx*A+x[j:len(x)-k+1+j]
        c=np.bincount(idx,minlength=A**k).astype(np.float64).reshape(-1,A)
        ctx=c.sum(1,keepdims=True)
        nz=(c>0).sum(1,keepdims=True)
        lower=np.tile(prev.reshape(-1,A) if prev.ndim>1 else prev.reshape(1,A),(1,1))
        # lower-order prob for suffix context: drop first char of context
        lowerfull=prev.reshape(A**(k-2) if k>2 else 1,A)
        lowerfull=np.tile(lowerfull,(A,1)) if k>2 else np.tile(lowerfull,(A,1))
        with np.errstate(divide='ignore',invalid='ignore'):
            pk=np.where(ctx>0,(np.maximum(c-d,0)+d*nz*lowerfull)/np.maximum(ctx,1),lowerfull)
        prev=pk
    lp=np.log(prev).astype(np.float32).ravel()
    if fn: np.save(fn,lp)
    return lp
if __name__=='__main__':
    t=open('it19.txt').read()
    build(t,5,fn='lm5sp.npy')
    build(t.replace(' ',''),5,fn='lm5ns.npy')
    print('ok')
