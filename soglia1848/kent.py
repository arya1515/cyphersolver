import collections,sys
s=open('ct.txt').read()
def parse(s):
    toks=[];i=0;buf=''
    while i<len(s):
        c=s[i]
        if c=='5':
            toks.append('5'); i+=1; continue
        if c=='7' and buf=='':
            # take 7 + next 3 non-5 digits
            j=i+1;g='7'
            while len(g)<4 and j<len(s):
                if s[j]!='5': g+=s[j]
                j+=1
            toks.append(g); i=j; continue
        buf+=c; i+=1
        if len(buf)==2: toks.append(buf); buf=''
    return toks
t=parse(s)
print(' '.join(t))
C=collections.Counter(x for x in t if x!='5')
print(len(t), len(C))
print(sorted(C.items(),key=lambda x:-x[1]))
