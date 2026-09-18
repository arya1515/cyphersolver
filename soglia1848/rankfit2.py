import collections,numpy as np,bisect
w=collections.Counter(open('it19.txt').read().split())
firm={8319:'imperatore',8340:'istruzione',8374:'monsignor',8422:'opportuno',8424:'ordine',8429:'padre',8433:'parte',8446:'porto',8620:'roma'}
new={8110:'col',8116:'colonia',8120:'come',8122:'cotesta',8211:'e',8247:'foglio',8310:'guerra',8346:'lontano',8737:'tuttavia',8632:'signor'}
V=sorted(set([x for x,_ in w.most_common(1500) if len(x)>1]+list(firm.values())+list(new.values())))
def rk(x): return bisect.bisect_left(V,x)
c=np.array(list(firm)); r=np.array([rk(v) for v in firm.values()])
b,a=np.polyfit(r,c,1)
print('fit on firm: slope',b)
for k,v in sorted(new.items()): print(k,v,'pred',round(a+b*rk(v)),'resid',round(k-(a+b*rk(v))))
