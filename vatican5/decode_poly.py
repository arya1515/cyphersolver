"""Viterbi decode of the Vatican-5 digit stream under a polyphonic key ("0=abc 1=de ..."), Italian trigram LM.
Dotted digits / after-dot digits are shown as [..] codes; 4 = word space."""
import sys, json, math, re
import numpy as np
from parse5 import load, digit_stream
AL='abcdefghilmnopqrstuvz'; LI={c:i for i,c in enumerate(AL)}; B=len(AL); N=B+1
ng=json.load(open('it_ngrams.json',encoding='utf-8'))
C3=np.full((N,N,N),0.5)
for k,v in ng['3'].items():
    idx=[LI.get(ch, B if ch==' ' else None) for ch in k]
    if None in idx: continue
    C3[idx[0],idx[1],idx[2]]+=v
L3=np.log(C3/C3.sum(axis=2,keepdims=True))
def parse_key(s):
    key={}
    for part in s.split():
        d,ls=part.split('='); key[int(d)]=[LI[c] for c in ls if c in LI]
    return key
def decode(key, runs):
    out=[]
    for r in runs:
        # build candidate lists per position; codes -> boundary marker
        cands=[]; marks=[]
        for i,t in enumerate(r):
            d=int(t[0]); dotted=('^' in t or '_' in t); after=i>0 and ('^' in r[i-1] or '_' in r[i-1])
            if d==4: cands.append([B]); marks.append(' '); continue
            if dotted or after: cands.append([B]); marks.append(f'[{t}]'); continue
            cands.append(key.get(d,[B])); marks.append(None)
        # Viterbi over states (prev2, prev1)
        S=N*N; V=np.full(S,-1e9); V[B*N+B]=0.0; back=[]
        for pos,cl in enumerate(cands):
            NV=np.full(S,-1e9); BP=np.full(S,-1,dtype=np.int64)
            p2=np.arange(S)//N; p1=np.arange(S)%N
            for c in cl:
                sc=V+L3[p2,p1,c]; ns=p1*N+c
                # scatter max
                order=np.argsort(sc)
                NV[ns[order]]=np.maximum(NV[ns[order]],sc[order])
                better=sc>NV[ns]-1e-12
                BP[ns[better]]=np.arange(S)[better]
            V=NV; back.append(BP)
        s=int(np.argmax(V)); letters=[]
        for pos in range(len(cands)-1,-1,-1):
            letters.append(s%N); s=int(back[pos][s])
        letters=letters[::-1]
        txt=''.join(marks[i] if marks[i] is not None else AL[letters[i]] for i in range(len(cands)))
        out.append(txt)
    return out
if __name__=='__main__':
    key=parse_key(sys.argv[1]); runs=digit_stream(load())
    res=decode(key,runs)
    n=int(sys.argv[2]) if len(sys.argv)>2 else 6
    for t in res[:n]: print(t[:400]); print()
