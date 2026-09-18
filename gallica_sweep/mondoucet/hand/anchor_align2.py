# Refined anchored alignment: per-glyph null rate, init from previous key counts, tight band around previous Viterbi path.
import sys, numpy as np, collections, json, re
def load_ct(files):
    toks=[]; lines=[]
    for f in files:
        for l in open(f,encoding='utf-8'):
            if ':' not in l or l.startswith('#'): continue
            lab,rest=l.split(':',1); t=rest.split(); lines.append((lab.strip(),len(toks),len(t))); toks+=t
    return toks,lines
toks,lines=load_ct(['hand/ct_f62.txt','hand/ct_f62v.txt'])
pt=''.join(l.strip() for l in open('pt_f64.txt',encoding='utf-8') if l.strip() and not l.startswith('#')).replace(' ','')
n,m=len(toks),len(pt)
# previous path from align_f62_out.txt: count letters consumed per token
prev=open('hand/align_f62_out.txt',encoding='utf-8').read().split('\n')
path=[0]; i=0
while i<len(prev)-1:
    if re.match(r'^ *\w+: ',prev[i]) and prev[i+1].startswith('     '):
        for d in prev[i+1].split():
            path.append(path[-1]+(0 if d=='_' else (2 if d.startswith('[') else 1)))
        i+=2
    else: i+=1
assert len(path)==n+1, (len(path),n)
BAND=int(sys.argv[1]) if len(sys.argv)>1 else 5
types=sorted(set(toks)); tix={t:i for i,t in enumerate(types)}; letters=sorted(set(pt)); lix={c:i for i,c in enumerate(letters)}
K,Lc=len(types),len(letters); Tn=np.array([tix[t] for t in toks]); Pn=np.array([lix[c] for c in pt])
kc=json.load(open('hand/key_counts.json'))
E=np.full((K,Lc),0.3)
for t,c in kc.items():
    for ch,v in c.items():
        if ch in lix: E[tix[t],lix[ch]]+=v
E/=E.sum(1,keepdims=True)
pnull=np.full(K,0.05); ps=0.03
mask=np.zeros((n+1,m+1),bool)
for i in range(n+1):
    lo,hi=max(0,path[i]-BAND),min(m,path[i]+BAND); mask[i,lo:hi+1]=True
mask[0,:]=False; mask[0,0]=True; mask[n,:]=False; mask[n,m]=True
for it in range(40):
    pm=1-pnull-ps
    al=np.zeros((n+1,m+1)); al[0,0]=1
    for i in range(1,n+1):
        t=Tn[i-1]; em=E[t][Pn]; a=np.zeros(m+1)
        a[1:]+=al[i-1,:-1]*pm[t]*em; a[2:]+=al[i-1,:-2]*ps*em[1:]; a+=al[i-1]*pnull[t]
        a*=mask[i]; al[i]=a/(a.sum()+1e-300)
    be=np.zeros((n+1,m+1)); be[n,m]=1
    for i in range(n-1,-1,-1):
        t=Tn[i]; em=E[t][Pn]; b=np.zeros(m+1)
        b[:-1]+=be[i+1,1:]*pm[t]*em; b[:-2]+=be[i+1,2:]*ps*em[1:]; b+=be[i+1]*pnull[t]
        b*=mask[i]; be[i]=b/(b.sum()+1e-300)
    C=np.zeros((K,Lc)); nullc=np.zeros(K); tot=np.zeros(K)
    for i in range(1,n+1):
        t=Tn[i-1]; em=E[t][Pn]
        pmatch=al[i-1,:-1]*pm[t]*em*be[i,1:]; pskip=al[i-1,:-2]*ps*em[1:]*be[i,2:]; pn=al[i-1]*pnull[t]*be[i]
        z=pmatch.sum()+pskip.sum()+pn.sum()+1e-300
        np.add.at(C[t],Pn,pmatch/z); np.add.at(C[t],Pn[1:],pskip/z); nullc[t]+=pn.sum()/z; tot[t]+=1
    E=(C+0.02)/(C+0.02).sum(1,keepdims=True)
    pnull=np.clip((nullc+0.5)/(tot+1.0),0.01,0.9)
# Viterbi
V=np.full((n+1,m+1),-1e18); V[0,0]=0; bp=np.zeros((n+1,m+1),np.int8)
lE=np.log(E); pm=1-pnull-ps
for i in range(1,n+1):
    t=Tn[i-1]; em=lE[t][Pn]
    c1=np.full(m+1,-1e18); c1[1:]=V[i-1,:-1]+np.log(pm[t])+em
    c2=np.full(m+1,-1e18); c2[2:]=V[i-1,:-2]+np.log(ps)+em[1:]
    c3=V[i-1]+np.log(pnull[t])
    st=np.stack([c1,c2,c3]); bp[i]=st.argmax(0); V[i]=st.max(0); V[i][~mask[i]]=-1e18
i,j=n,m; out=[]
while i>0:
    k=bp[i,j]
    if k==0: out.append(pt[j-1]); j-=1
    elif k==1: out.append('['+pt[j-2]+']'+pt[j-1]); j-=2
    else: out.append('_')
    i-=1
out=out[::-1]
for lab,s,c in lines:
    print('%3s: %s'%(lab,' '.join(toks[s:s+c]))); print('     %s'%(' '.join(out[s:s+c])))
key=collections.defaultdict(collections.Counter); nulls=collections.Counter()
for i,d in enumerate(out):
    if d=='_': nulls[toks[i]]+=1
    else: key[toks[i]][d[-1]]+=1
print('\nKEY')
for t in sorted(types,key=lambda t:-(sum(key[t].values())+nulls[t])):
    print('%4s tot %3d null %2d  %s'%(t,sum(key[t].values())+nulls[t],nulls[t],' '.join('%s%d'%kv for kv in key[t].most_common(6))))
json.dump({'key':{t:dict(key[t]) for t in key},'nulls':dict(nulls)},open('hand/key2.json','w'))
