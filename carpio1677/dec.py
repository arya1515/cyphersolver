import sys,glob
from parse import load
L='a b c d e f g h i l m n o p q r s t u x y z'.split()
P={str(9+i):c for i,c in enumerate(L)}
for b,c in {31:'m',36:'n',41:'p',46:'r',51:'s',56:'t'}.items():
    for j,v in enumerate('aeiou'): P[str(b+j)]=c+v
S={}
for b,c in {15:'t',20:'f'}.items():
    for j,v in enumerate('aeiou'): S[str(b+j)]=c+v
for b,c in {30:'l',35:'s',40:'n',45:'r'}.items():
    for j,v in enumerate('aeiou'): S[str(b+j)]=v+c
S.update({'50':'que','51':'qua','52':'qui','N':'_','R':'_','g':'_','4':'_'})
SP={'ag':'ha','eg':'he','116':'V.S.'}
sw={'b':'c','c':'b','g':'d','l':'g','m':'l','d':'m','ì':'i','í':'i'}
def tr(t):
    if t.endswith('*'):
        k=t[:-1]; return S[k] if k in S else '['+k+']'
    if t in P: return P[t]
    if t in SP: return SP[t]
    if t.isalpha(): return ''.join(sw.get(ch,ch) for ch in t.lower())
    return '{'+t+'}'
def dec(f): return ' '.join(tr(t) for t in load(glob.glob('img/DOC_R%s*'%f)[0]))
if __name__=='__main__': print(dec(sys.argv[1]))
