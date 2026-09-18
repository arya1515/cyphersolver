# Anchored soft-EM alignment, glyph tokens vs plaintext letters, ~1:1 with nulls and letter-skips.
import sys, numpy as np, collections, re
def load_ct(files):
    toks=[]; lines=[]
    for f in files:
        for l in open(f,encoding='utf-8'):
            if ':' not in l: continue
            lab,rest=l.split(':',1); t=rest.split(); lines.append((lab.strip(),len(toks),len(t))); toks+=t
    return toks,lines
toks,lines=load_ct(['hand/ct_f62.txt','hand/ct_f62v.txt'])
pt=''.join(l.strip() for l in open('pt_f64.txt',encoding='utf-8') if l.strip() and not l.startswith('#')).replace(' ','')
n,m=len(toks),len(pt); print('glyphs',n,'letters',m)
L={lab:(s,c) for lab,s,c in lines}
def gi(lab,k): return L[lab][0]+k
# anchors: (glyph index, letter index)
anch=[(gi('18',0),0),(gi('22',0),pt.find('leurdelivrance')),(gi('23',0),pt.find('labruslation')),
      (gi('27',27),pt.find('nousmaintenant')),(gi('28',23),pt.find('euaucunes')),(n,m)]
print('anchors',anch)
f=np.interp(np.arange(n+1),[a for a,b in anch],[b for a,b in anch])
BAND=float(sys.argv[1]) if len(sys.argv)>1 else 12
types=sorted(set(toks)); tix={t:i for i,t in enumerate(types)}; letters=sorted(set(pt)); lix={c:i for i,c in enumerate(letters)}
K,Lc=len(types),len(letters); Tn=np.array([tix[t] for t in toks]); Pn=np.array([lix[c] for c in pt])
E=np.full((K,Lc),1.0/Lc); pn,ps=0.05,0.05; pm=1-pn-ps
mask=np.zeros((n+1,m+1),bool)
for i in range(n+1):
    lo,hi=int(max(0,f[i]-BAND)),int(min(m,f[i]+BAND)); mask[i,lo:hi+1]=True
mask[0,:]=False; mask[0,0]=True
for it in range(30):
    al=np.zeros((n+1,m+1)); al[0,0]=1; sc=np.ones(n+1)
    for i in range(1,n+1):
        em=E[Tn[i-1]][Pn]  # em[j-1] for letter j-1
        a=np.zeros(m+1)
        a[1:]+=al[i-1,:-1]*pm*em
        a[2:]+=al[i-1,:-2]*ps*em[1:]
        a+=al[i-1]*pn
        a*=mask[i]; sc[i]=a.sum()+1e-300; al[i]=a/sc[i]
    be=np.zeros((n+1,m+1)); be[n,m]=1
    for i in range(n-1,-1,-1):
        em=E[Tn[i]][Pn]; b=np.zeros(m+1)
        b[:-1]+=be[i+1,1:]*pm*em
        b[:-2]+=be[i+1,2:]*ps*em[1:]
        b+=be[i+1]*pn
        b*=mask[i]; be[i]=b/(b.sum()+1e-300)
    C=np.zeros((K,Lc)); nulls=0; skips=0
    for i in range(1,n+1):
        em=E[Tn[i-1]][Pn]
        pmatch=al[i-1,:-1]*pm*em*be[i,1:]
        pskip=al[i-1,:-2]*ps*em[1:]*be[i,2:]
        pnull=al[i-1]*pn*be[i]
        z=pmatch.sum()+pskip.sum()+pnull.sum()+1e-300
        np.add.at(C[Tn[i-1]],Pn,pmatch/z); np.add.at(C[Tn[i-1]],Pn[1:],pskip/z); nulls+=pnull.sum()/z; skips+=pskip.sum()/z
    E=(C+0.01)/(C+0.01).sum(1,keepdims=True)
    if it%10==9: print('iter',it,'nulls %.1f skips %.1f'%(nulls,skips))
# Viterbi
V=np.full((n+1,m+1),-1e18); V[0,0]=0; bp=np.zeros((n+1,m+1),np.int8)
lE=np.log(E); lpm,lps,lpn=np.log(pm),np.log(ps),np.log(pn)
for i in range(1,n+1):
    em=lE[Tn[i-1]][Pn]
    c1=np.full(m+1,-1e18); c1[1:]=V[i-1,:-1]+lpm+em
    c2=np.full(m+1,-1e18); c2[2:]=V[i-1,:-2]+lps+em[1:]
    c3=V[i-1]+lpn
    st=np.stack([c1,c2,c3]); bp[i]=st.argmax(0); V[i]=st.max(0); V[i][~mask[i]]=-1e18
i,j=n,m; out=[]
while i>0:
    k=bp[i,j]
    if k==0: out.append((i-1,pt[j-1])); j-=1
    elif k==1: out.append((i-1,'['+pt[j-2]+']'+pt[j-1])); j-=2
    else: out.append((i-1,'_'))
    i-=1
out=out[::-1]; dec=[x[1] for x in out]
for lab,s,c in lines:
    print('%3s: %s'%(lab,' '.join(toks[s:s+c]))); print('     %s'%(' '.join(dec[s:s+c])))
# key table
key=collections.defaultdict(collections.Counter)
for (i,d) in out:
    if d!='_': key[toks[i]][d[-1]]+=1
print('\nKEY (glyph: letter counts)')
for t in sorted(key,key=lambda t:-sum(key[t].values())):
    print('%4s %3d  %s'%(t,sum(key[t].values()),' '.join('%s%d'%kv for kv in key[t].most_common(5))))
import json; json.dump({t:dict(key[t]) for t in key},open('hand/key_counts.json','w'))
