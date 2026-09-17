"""Word-aware beam decoder: decides letters and word boundaries jointly.

State: (words_so_far_score, current_word, char_context). At each glyph token we try every
candidate letter; after appending we may also close the current word. Closing scores the word by
a unigram model (with a character-LM fallback for words the corpus does not have), which is what
lets French vocabulary, not just 6-gram statistics, correct a mis-seen glyph.
"""
import json, math, sys, pickle, heapq
D=pickle.load(open('lm.pkl','rb')); CNT=D['cnt']; N=D['N']
AL='abcdefghilmnopqrstuxyz'
LAM=0.4
def clogp(ctx,ch):
    tot=0.0; w=1.0
    for n in range(N,1,-1):
        c=ctx[-(n-1):]
        if len(c)<n-1: continue
        den=CNT[n-1][c]
        if den<2: continue
        tot+=w*LAM*(CNT[n][c+ch]/den); w*=(1-LAM)
        if w<1e-6: break
    u=CNT[1][ch]; tot+=w*(u+1)/(sum(CNT[1].values())+22)
    return math.log(max(tot,1e-12))
WORDS={}
for line in open('corpus_words.txt',encoding='utf-8'):
    w,c=line.rstrip('\n').split('\t'); WORDS[w]=int(c)
TOT=sum(WORDS.values())
PREF=set()
for w in WORDS:
    for i in range(1,len(w)+1): PREF.add(w[:i])
def wordlp(w):
    c=WORDS.get(w)
    if c: return math.log(c/TOT)
    # unknown: charLM cost plus a flat penalty
    s=0.0; ctx=' '
    for ch in w: s+=clogp(ctx,ch); ctx+=ch
    return s-7.0
key=json.load(open('key.json'))
def decode(tokens, width=500, maxw=16):
    """beam entry: (score, words, curword, ctx, curcharlp)

    While a word is being built we charge the character model, so partial states stay comparable;
    when the word closes we add (unigram word score - the character score already charged), i.e.
    we swap the char model for the word model over exactly that span."""
    beams=[(0.0,(),'',' ',0.0)]
    for t in tokens:
        opts=key.get(t, list(AL))
        nb=[]
        for sc,ws,cw,ctx,ccl in beams:
            for o in opts:
                if o and not o[0].isalpha():
                    ns=sc+((wordlp(cw)-ccl) if cw else 0.0)
                    nb.append((ns,ws+((cw,) if cw else ())+(o,),'',' ',0.0)); continue
                w2=cw+o
                if len(w2)>maxw: continue
                d=0.0; c=ctx
                for ch in o:
                    d+=clogp(c,ch); c=(c+ch)[-(N-1):]
                nb.append((sc+d,ws,w2,c,ccl+d))
                nb.append((sc+d+wordlp(w2)-(ccl+d),ws+(w2,),'',' ',0.0))
        if not nb: break
        nb.sort(key=lambda x:-x[0])
        seen=set(); out=[]
        for e in nb:
            k=(e[2],e[3])
            if k in seen: continue
            seen.add(k); out.append(e)
            if len(out)>=width: break
        beams=out
    best=max(beams,key=lambda e:e[0]+((wordlp(e[2])-e[4]) if e[2] else 0.0))
    ws=best[1]+((best[2],) if best[2] else ())
    return ' '.join(ws)
if __name__=='__main__':
    for i,line in enumerate(open(sys.argv[1],encoding='utf-8'),1):
        line=line.strip()
        if line: print(i, decode(line.split()))
