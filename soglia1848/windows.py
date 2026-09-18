import collections,numpy as np,bisect
w=collections.Counter(open('it19.txt').read().split())
N=1500
anch={8319:'imperatore',8340:'istruzione',8374:'monsignor',8422:'opportuno',8424:'ordine',8429:'padre',8433:'parte',8446:'porto',8620:'roma'}
V=sorted(set([x for x,_ in w.most_common(N) if len(x)>1]+list(anch.values())+['santo','santita','signor','conte','vostra','signoria','sua','senonche','spirato','stante','sei','sette','venti','tre','maggio','giugno','corrente','scorso','passato','germania','baviera','svizzera','napoli','firenze','torino','milano','vienna','inspruck','lombardia','ambasciatore','ministro','governo','guerra','comunicata','codesta','cotesta','affine','lontana','libera']))
ks=sorted(anch); rs=[bisect.bisect_left(V,anch[k]) for k in ks]
slope=(rs[-1]-rs[0])/(ks[-1]-ks[0])
def pred(c):
    if c<ks[0]: return rs[0]-(ks[0]-c)*slope*1.0
    if c>ks[-1]: return rs[-1]+(c-ks[-1])*slope
    return np.interp(c,ks,rs)
for c in [8093,8102,8110,8116,8120,8122,8131,8136,8211,8227,8247,8310,8346,8413,8632,8704,8734,8737,8739,8760,8904]:
    p=int(pred(c)); print(c,V[p],'|',' '.join(V[max(0,p-25):p+25]))
    print()
