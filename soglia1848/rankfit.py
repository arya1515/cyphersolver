import collections,numpy as np,bisect,sys
w=collections.Counter(open('it19.txt').read().split())
anch={8319:'imperatore',8340:'istruzione',8374:'monsignor',8422:'opportuno',8424:'ordine',8429:'padre',8433:'parte',8446:'porto',8620:'roma'}
for N in [800,1500,2500,4000,6000]:
    V=sorted(set([x for x,_ in w.most_common(N) if len(x)>1]+list(anch.values())))
    r=np.array([bisect.bisect_left(V,v) for v in anch.values()]); c=np.array(list(anch.keys()))
    b,a=np.polyfit(r,c,1); res=c-(a+b*r)
    print(N,len(V),'slope',round(b,3),'resid',np.round(res).astype(int))
