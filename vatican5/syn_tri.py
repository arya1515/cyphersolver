"""Identifiability check: synthetic polyphonic cipher from the Italian corpus, then trigram partition SA."""
import re, random, json, math, sys
import numpy as np
AL='abcdefghilmnopqrstuvz'; LI={c:i for i,c in enumerate(AL)}; B=len(AL); N=B+1
rnd=random.Random(7)
t=open('corpus_it.txt',encoding='utf-8',errors='ignore').read().lower()
t=re.sub(r'[^a-z ]+',' ',t); t=re.sub(r'[jkwxy]','',t); t=re.sub(r' +',' ',t)
start=rnd.randrange(0,len(t)-8000); sample=t[start:start+7000]
digits=[0,1,2,3,5,6,7,8,9]
letters=list(AL); rnd.shuffle(letters)
truth={}
for i,c in enumerate(letters): truth[LI[c]]=digits[i%9]
seq=[]
for ch in sample:
    if ch==' ':
        if rnd.random()<0.45: seq.append(4)
        continue
    seq.append(truth[LI[ch]])
print('true key:',' '.join(f"{d}={''.join(AL[l] for l in sorted(truth) if truth[l]==d)}" for d in digits))
import trigramfit as tf
C=np.zeros((10,10,10))
for a,b,c in zip(seq,seq[1:],seq[2:]): C[a,b,c]+=1
tf.C=C; tf.mask=C>0
print('true key LL:',round(tf.ll(truth),1))
for trial in range(3):
    v,a=tf.sa(random.Random(trial),150000); print('trial',trial,round(v,1),tf.show(a),flush=True)
