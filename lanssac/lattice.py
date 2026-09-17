"""Beam-search decode of a token line where each token has a small set of candidate strings; French 5-gram score."""
import sys, numpy as np, heapq
ALPHA='abcdefghiklmnopqrstuvxyz'; IDX={c:i for i,c in enumerate(ALPHA)}
TAB=np.load('../sp53/fr5.npy')
def lp(ctx,ch):
    if len(ctx)<4: return -3.0
    return float(TAB[IDX[ctx[-4]],IDX[ctx[-3]],IDX[ctx[-2]],IDX[ctx[-1]],IDX[ch]])
CAND={
 'X':['e'],'ast':['e'],'i':['i',''],'s':['n'],'nn':['n'],'pi':['a'],'T':['a'],'Y':['p'],'g':['s'],'7':['c'],'8':['m'],
 'c':['o'],'oo':['g'],'F':['r'],'phi':['r'],'ff':['u'],'ot':['u'],'Z':['car'],'st':['st'],'hh':['d'],'Lo':['s'],
 'G':['e','i'],'3':['l','t'],'sh':['s','t','z'],'IIII':['s','z','x'],'sm':['st','nt','r','s','ie','que','qui'],
 'qq':['qu','qui','que','q'],'N':['q','t','d','b','l'],'B':['q','n','l','r','ou','qu'],'u2':['u','v'],'L':['o','n'],
 'ol':['l','u'],'of':['f'],'cross':['h','c','ch','pour'],'pour':['h','c','ch','pour','au'],'de4':['de','d','ou'],
 '4h':['de','d','t'],'ll':['m','l','s'],'et':['et','h','e'],'d':['u','d','e','o'],'2':['de','il','ie','o'],
 'M':['x','t','u','l'],'5':['p','t'],'4':['b','de','d','s'],'q9':['i','y'],'H':['a'],'ns':['ns','n'],'D':['e'],'4o':['de','d'],
}
def decode(toks,beam=200):
    beams=[(0.0,'','')]  # score, text, spaced
    for t in toks:
        cands=CAND.get(t,[t]); nb=[]
        for sc,txt,sp in beams:
            for c in cands:
                s=sc; ctx=txt
                for ch in c:
                    s+=lp(ctx,ch); ctx+=ch
                nb.append((s,ctx,sp+('·' if c=='' else c)+' '))
        nb.sort(key=lambda b:-b[0]); beams=nb[:beam]
    return beams[:3]
if __name__=='__main__':
    lines=[]
    for l in open(sys.argv[1] if len(sys.argv)>1 else 'tokens.txt',encoding='utf-8'):
        l=l.strip()
        if not l or l[0] in '#@': continue
        lines.append(l.split())
    for toks in lines:
        for sc,txt,sp in decode(toks)[:2]: print(round(sc,1),sp)
        print()
