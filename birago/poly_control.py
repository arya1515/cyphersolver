# Polyphonic control matched to the target: 483 figures (16 doubled), 9 breaks, letter->digit partition with the target's digit profile.
import random,sys,re
LETTERS='abcdefghilmnopqrstuz'
def make(seed,out):
    rnd=random.Random(seed); txt=open('corpus_clean.txt').read()
    i=rnd.randrange(1000000,len(txt)-3000); p=[c for c in txt[i:i+1500] if c in LETTERS]
    # partition: shuffle letters, assign to 10 digits so that digits 6,7 get one rare letter each, others 2-3 letters
    freq={'a':.117,'e':.118,'i':.113,'o':.098,'u':.03,'n':.069,'r':.064,'s':.05,'t':.056,'l':.065,'c':.045,'d':.037,'m':.025,'p':.031,'g':.016,'b':.009,'f':.01,'h':.015,'q':.005,'z':.01}
    letters=sorted(LETTERS,key=lambda c:-freq[c]); rnd.shuffle(letters)
    rare=[c for c in letters if freq[c]<0.012]; rnd.shuffle(rare)
    assign={rare[0]:6,rare[1]:7}
    rest=[c for c in letters if c not in assign]; rnd.shuffle(rest)
    digits=[0,1,2,3,4,5,8,9]
    for k,c in enumerate(rest): assign[c]=digits[k%8]
    # encipher with doubling marks: a doubled letter -> one marked digit; breaks every ~50 letters
    outg=[];pl=[];n=0;j=0
    while n<483 and j<len(p):
        c=p[j]
        if j+1<len(p) and p[j+1]==c and c not in 'aeiou':
            outg.append(f'{assign[c]}.'); pl.append(c+c); j+=2; n+=1
        else:
            outg.append(str(assign[c])); pl.append(c); j+=1; n+=1
        if rnd.random()<0.02: outg.append('|'); pl.append('#')
        if rnd.random()<0.03: outg.append(rnd.choice('nnfmacl'))
    open(out,'w').write(' '.join(outg)); open(out.replace('.txt','_plain.txt'),'w').write(''.join(pl))
    return assign
if __name__=='__main__':
    for s in (1,2):
        a=make(s,f'pctl{s}.txt'); inv={}
        for c,d in a.items(): inv.setdefault(d,'') ; inv[d]+=c
        print(s,{d:inv.get(d,'') for d in range(10)})
