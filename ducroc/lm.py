import numpy as np,re,unicodedata,glob
# French, 16th c. orthography; alphabet a-z with v->u, j->i, plus space = index 26
def clean(t):
    t=unicodedata.normalize('NFKD',t.lower()); t=''.join(c for c in t if not unicodedata.combining(c))
    t=t.replace('v','u').replace('j','i').replace('k','').replace('w','')
    words=re.findall(r'[a-z]+',t)
    words=[w for w in words if not (re.fullmatch(r'[iuxlcdm]+',w) and w not in ('il','du','di','lui','mi','ci','cil','mil','lui')) and 'ii' not in w and len(w)<16]
    return ' '.join(words)
def build(files,out='fr',spaces=True):
    text=' '.join(clean(open(f,encoding='utf-8',errors='ignore').read()) for f in files)
    if not spaces: text=text.replace(' ','')
    idx=np.array([26 if c==' ' else ord(c)-97 for c in text],dtype=np.int64); n=len(idx); V=27
    print('chars',n)
    prev=(np.bincount(idx,minlength=V)+0.5)/(n+V/2)
    for order in range(2,6):
        ctx=np.zeros(n-order+1,dtype=np.int64)
        for k in range(order-1): ctx=ctx*V+idx[k:n-order+1+k]
        nxt=idx[order-1:]
        c=np.bincount(ctx*V+nxt,minlength=V**order).astype(np.float64).reshape(-1,V)
        tot=c.sum(1,keepdims=True); D=0.75; nz=(c>0).sum(1,keepdims=True)
        low=np.tile(prev.reshape(-1,V) if order>2 else prev[None,:],(V,1))
        prev=np.where(tot>0,(np.maximum(c-D,0)+D*nz*low)/np.maximum(tot,1),low)
    np.save(out+'5.npy',np.log(prev.astype(np.float32)).reshape(-1))
if __name__=='__main__':
    build(sorted(glob.glob('corpus/*.txt')))
    build(sorted(glob.glob('corpus/*.txt')),out='frn',spaces=False)
