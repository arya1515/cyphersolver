"""Decode Maisse's Cipher (1592) with Tomokiyo's key."""
import sys, re
K={}
for line in open('key1.tsv'):
    if line.startswith('#') or not line.strip(): continue
    a,b=line.split('\t'); K[a.strip()]=b.strip()
def dec(toks):
    out=[]
    for t in toks:
        if t in K: out.append(K[t])
        elif t=='w': out.append('[w]')
        else: out.append('{%s}'%t)
    return ''.join(out)
if __name__=='__main__':
    toks=[]
    for line in open(sys.argv[1]):
        if line.startswith('#'): continue
        toks+=line.split()
    print(dec(toks))
