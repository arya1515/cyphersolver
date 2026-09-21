import re,json,sys
sys.stdout.reconfigure(encoding='utf-8')
exec(open('try.py',encoding='utf8').read().split('for f in')[0])
V=set(K)
def seg(s):
    n=len(s);D=[(0,None)]+[(1e9,None)]*n
    for i in range(n):
        if D[i][0]>=1e9: continue
        for L in range(1,6):
            w=s[i:i+L]
            if len(w)<L: break
            c=D[i][0]+((1 if L>1 else 2.5) if w in V else 6*L)
            if c<D[i+L][0]: D[i+L]=(c,w)
    out=[];j=n
    while j>0: w=D[j][1];out.append(w);j-=len(w)
    return out[::-1]
import glob
for r in sys.argv[1:]:
    f=glob.glob(f'img/DOC_R{r}_*.txt')[0];C=[];M=[]
    mode='c'
    for line in open(f,encoding='utf8',errors='replace'):
        if line.startswith('#') and 'margin' in line.lower(): mode='m';continue
        if line.startswith('#IMAGE'): mode='c'
        if line.startswith('#'): continue
        if mode=='m': M.append(re.sub(r'<[^>]*>','',line).strip());continue
        for chunk in [re.sub(r'\s','',re.sub(r'<[^>]*>','',line))]:
            C+=seg(chunk.replace('?','').replace('Water','').replace('_',''))
    kn=sum(t in K for t in C)
    print(f'== R{r} {len(C)} groups, key reads {kn/max(len(C),1):.0%}, margin lines {len([m for m in M if m])}')
    print(''.join(K.get(t,'['+t+']') for t in C)[:400])
