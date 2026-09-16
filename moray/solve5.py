# nomenclator hypothesis: symbols in BREAK are word-codes; 5-gram windows spanning them are not scored.
import numpy as np,math,sys,json,collections,random,re
import ng5
from solve3 import load_ct,AL
tab=ng5.load()
def windows(ctidx,brk):
    n=len(ctidx); isb=np.array([i in brk for i in ctidx])
    ok=[i for i in range(n-4) if not isb[i:i+5].any()]
    return np.array(ok)
def score(tab,p,W):
    q=p[W]*456976+p[W+1]*17576+p[W+2]*676+p[W+3]*26+p[W+4]
    return float(tab[q].sum())
def anneal(ctidx,nsym,W,free,iters=200000,T0=8.0,Tend=0.2,seed=0):
    rnd=np.random.default_rng(seed); key=rnd.integers(0,26,nsym)
    cur=score(tab,key[ctidx],W); best=cur; bestkey=key.copy(); lam=math.log(Tend/T0)/iters
    for it in range(iters):
        T=T0*math.exp(lam*it); k2=key.copy()
        if rnd.random()<0.75: k2[free[rnd.integers(len(free))]]=rnd.integers(26)
        else:
            a,b=rnd.choice(free,2,replace=False); k2[a],k2[b]=k2[b],k2[a]
        sc=score(tab,k2[ctidx],W)
        if sc>cur or rnd.random()<math.exp((sc-cur)/T):
            key,cur=k2,sc
            if cur>best: best,bestkey=cur,key.copy()
    return best,bestkey
def run(ct,breaks,restarts=12):
    syms=sorted(set(ct)); si={s:i for i,s in enumerate(syms)}; ctidx=np.array([si[s] for s in ct])
    brk={si[s] for s in breaks}; W=windows(ctidx,brk); free=[i for i in range(len(syms)) if i not in brk]
    best=max((anneal(ctidx,len(syms),W,free,seed=r) for r in range(restarts)),key=lambda t:t[0])
    dec=''.join('#' if i in brk else AL[best[1][i]] for i in ctidx)
    return best[0],len(W),dec,{s:AL[best[1][si[s]]] for s in syms if si[s] not in brk}
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='target':
        ct=load_ct('elizabeth_moray.txt'); c=collections.Counter(ct)
        for thr in (1,2,3):
            breaks=[s for s,n in c.items() if n<=thr]
            sc,nw,dec,key=run(ct,breaks)
            print(f'thr<={thr} breaks={len(breaks)} windows={nw} score/window={sc/nw:.3f}\n  {dec}\n  {json.dumps(key,sort_keys=True)}',flush=True)
    elif mode=='custom':
        ct=load_ct('elizabeth_moray.txt')
        for name,breaks in [('numbers as word-codes',[s for s in set(ct) if s[0].isdigit() or s=='Eb']),
                            ('letters as word-codes',[s for s in set(ct) if not (s[0].isdigit() or s=='Eb')]),
                            ('x,z families as word-codes',[s for s in set(ct) if s[0] in 'xz'])]:
            sc,nw,dec,key=run(ct,breaks)
            print(f'{name}: breaks={len(breaks)} windows={nw} score/window={sc/nw:.3f}
  {dec}
  {json.dumps(key,sort_keys=True)}',flush=True)
    else:
        # control: Scots text, same symbol profile, plus the same number of break positions replaced by word-codes
        from lm import clean
        ho=open('corpus/historielifeofki00colvuoft.txt',encoding='utf-8',errors='ignore').read()
        txt=re.sub(r' +','',clean(ho)); rnd=random.Random(int(sys.argv[2])); N=134
        for trial in range(int(sys.argv[3])):
            i=rnd.randrange(200000,len(txt)-N); p=txt[i:i+N]
            freq=collections.Counter(p); syms={}; sid=0
            for L in sorted(freq): syms[L]=[f's{sid}']; sid+=1
            top=[L for L,_ in freq.most_common(8)]
            while sid<24: L=rnd.choice(top); syms[L].append(f's{sid}'); sid+=1
            ct=[syms[c][0] if len(syms[c])==1 or rnd.random()<0.6 else rnd.choice(syms[c][1:]) for c in p]
            # 16 rare symbols as word-codes at 26 positions
            pos=rnd.sample(range(N),26); codes=[f'W{k}' for k in range(16)]
            for j,ps in enumerate(pos): ct[ps]=codes[j%16]
            sc,nw,dec,key=run(ct,codes)
            truth=''.join('#' if j in pos else p[j] for j in range(N))
            acc=sum(a==b for a,b in zip(dec,truth) if b!='#')/(N-26)
            print(f'control {trial} windows={nw} score/window={sc/nw:.3f} acc={acc:.2f}\n  T {truth}\n  D {dec}',flush=True)
