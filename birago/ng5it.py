import numpy as np,re,sys,unicodedata

def clean(t):

    t=unicodedata.normalize('NFKD',t.lower()); t=''.join(c for c in t if not unicodedata.combining(c))

    t=t.replace('&',' et ')

    words=re.findall(r'[a-z]+',t)

    keep=[]

    for w in words:

        if re.fullmatch(r'[ivxlcdm]+',w) and w not in ('di','mi','li','il','ci','vi','d�','mill','dl'): continue

        if any(ch in w for ch in 'kwxyj'): continue

        keep.append(w.replace('v','u'))

    return ''.join(keep)

def build(files,out='ng5it.npy'):

    text=''.join(clean(open(f,encoding='utf-8',errors='ignore').read()) for f in files)

    idx=np.frombuffer(text.encode(),dtype=np.uint8).astype(np.int64)-97; n=len(idx)

    c5=np.bincount(idx[:-4]*456976+idx[1:-3]*17576+idx[2:-2]*676+idx[3:-1]*26+idx[4:],minlength=26**5).astype(np.float32)

    c4=np.bincount(idx[:-3]*17576+idx[1:-2]*676+idx[2:-1]*26+idx[3:],minlength=26**4).astype(np.float32)

    c3=np.bincount(idx[:-2]*676+idx[1:-1]*26+idx[2:],minlength=26**3).astype(np.float32)

    c2=np.bincount(idx[:-1]*26+idx[1:],minlength=26**2).astype(np.float32)

    ctx4=c5.reshape(26**4,26).sum(1); ctx3=c4.reshape(26**3,26).sum(1); ctx2=c3.reshape(26**2,26).sum(1); ctx1=c2.reshape(26,26).sum(1)







    k=0.02
    p1=(np.bincount(idx,minlength=26)+1)/(n+26)
    p2=(c2.reshape(26,26)+k)/(ctx1[:,None]+26*k)
    p3=(c3.reshape(676,26)+k)/(ctx2[:,None]+26*k)
    p4=(c4.reshape(17576,26)+k)/(ctx3[:,None]+26*k)
    p5=(c5.reshape(456976,26)+k)/(ctx4[:,None]+26*k)
    P=0.55*p5+0.25*np.tile(p4,(26,1))+0.12*np.tile(p3,(676,1))+0.06*np.tile(p2,(17576,1))+0.02*p1[None,:]
    np.save(out,np.log(P).astype(np.float32).reshape(-1)); np.save('p1it.npy',p1)

    print('chars',n); return text

def load(): return np.load('ng5it.npy')

def toidx(t): return np.frombuffer(t.encode(),dtype=np.uint8).astype(np.int64)-97

def score(tab,p):

    q=p[:-4]*456976+p[1:-3]*17576+p[2:-2]*676+p[3:-1]*26+p[4:]

    return float(tab[q].sum())

if __name__=='__main__':

    text=build(sys.argv[1:])

    open('corpus_clean.txt','w').write(text)

    tab=load()

    for t in ['lasupplicoafarlosaperealreetallaregina','quellichehannoilgouernodicarmagnola','xkqzwjfhgbdpqzxkwmnbv','etquestocheiononuoglio']:

        print(round(score(tab,toidx(t))/(len(t)-4),3),t)

