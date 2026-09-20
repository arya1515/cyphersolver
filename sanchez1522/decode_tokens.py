"""Resolve a space-separated token string against the Sanchez 1522 key.
Codes are CVC (or CV); a trailing 's' marks the plural sign (q with double bar).
Unknown three-letter codes get an alphabetical bracket from their neighbours."""
import sys,re
C1='zyxvtsrpnmlhgfdcb'; V='aeiou'; C3='bcdfghlmn'
K={}
for line in open('key_codes.tsv',encoding='utf-8').read().splitlines()[1:]:
    c,p=line.split('\t'); K[c.rstrip('?')]=p
def rank(k):
    return (C1.index(k[0]),C3.index(k[2]),V.index(k[1])) if (len(k)==3 and k[0] in C1 and k[1] in V and k[2] in C3) else None
ORD=sorted(((rank(k),k,p) for k,p in K.items() if rank(k)),key=lambda t:t[0])
def bracket(k):
    r=rank(k)
    if not r: return None
    lo=[p for rr,_,p in ORD if rr<r]; hi=[p for rr,_,p in ORD if rr>r]
    return '<%s..%s>'%(lo[-1] if lo else '', hi[0] if hi else '')
def one(t):
    plural = t.endswith('+s')
    k=t[:-2] if plural else t
    if k in K: v=re.sub(r" *\[.*?\]","",K[k])
    else:
        b=bracket(k); v=('?%s%s'%(k,b) if b else '?'+k)
    return v+('s' if plural else '')
if __name__=='__main__':
    toks=sys.argv[1:] or sys.stdin.read().split()
    print(' '.join(one(t) for t in toks))
