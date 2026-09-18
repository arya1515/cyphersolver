import sys,re
K={}
for letter,toks in [('a','q T x f X'),('c','z'),('d','v 6 n'),('e','g D t e3 S'),('g','12'),('h','+ 7'),
 ('i','pi 6^ 33 ph'),('l','II p m'),('m','HH oo'),('n','8 s 4 o.'),('o','o Lo F 24 4_'),('p','E 26 I'),('q','H 28'),
 ('r','r 30 Q rr'),('s','80 dz k tt'),('t','y 4y h'),('u','L A d J 36'),('y','44 56 60'),('&','w'),('','# ... C ?')]:
    for t in toks.split(): K[t]=letter
K0=K
if __name__=='__main__':
 for f in sys.argv[1:]:
  for line in open(f,encoding='utf-8'):
    m=re.match(r'(C\d+):\s*(.*)',line)
    if not m: continue
    out=''.join(K.get(t,'['+t+']') for t in m.group(2).split())
    print(m.group(1),out)
