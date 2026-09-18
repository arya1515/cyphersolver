"""Is the fr. 3621 no. 97 symbol stream consistent with a letter-for-letter cipher?

Compares the index of coincidence of single symbols and of adjacent symbol pairs against
(a) letter-homophonic ciphertexts built from real French with the same symbol count and
segmentation, and (b) plain French itself. A syllabic or word-level cipher, which the
surviving French keys of this milieu all contain alongside their letter alphabets, gives a
different digraph coincidence rate from a letter cipher.
"""
import re, random, collections, sys
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])

P0=Problem(); seglens=[len(g) for g in P0.segs]; nsym=P0.ns
txt=open('src/corpus_fr.txt',encoding='utf-8',errors='replace').read().lower()
txt=re.sub(r'[^a-z]',' ',txt).translate(str.maketrans({'v':'u','w':'u','j':'i','k':'c'}))
txt=''.join(txt.split())

def ic(seq):
    c=collections.Counter(seq); n=len(seq)
    return sum(k*(k-1) for k in c.values())/(n*(n-1))

def ic2(segs):
    pairs=[]
    for g in segs:
        for i in range(len(g)-1): pairs.append((g[i],g[i+1]))
    c=collections.Counter(pairs); n=len(pairs)
    return sum(k*(k-1) for k in c.values())/(n*(n-1)), n, len(c)

def rep3(segs):
    """fraction of trigram positions whose trigram occurs more than once"""
    tri=[]
    for g in segs:
        for i in range(len(g)-2): tri.append(tuple(g[i:i+3]))
    c=collections.Counter(tri)
    return sum(1 for t in tri if c[t]>1)/len(tri), len(tri)

print('MANUSCRIPT  BnF fr. 3621 no. 97')
ms=[[s for s in g] for g in P0.segs]
i1=ic([s for g in ms for s in g]); i2,np_,nd=ic2(ms); r3,nt=rep3(ms)
print(f'  symbols {sum(len(g) for g in ms)}  distinct {nsym}')
print(f'  IC1 {i1:.5f}   IC2 {i2:.6f} over {np_} pairs, {nd} distinct   trigram-repeat {r3*100:.1f}%')
print()
print('CONTROLS  real French enciphered letter-for-letter, same size and segmentation')
def mkct(seed, homo_n):
    rnd=random.Random(seed)
    p=rnd.randrange(len(txt)-5000); pt=txt[p:p+sum(seglens)]
    order=sorted(range(NA), key=lambda i:-FREQ[i])
    sl=[order[i%NA] for i in range(homo_n)]; rnd.shuffle(sl)
    h=collections.defaultdict(list)
    for si,li in enumerate(sl): h[li].append(si)
    for li in range(NA):
        if not h[li]: h[li]=[rnd.randrange(homo_n)]
    ct=[rnd.choice(h[AI[ch]]) for ch in pt]
    segs=[]; k=0
    for L in seglens: segs.append(ct[k:k+L]); k+=L
    return segs, pt
for label,hn in (('44-symbol homophonic',44),('22-symbol monoalphabetic',22)):
    A=[];B=[];C=[]
    for sd in range(41,49):
        segs,pt=mkct(sd,hn)
        A.append(ic([s for g in segs for s in g])); b,_,_=ic2(segs); B.append(b)
        c,_=rep3(segs); C.append(c)
    m=lambda L: sum(L)/len(L); lo=lambda L: min(L); hi=lambda L: max(L)
    print(f'  {label:26s} IC1 {m(A):.5f} [{lo(A):.5f}-{hi(A):.5f}]  IC2 {m(B):.6f} [{lo(B):.6f}-{hi(B):.6f}]  tri-rep {m(C)*100:.1f}%')
print()
segs,pt=mkct(41,22)
plain=[]; k=0
for L in seglens: plain.append(pt[k:k+L]); k+=L
p1=ic(pt); p2,_,_=ic2(plain); p3,_=rep3(plain)
print(f'  {"plain French (22 letters)":26s} IC1 {p1:.5f}  IC2 {p2:.6f}  tri-rep {p3*100:.1f}%')
