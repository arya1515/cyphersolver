# Decode a class-string transcription (A B C D E F G H I L M = pairs an bo cp dq er fs gt hu ix ly mz; Q=que K=qui P=pour
# S=S-sign W=du-Mayne-sign .=null ?=unknown |=word break hint (ignored) ) with the French 6-gram beam decoder.
import sys, os, re
sys.path.insert(0,'sega1593'); sys.path.insert(0,'sp53')
from poly_decode import decode, LM
MAP={'A':'a','B':'b','C':'c','D':'d','E':'e','F':'f','G':'g','H':'h','I':'i','L':'l','M':'m'}
def to_poly(s):
    out=[]
    for ch in s:
        if ch in MAP: out.append(MAP[ch])
        elif ch=='Q': out.append('{que}')
        elif ch=='K': out.append('{qui}')
        elif ch=='P': out.append('{pour}')
        elif ch=='S': out.append('{s}')      # placeholder, treated as letter s-sign
        elif ch=='W': out.append('{dumayne}')
        elif ch=='?': out.append('?')
    return ''.join(out)
if __name__=='__main__':
    lm=LM('sp53/fr6.pkl')
    txt=open(sys.argv[1],encoding='utf-8').read() if os.path.exists(sys.argv[1]) else sys.argv[1]
    beam=int(sys.argv[2]) if len(sys.argv)>2 else 3000
    for line in txt.strip().split('\n'):
        if not line.strip() or line.startswith('#'): continue
        tag,_,s=line.partition(':') if ':' in line else ('',None,line)
        s=re.sub(r'[\s|.]','',s)
        res=decode(to_poly(s),lm,beam=beam,nbest=1)
        print(tag, res[0][0])
