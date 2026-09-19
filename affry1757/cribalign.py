# local hard-EM alignment of crib plaintext against a code letter; seeds from key file are hard
import re,math,collections,sys,json,unicodedata
from view import load
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z]','',s)
LP={1:.25,2:.3,3:.2,4:.1,5:.05,6:.03,7:.02,8:.015,9:.01,10:.008,11:.006,12:.004}
MAXL=12
SKIPC=12.0   # cipher group not in crib (inside)
SKIPP=6.0    # crib letter dropped
SEEDMISS=1e9
ALPHA=0.05
def run(tasks,seed,iters=8,verbose=True,glob=False):
    cnt=collections.defaultdict(collections.Counter)
    def cost(tok,sub):
        if len(sub)>12: return 1e9
        if tok in seed:
            return 0.0 if sub in seed[tok] else SEEDMISS
        if len(sub)>7: return 1e9
        c=cnt[tok];n=sum(c.values());a=ALPHA
        p=(c[sub]+a*LP[len(sub)]*(1/18)**len(sub))/(n+a)
        return -math.log(p)+0.8*len(sub)
    res={}
    for it in range(iters):
        new=collections.defaultdict(collections.Counter);tot=0
        for name,t,s in tasks:
            I,J=len(t),len(s);INF=1e18
            D=[[INF]*(J+1) for _ in range(I+1)];B=[[None]*(J+1) for _ in range(I+1)]
            D[0][0]=0
            if not glob:
                for i in range(I+1): D[i][0]=0
            for i in range(I+1):
                Di=D[i]
                for j in range(J+1):
                    d=Di[j]
                    if d>=INF: continue
                    if j<J and d+SKIPP<Di[j+1]: Di[j+1]=d+SKIPP;B[i][j+1]=(i,j,'P')
                    if i<I:
                        Dn=D[i+1]
                        if (glob or (j>0 and j<J)) and d+SKIPC<Dn[j]: Dn[j]=d+SKIPC;B[i+1][j]=(i,j,'C')
                        tok=t[i]
                        for L in range(1,min(MAXL,J-j)+1):
                            v=d+cost(tok,s[j:j+L])
                            if v<Dn[j+L]: Dn[j+L]=v;B[i+1][j+L]=(i,j,s[j:j+L])
            bi=I if glob else min(range(I+1),key=lambda i:D[i][J]);tot+=D[bi][J]
            i,j=bi,J;path=[]
            while j>0 or i>0:
                pi,pj,sub=B[i][j]
                path.append((pi,t[pi] if sub not in('P',) else None,sub)); i,j=pi,pj
            path=path[::-1]; res[name]=path
            for pi,tok,sub in path:
                if tok is not None and sub not in ('P','C'): new[tok][sub]+=1
        cnt=new
        if verbose: print('iter',it,round(tot),flush=True)
    return res,cnt
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1],encoding='utf8'))
    SEEDMISS=cfg.get("seedmiss",1e9)
    ALPHA=cfg.get("alpha",0.05)
    L=load(cfg['code']);seed={int(k):set([norm(x) for x in (v if isinstance(v,list) else [v])]) for k,v in json.load(open(f"key_{cfg['code']}.json",encoding='utf8')).items()}
    tasks=[]
    for ci,c in enumerate(cfg["cribs"]):
        t=L[c['rec']][c.get('a',0):c.get('b')]
        tasks.append((c["rec"]+"#"+str(ci),t,norm(c["text"] if 'text' in c else open(c['file'],encoding='utf8').read())))
    res,cnt=run(tasks,seed,cfg.get('iters',8),glob=cfg.get('glob',False))
    json.dump({n:[(i,t,s) for i,t,s in p] for n,p in res.items()},open(sys.argv[1].replace('.json','_paths.json'),'w'))
    json.dump({str(k):v.most_common(3) for k,v in cnt.items()},open(sys.argv[1].replace('.json','_counts.json'),'w'))
    for name,path in res.items():
        print('==',name, 'start', path[0][0] if path else None)
        print(' '.join(f"{tok}={sub}" if sub not in('P','C') else (f"[{sub}]" if tok is None else f"{tok}=_") for _,tok,sub in path))
