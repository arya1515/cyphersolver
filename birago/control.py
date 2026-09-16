# Synthetic control: Italian text enciphered with a random variable-length figure key of the target's design.
import re,random,sys,collections,unicodedata
import ng5it
def make(seed,ndig=482,S=None,nomen=22,nulls=15,src='../sp53/corpus_it.txt'):
    rnd=random.Random(seed)
    txt=ng5it.clean(open(src,encoding='utf-8',errors='ignore').read())
    txt=re.sub(r'[^a-z]','',txt)
    S=S or set(rnd.sample('0123456789',rnd.choice([2,3,3,4])))
    singles=[d for d in '0123456789' if d not in S]
    twos=[a+b for a in S for b in '0123456789']
    pool=singles+twos; rnd.shuffle(pool)
    letters='abcdefghilmnopqrstuz'  # 20-letter Italian alphabet (u=v, i=j)
    # homophones: more for vowels, proportional-ish
    weights={'a':3,'e':3,'i':3,'o':3,'u':2,'n':2,'r':2,'s':2,'t':2,'l':2,'c':2,'d':1,'m':1,'p':1,'g':1,'b':1,'f':1,'h':1,'q':1,'z':1}
    key={}; pi=0
    for L in letters:
        k=min(weights[L],1+ (len(pool)-len(letters))//len(letters))
        key[L]=[]
        for _ in range(k):
            if pi<len(pool): key[L].append(pool[pi]); pi+=1
    for L in letters:
        if not key[L]: key[L]=[pool[pi%len(pool)]]; pi+=1
    i=rnd.randrange(100000,len(txt)-2000); p=txt[i:i+1500]
    p=p.replace('k','c').replace('x','s').replace('y','i').replace('w','u')
    out=[]; plain=[]; n=0
    marks='%:+-'
    j=0
    while n<ndig:
        c=p[j]; j+=1
        if c not in key: continue
        out.append(rnd.choice(key[c])); plain.append(c); n+=len(out[-1])
    # insert nomenclator groups and null letters at random positions
    pos=sorted(rnd.sample(range(len(out)),nomen+nulls))
    ins={}
    for q,ps in enumerate(pos):
        if q<nomen: ins[ps]=rnd.choice(marks)+f'{rnd.randrange(100):02d}'
        else: ins[ps]=rnd.choice('nnnnfmacl')
    ct=[]; pl=[]
    for q,(t,c) in enumerate(zip(out,plain)):
        if q in ins: ct.append(' '+ins[q]+' '); pl.append('#' if ins[q][0] in marks else '')
        ct.append(t); pl.append(c)
    return ''.join(ct),''.join(pl),S,key
if __name__=='__main__':
    seed=int(sys.argv[1]); ct,pl,S,key=make(seed)
    open(f'control{seed}.txt','w').write(ct); open(f'control{seed}_plain.txt','w').write(pl)
    print('S=',''.join(sorted(S))); print(pl[:120]); print(ct[:200])
