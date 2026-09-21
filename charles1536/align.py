# EM alignment of clean token lines vs margin plaintext, emission = substring, prior favours 1-4 letters
import re,math,collections,sys,glob,json
sys.stdout.reconfigure(encoding='utf-8')
def read_tx(f):
    toks=[];plain=[]
    for line in open(f,encoding='utf-8'):
        if line.startswith('C:'):
            toks+= [t for t in line[2:].split() if t]
        elif line.startswith('M:'):
            plain.append(line[2:])
    return toks,plain
def ctok(t): return t.rstrip('?')
def cplain(lines):
    s=' '.join(lines).lower()
    s=s.replace('[?]','#').replace('ç','z').replace('ñ','n').replace('ñ','n')
    for a,b in zip('áéíóúàèìòùâêîôû','aeiouaeiouaeiou'): s=s.replace(a,b)
    s=re.sub(r'\bv\.?\s?s\.?\b','$',s)   # VS as one symbol
    s=re.sub(r'[^a-z#$]','',s)
    return s
KNOWN=json.load(open('known.json',encoding='utf-8')) if glob.glob('known.json') else {}
data=[]
for f in sorted(glob.glob('tx/S*.txt')):
    t,p=read_tx(f); t=[ctok(x) for x in t]; s=cplain(p)
    if len(t)>10: data.append((f[3:-4],t,s))
MAXL=9
LP={0:.005,1:.45,2:.35,3:.15,4:.04,5:.004,6:.001,7:.0005,8:.0003,9:.0002}
cnt=collections.defaultdict(collections.Counter)
SKIP=7.0
def cost(tok,sub):
    if tok in KNOWN:
        return 0.0 if sub in KNOWN[tok] else 30.0
    c=cnt[tok];n=sum(c.values());a=1.0
    p=(c[sub]+a*LP[len(sub)]*(1/20)**len(sub))/(n+a)
    return -math.log(p)
def align(t,s):
    I,J=len(t),len(s);INF=1e18
    D=[[INF]*(J+1) for _ in range(I+1)];B=[[None]*(J+1) for _ in range(I+1)]
    D[0][0]=0
    band=max(60,int(0.25*J))
    for i in range(I+1):
        Di=D[i];c=i*J/max(I,1)
        lo=max(0,int(c-band));hi=min(J,int(c+band))
        for j in range(lo,hi+1):
            d=Di[j]
            if d>=INF: continue
            if j<J and d+SKIP<Di[j+1]: Di[j+1]=d+SKIP;B[i][j+1]=(i,j,None)
            if i<I:
                tok=t[i];Dn=D[i+1]
                for L in range(0,min(MAXL,J-j)+1):
                    sub=s[j:j+L]
                    if '#' in sub and sub!='#': break
                    v=d+cost(tok,sub)
                    if v<Dn[j+L]: Dn[j+L]=v;B[i+1][j+L]=(i,j,sub)
    if D[I][J]>=INF: return INF,[]
    i,j=I,J;path=[]
    while (i,j)!=(0,0):
        pi,pj,sub=B[i][j]
        path.append((t[pi] if sub is not None else None,sub if sub is not None else s[pj]))
        i,j=pi,pj
    return D[I][J],path[::-1]
if __name__=='__main__':
    for it in range(int(sys.argv[1]) if len(sys.argv)>1 else 10):
        new=collections.defaultdict(collections.Counter);tot=0;paths={}
        for r,t,s in data:
            c,p=align(t,s);tot+=c;paths[r]=p
            for tok,sub in p:
                if tok is not None: new[tok][sub]+=1
        cnt=new;print('iter',it,round(tot),flush=True)
    json.dump(paths,open('paths.json','w',encoding='utf-8'))
    freq=collections.Counter()
    for r,t,s in data: freq.update(t)
    for tok,n in freq.most_common(200):
        print(tok,n,cnt[tok].most_common(5))
