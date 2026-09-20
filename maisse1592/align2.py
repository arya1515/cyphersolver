"""As align.py but each cipher value may instead be a NULL (consumes no plaintext).
A value behaves consistently: always the same letter, or always a null.
Beam search over (map, cipher index, plain index)."""
import re, unicodedata
from align import PLAIN, CT           # reuse the normalised plaintext and transcription

def search(off, ct, beam=4000, max_nulls=4):
    # state: (i, j, frozen map items, nulls frozenset)
    start=(0, off, (), ())
    states={start:0}
    best=(0,None)
    for step in range(len(ct)):
        nxt={}
        for (i,j,mp,nl),_ in states.items():
            if i!=step: continue
            g=ct[i]
            d=dict(mp); nulls=set(nl)
            # option 1: null
            if (g in nulls) or (g not in d and len(nulls)<max_nulls):
                key=(i+1,j,mp,tuple(sorted(set(nl)|{g})))
                nxt[key]=max(nxt.get(key,0), i+1)
            # option 2: letter
            if g not in nulls and j < len(PLAIN):
                ch=PLAIN[j]
                inv={v:k for k,v in d.items()}
                if (g not in d or d[g]==ch) and (ch not in inv or inv[ch]==g):
                    d2=dict(d); d2[g]=ch
                    key=(i+1,j+1,tuple(sorted(d2.items())),nl)
                    nxt[key]=max(nxt.get(key,0), i+1)
        if not nxt: break
        # keep the deepest states
        items=sorted(nxt.items(), key=lambda kv:-kv[1])[:beam]
        states=dict(items)
        for (i,j,mp,nl),_ in items[:1]:
            if i>best[0]: best=(i,(j,mp,nl,off))
    return best

res=[]
for off in range(0,len(PLAIN)-30,1):
    n,info=search(off,CT)
    res.append((n,off,info))
res.sort(key=lambda t:-t[0])
print('best with nulls allowed (max 4 null values):')
for n,off,info in res[:6]:
    print(f'  off={off:4d} placed={n:3d}/{len(CT)}  "{PLAIN[off:off+24]}"')
n,off,info=res[0]
j,mp,nl,_=info
print('\nnulls:',nl)
print('map:',dict(mp))
