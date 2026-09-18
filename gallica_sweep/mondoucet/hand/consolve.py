# Constrained homophonic anneal: glyphs with a fixed letter stay fixed; the rest are annealed against the French 5-gram table.
import sys, random, collections, numpy as np
sys.path.insert(0,'../../sp53')
from numba import njit
from fasthomo import full_score, local_score
from homo import ALPHA
K=len(ALPHA)
FIXED={'d':'e','n':'e','c':'e','m':'d','O':'s','h':'a','g':'a','k':'n','e':'n','v':'t','V':'t','@':'r','F':'l','f':'c','i':'c','t':'c','G':'m','10':'i','#':'p','N':'u','23':'u','8':'u','N3':'u','L':'o','o':'o','w':'s','9':'r','q':'r','S':'u','A':'s'}
NULL={'*','C','mq','j'}
@njit(cache=True)
def anneal(toks,nsym,tab,init_map,free,iters,T0,T1,seed,sym_pos,sym_start,sym_count):
    np.random.seed(seed); n=toks.shape[0]; mp=init_map.copy()
    text=np.empty(n,dtype=np.int64)
    for i in range(n): text[i]=mp[toks[i]]
    cur=full_score(text,tab); best=cur; bestmap=mp.copy(); buf=np.empty(n,dtype=np.int64); nf=free.shape[0]
    for it in range(iters):
        T=T0*(T1/T0)**(it/iters); s=free[np.random.randint(nf)]
        u=np.random.randint(K)
        if u==mp[s]: continue
        c=sym_count[s]; st=sym_start[s]
        for k in range(c): buf[k]=sym_pos[st+k]
        before=local_score(text,tab,buf,c); old=mp[s]
        for k in range(c): text[buf[k]]=u
        after=local_score(text,tab,buf,c); d=after-before
        if d>=0 or np.random.random()<np.exp(d/T): mp[s]=u; cur+=d
        else:
            for k in range(c): text[buf[k]]=old
        if cur>best:
            best=cur
            for j in range(nsym): bestmap[j]=mp[j]
    return best,bestmap
def load(files):
    toks=[];lines=[]
    for f in files:
        for l in open(f,encoding='utf-8'):
            if ':' not in l or l.startswith('#'): continue
            lab,rest=l.split(':',1); t=[x for x in rest.split() if x not in NULL]; lines.append((lab.strip(),len(toks),len(t))); toks+=t
    return toks,lines
if __name__=='__main__':
    files=sys.argv[1].split(','); iters=int(sys.argv[2]); restarts=int(sys.argv[3]); seed=int(sys.argv[4])
    toks,lines=load(files)
    tab=np.load('../../sp53/fr5.npy')
    syms=sorted(set(toks),key=lambda s:-toks.count(s)); sid={s:i for i,s in enumerate(syms)}
    arr=np.array([sid[t] for t in toks],dtype=np.int64)
    pos=collections.defaultdict(list)
    for i,t in enumerate(arr): pos[t].append(i)
    sym_pos=[];sym_start=np.zeros(len(syms),dtype=np.int64);sym_count=np.zeros(len(syms),dtype=np.int64)
    for i in range(len(syms)):
        sym_start[i]=len(sym_pos);sym_count[i]=len(pos[i]);sym_pos+=pos[i]
    sym_pos=np.array(sym_pos,dtype=np.int64)
    free=np.array([i for i,s in enumerate(syms) if s not in FIXED],dtype=np.int64)
    print('tokens',len(toks),'symbols',len(syms),'free',len(free),[syms[i] for i in free])
    rnd=random.Random(seed); best=-1e18
    for r in range(restarts):
        m0=np.array([ALPHA.index(FIXED[s]) if s in FIXED else rnd.randrange(K) for s in syms],dtype=np.int64)
        sc,m=anneal(arr,len(syms),tab,m0,free,iters,2.0,0.02,seed*1000+r,sym_pos,sym_start,sym_count)
        print('restart',r,round(sc,1),round(sc/len(toks),3),flush=True)
        if sc>best: best=sc;bestmap=m.copy()
    mp={syms[i]:ALPHA[bestmap[i]] for i in range(len(syms))}
    print('MAP free:',{s:mp[s] for s in syms if s not in FIXED})
    for lab,s,c in lines: print(lab+':',''.join(mp[t] for t in toks[s:s+c]))
