import re,collections,json
L=[];cur=None
for l in open('img/DOC_R1874_D3607_3607.txt',encoding='utf8'):
    if l.startswith('#IMAGE'): cur=l.split()[-1]
    if l.strip() and not l.startswith(('#','<')): L.append((cur,l))
PRE=('6','21','13','11','12','15','17','10','14','16')
toks=[]
for pg,l in L:
    s=l.replace('?','').replace("'",'')
    for g in re.split(r'\s{2,}',s.strip()):
        g=g.replace(' ','')
        if not g: continue
        if not g.isdigit(): toks.append((pg,g)); continue
        if toks and not g.startswith(PRE) : toks[-1]=(toks[-1][0],toks[-1][1]+g)
        else: toks.append((pg,g))
if __name__=='__main__':
    c=collections.Counter(t for _,t in toks)
    print(len(toks),len(c)); print(c.most_common(150))
    lens=collections.Counter(len(t) for _,t in toks); print(lens)
