import itertools,sys
def solve(signs,plain):
    types=sorted(set(signs))
    res=[]
    for k in range(0,4):
        for nulls in itertools.combinations(types,k):
            s=[x for x in signs if x not in nulls]
            if len(s)!=len(plain): continue
            m={};ok=True
            for a,b in zip(s,plain):
                if m.setdefault(a,b)!=b: ok=False;break
            if ok: res.append((nulls,m))
    return res
