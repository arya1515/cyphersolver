import numpy as np,re,unicodedata,glob,sys
A='abcdefghilmnopqrstuz'  # v->u, j->i, k w x y dropped
def clean(t):
    t=unicodedata.normalize('NFKD',t.lower()); t=''.join(c for c in t if not unicodedata.combining(c))
    t=t.replace('v','u').replace('j','i').replace('y','i')
    words=[w for w in re.findall(r'[a-z]+',t) if not (re.fullmatch(r'[iuxlcdm]+',w) and w not in ('di','mi','li','il','ci','ui','dl','lui','cui','mi','mill'))]
    return ''.join(words).translate(str.maketrans('','','kwx'))
def strip_gut(t):
    a=t.find('*** START'); b=t.find('*** END'); 
    return t[a:b] if a>0 and b>a else t
def build(files,out='it'):
    text=''.join(clean(strip_gut(open(f,encoding='utf-8',errors='ignore').read())) for f in files)
    idx=np.frombuffer(text.encode(),dtype=np.uint8).astype(np.int64)-97; n=len(idx)
    print('chars',n)
    # interpolated absolute-discount 5-gram over 26 letters
    p1=(np.bincount(idx,minlength=26)+0.5)/(n+13)
    P=p1
    tabs={}
    prev=p1  # shape (26,) for order1
    for order in range(2,6):
        ctx=np.zeros(len(idx)-order+1,dtype=np.int64)
        for k in range(order-1): ctx=ctx*26+idx[k:len(idx)-order+1+k]
        nxt=idx[order-1:]
        c=np.bincount(ctx*26+nxt,minlength=26**order).astype(np.float64).reshape(-1,26)
        tot=c.sum(1,keepdims=True); D=0.75
        nz=(c>0).sum(1,keepdims=True)
        lower=prev if order==2 else prev.reshape(-1,26)
        # lower for ctx (a,b,c,d) is prev[(b,c,d)] -> tile
        if order==2: low=np.tile(prev[None,:],(26,1))
        else: low=np.tile(prev.reshape(26**(order-2),26),(26,1))
        p=np.where(tot>0,(np.maximum(c-D,0)+D*nz*low)/np.maximum(tot,1),low)
        prev=p
    np.save(out+'5.npy',np.log(prev.astype(np.float32)).reshape(-1))
    return text
if __name__=='__main__': build(sorted(glob.glob('corpus/*.txt')))
