from solve import load_doc, norm_plain

def simulate(C,P,i,j,mp,limit=40):
    """Count consistent letters ahead without modifying mp."""
    local=dict(mp); good=0; bad=0
    while j<len(P) and i+2<=len(C) and (good+bad)<limit:
        c=C[i:i+2]; l=P[j]
        t=local.get(c)
        if t is None: local[c]=l
        elif t==l: good+=1
        else:
            bad+=1
            if bad>3: break
        i+=2; j+=1
    return good-4*bad

def walk(C,P,limit=40):
    mp={}; i=j=0; ops=[]
    while j<len(P) and i+2<=len(C):
        c=C[i:i+2]; l=P[j]; t=mp.get(c)
        if t is None or t==l:
            if t is None: mp[c]=l
            ops.append(('S',c,l)); i+=2; j+=1; continue
        # conflict: try repairs
        cands=[]
        # a) drop one digit before this letter (transcriber inserted a digit)
        cands.append(('X1', i+1, j, ('X',C[i:i+1],'')))
        # b) this letter's code is 3 digits (transcriber dropped/added)
        cands.append(('X3', i+3, j+1, ('X',C[i:i+3],l)))
        # c) null: these 2 digits encode nothing
        cands.append(('N', i+2, j, ('N',c,'')))
        # d) crib has a letter the cipher lacks
        cands.append(('D', i, j+1, ('D','',l)))
        # e) force: accept and re-map (transcription error made a valid-looking code)
        cands.append(('F', i+2, j+1, ('F',c,l)))
        best=None
        for name,ni,nj,op in cands:
            m2=dict(mp)
            if name=='F': m2[c]=l
            s=simulate(C,P,ni,nj,m2,limit)
            if name=='F': s-=3
            if name=='D': s-=1
            if best is None or s>best[0]: best=(s,ni,nj,op,name)
        s,ni,nj,op,name=best
        if name=='F': mp[c]=l
        ops.append(op); i,j=ni,nj
    return mp,ops
