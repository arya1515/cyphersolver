# Control for design H*: every letter token is a two-digit number (about NSYM homophones over 00-99), 22 code groups, 15 nulls.
import random,re,sys,collections
def make(seed,ntok=215,nsym=60,nomen=22,nulls=15):
    rnd=random.Random(seed); txt=open('corpus_clean.txt').read()
    letters='abcdefghilmnopqrstuz'
    base={'a':0.117,'e':0.118,'i':0.113,'o':0.098,'u':0.03,'n':0.069,'r':0.064,'s':0.05,'t':0.056,'l':0.065,'c':0.045,'d':0.037,'m':0.025,'p':0.031,'g':0.016,'b':0.009,'f':0.01,'h':0.015,'q':0.005,'z':0.01}
    # allocate homophones roughly proportional to frequency, at least 1
    alloc={L:1 for L in letters}; rem=nsym-len(letters)
    for L in sorted(letters,key=lambda L:-base[L]):
        k=round(base[L]*rem); alloc[L]+=k
    while sum(alloc.values())>nsym:
        L=max(alloc,key=alloc.get); alloc[L]-=1
    pool=[f'{i:02d}' for i in range(100)]; rnd.shuffle(pool); key={}; pi=0
    for L in letters: key[L]=pool[pi:pi+alloc[L]]; pi+=alloc[L]
    i=rnd.randrange(3000000,len(txt)-2000); p=txt[i:i+1000]
    out=[];plain=[]
    for c in p:
        if c not in key: continue
        out.append(rnd.choice(key[c])); plain.append(c)
        if len(out)>=ntok: break
    pos=sorted(rnd.sample(range(len(out)),nomen+nulls)); ins={}
    for q,ps in enumerate(pos): ins[ps]=(rnd.choice('%:+-')+f'{rnd.randrange(100):02d}') if q<nomen else rnd.choice('nnnnfmacli')
    ct=[];pl=[]
    for q,(t,c) in enumerate(zip(out,plain)):
        if q in ins: ct.append(' '+ins[q]+' '); pl.append('#' if ins[q][0] in '%:+-' else '')
        ct.append(' '+t); pl.append(c)
    return ''.join(ct),''.join(pl),key
if __name__=='__main__':
    for seed in (1,2,3):
        nsym=int(sys.argv[1]) if len(sys.argv)>1 else 60
        ct,pl,key=make(seed,nsym=nsym); open(f'cpair{nsym}_{seed}.txt','w').write(ct); open(f'cpair{nsym}_{seed}_plain.txt','w').write(pl)
        print(seed,pl[:100])
