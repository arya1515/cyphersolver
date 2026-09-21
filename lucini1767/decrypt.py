import re,sys
key={}
for l in open('decode/DOC_R120_D3314_3314.txt',encoding='utf8'):
    m=re.match(r'^([\d|]+) - (.+)$',l.strip())
    if m:
        for c in m.group(1).split('|'): key[c]=m.group(2)
# Corrections and additions made here (21 Sept 2026)
key.update({'63':'se','03':'chi','8061':'qual','8099':'zion','8700':'anno'})
def dec(d):
    i=0;out=[];toks=[]
    while i<len(d):
        if d[i]=='5': toks.append('5');out.append('_');i+=1;continue
        n=4 if d[i]=='8' else 2
        t=d[i:i+n];toks.append(t);out.append(key.get(t,'<%s>'%t));i+=n
    return toks,out
if __name__=='__main__':
    d=re.sub(r'\D','',''.join(l for l in open(sys.argv[1]) if not l.startswith('#')))
    toks,out=dec(d)
    print(' '.join(toks));print(' '.join(out))
    print(''.join(o if o!='_' else ' ' for o in out).replace('u|v','v'))
