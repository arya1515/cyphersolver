import pickle, math, sys, json, collections
D=pickle.load(open('lm.pkl','rb')); CNT=D['cnt']; N=D['N']
AL='abcdefghilmnopqrstuxyz'   # no j k v w (period orthography: u=v, i=j)
LAM=0.4
MINCTX=15   # a context must be properly attested: 8 stray 'iiiii' once made runs of i
            # score better than French, which let the solver collapse onto one letter
def logp(ctx, ch):
    # interpolated backoff
    p=0.0; w=1.0; tot=0.0
    for n in range(N,0,-1):
        if n==1:
            num=CNT[1][ch]; den=sum(CNT[1].values())
            tot+=w*(num+1)/(den+len(AL)); break
        c=ctx[-(n-1):] if n>1 else ''
        if len(c)<n-1: continue
        den=CNT[n-1][c] if n>1 else 0
        if den<MINCTX: continue
        num=CNT[n][c+ch]
        tot+=w*LAM*(num/den); w*=(1-LAM)
        if w<1e-6: break
    return math.log(max(tot,1e-12))

def beam(tokens, cand, width=400):
    # cand: dict token -> list of letters (or '' for null / multi-letter string for codes)
    beams=[('',0.0)]
    for t in tokens:
        opts=cand.get(t)
        if opts is None: opts=list(AL)
        nb=[]
        for txt,sc in beams:
            for o in opts:
                s=sc; c=txt
                for ch in o:
                    s+=logp(c,ch); c=c+ch
                nb.append((c[-60:] if False else c, s))
        nb.sort(key=lambda x:-x[1])
        # dedupe by last N-1 chars
        seen={}; out=[]
        for txt,sc in nb:
            k=txt[-(N-1):]
            if k in seen: continue
            seen[k]=1; out.append((txt,sc))
            if len(out)>=width: break
        beams=out
    return beams

WORDS={}
for line in open('corpus_words.txt',encoding='utf-8'):
    w,c=line.rstrip('\n').split('\t'); WORDS[w]=int(c)
TOTW=sum(WORDS.values())
def segment(s, maxw=16):
    n=len(s); best=[(-1e18,-1)]*(n+1); best[0]=(0.0,-1)
    for i in range(1,n+1):
        for j in range(max(0,i-maxw),i):
            w=s[j:i]
            c=WORDS.get(w,0)
            sc=math.log((c+0.01)/TOTW) - 3.0*(0 if c else len(w))
            v=best[j][0]+sc
            if v>best[i][0]: best[i]=(v,j)
    out=[];i=n
    while i>0:
        j=best[i][1]; out.append(s[j:i]); i=j
    return ' '.join(reversed(out))
if __name__=='__main__':
    print(segment('vouspouezjugerquecesteouuerturenestpastoutenouuelle'))
