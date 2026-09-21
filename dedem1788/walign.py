# word-level hard-EM monotone aligner: each code group -> 0..3 whole words (or a word split in 2 parts)
import re, math, collections, sys, json, unicodedata
import align as A
sys.stdout.reconfigure(encoding='utf-8')
def words(f, start=None, end=None):
    txt=[]
    for line in open(f, encoding='utf-8'):
        if line.startswith('#') or line.lstrip().startswith('[catchword') or line.lstrip().startswith('[folio') or line.lstrip().startswith('[margin'): continue
        line=re.sub(r'<[^>]*>','',line); line=re.sub(r'\[[^\]]*\]','',line).replace('{','').replace('}','')
        line=line.rstrip()
        txt.append(line[:-1] if line.endswith('-') else line+' ')
    s=''.join(txt)
    w=[A.norm(x) for x in re.split(r"[\s']+", s)]; w=[x for x in w if x]
    if start:
        st=[A.norm(x) for x in start.split()]
        for i in range(len(w)):
            if w[i:i+len(st)]==st: w=w[i:]; break
    if end:
        en=[A.norm(x) for x in end.split()]
        for i in range(len(w)):
            if w[i:i+len(en)]==en: w=w[:i+len(en)]; break
    return w
cnt=collections.defaultdict(collections.Counter)
SKIP=7.0
def cost(tok, ph):
    if tok=='*': return 1.0*len(ph)
    if tok[0]=='=':
        if len(ph)!=1: return 99
        return 0 if ph[0]==tok[1:] else 2.0*A.lev(ph[0],tok[1:])+1
    c=cnt[tok]; n=sum(c.values()); a=0.3
    k=len(ph.split(' ')) if isinstance(ph,str) else len(ph)
    key=' '.join(ph)
    prior={0:.05,1:.8,2:.12,3:.03}[k]*(1/60.)
    return -math.log((c[key]+a*prior)/(n+a))
def align(t,w):
    I,J=len(t),len(w);INF=1e18
    D=[dict() for _ in range(I+1)];B=[dict() for _ in range(I+1)];D[0][0]=0
    band=max(40,int(.12*J))
    for i in range(I+1):
        c=i*J/max(I,1)
        for j in sorted(k for k in D[i] if abs(k-c)<=band or i==I):
            d=D[i][j]
            if j<J and d+SKIP<D[i].get(j+1,INF): D[i][j+1]=d+SKIP;B[i][j+1]=(i,j,None)
            if i<I:
                tok=t[i]; mx=12 if tok=='*' else 3
                for k in range(0,min(mx,J-j)+1):
                    ph=tuple(w[j:j+k]); v=d+cost(tok,ph)
                    if v<D[i+1].get(j+k,INF): D[i+1][j+k]=v;B[i+1][j+k]=(i,j,ph)
    i,j=I,J;path=[]
    if J not in D[I]: return INF,[]
    while (i,j)!=(0,0):
        pi,pj,ph=B[i][j]; path.append((t[pi] if ph is not None else None,' '.join(ph) if ph is not None else w[pj])); i,j=pi,pj
    return D[I][J],path[::-1]
DATA=[('R2121',[x for x in A.read_cipher('tx/R2121_cipher.txt',cut='3107') if x not in ('=hoog','=edele','=gestrenge','=heer')],words('tx/R2121_clear.txt','Bij eene volgende','volmaakt geschikt'))]
if __name__=='__main__':
    for x in sys.argv[2:]:
        n,cf,pf=x.split(':'); DATA.append((n,A.read_cipher(cf),words(pf)))
    for n,t,w in DATA: print(n,len(t),len(w))
    for it in range(int(sys.argv[1])):
        new=collections.defaultdict(collections.Counter);tot=0;paths={}
        for n,t,w in DATA:
            c,p=align(t,w);tot+=c;paths[n]=p
            for tok,ph in p:
                if tok and tok[0] not in '=*': new[tok][ph]+=1
        cnt=new;print('iter',it,round(tot),flush=True)
    json.dump(paths,open('wpaths.json','w',encoding='utf-8'),ensure_ascii=False)
    for n,p in paths.items():
        print('\n##',n); print(' | '.join(f'{t}={s}' if t else f'_{s}' for t,s in p))
