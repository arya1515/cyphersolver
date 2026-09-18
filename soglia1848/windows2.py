import collections,numpy as np,bisect
w=collections.Counter(open('it19.txt').read().split())
A={8110:'col',8116:'colonia',8120:'come',8122:'cotesta',8211:'e',8247:'foglio',8310:'guerra',8319:'imperatore',8340:'istruzione',8346:'lontano',8374:'monsignor',8422:'opportuno',8424:'ordine',8429:'padre',8433:'parte',8446:'porto',8620:'roma',8632:'signor',8737:'tuttavia'}
extra='conte famiglia ex feld signora eccellentissimo ambasciatore dunque dianzi data diretta dispaccio dianzi davvero di da dal dalla degli sommamente sempre stesso stessa trenta trentuno uno ultimo ultimi venti ventuno ventidue ventitre ventiquattro venticinque ventisei ventisette ventotto ventinove volgente vostra maggio giugno nove otto numero tre tredici sei sette sedici spirato stante scorso passato corrente assai altresi anche avere a ad accordo affine anzi cenno comando consenso'.split()
V=sorted(set([x for x,_ in w.most_common(2500) if len(x)>1]+list(A.values())+extra))
ks=sorted(A); rs=[bisect.bisect_left(V,A[k]) for k in ks]
def pred(c):
    if c<=ks[0]: return rs[0]-(ks[0]-c)*(rs[1]-rs[0])/(ks[1]-ks[0]) if False else rs[0]-(ks[0]-c)*0.5*2.1
    if c>=ks[-1]: return rs[-1]+(c-ks[-1])*(rs[-1]-rs[-3])/(ks[-1]-ks[-3])
    return np.interp(c,ks,rs)
for c in [8093,8102,8131,8136,8227,8413,8704,8734,8739,8760,8904]:
    p=int(pred(c)); print(c,'~',V[min(p,len(V)-1)],'|',' '.join(V[max(0,p-18):p+18])); print()
