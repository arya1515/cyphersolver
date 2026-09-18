import sys, re
from key import load
K=load()
def dec(s):
    out=[]
    for tok in re.findall(r'\[[^\]]*\]|[^\[\]]+', s):
        if tok.startswith('['):
            nums=re.findall(r'\d+\??', tok)
            parts=[]
            for n in nums:
                q=n.endswith('?'); v=int(n.rstrip('?'))
                if v<3 or v>2342 or v%10 in (5,9) or 516<v<617: w='<null>'
                else: w=K.get(v,'<%d?>'%v)
                parts.append(w+('?' if q else ''))
            out.append('{'+' '.join(parts)+'}')
        else: out.append(tok)
    return ''.join(out)
if __name__=='__main__':
    print(dec(open(sys.argv[1],encoding='utf8').read()))
