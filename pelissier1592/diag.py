import re,sys,collections,beam
from beam import decode,C,MULTI
PEN_ANY=float(sys.argv[1]) if len(sys.argv)>1 else 2.5
letters='abcdefghilmnopqrstuxyz'
base={k:list(v) for k,v in C.items()}
for k,v in C.items():
    have={l for l,_ in v}
    C[k]=v+[(l,PEN_ANY) for l in letters if l not in have and v[0][0]!='' ]
cnt=collections.defaultdict(collections.Counter)
import glob
# instrument: decode, then recover per-token letters by re-decoding with trace
def decode_trace(toks,B=300):
    n=len(toks); beams={0:[(0.0,'   ','',())]}
    for i in range(n+1):
        if i not in beams: continue
        cur=sorted(beams.pop(i),key=lambda x:-x[0]); seen={}
        for b in cur:
            k=(b[1],b[2][-6:])
            if k not in seen: seen[k]=b
        cur=list(seen.values())[:B]
        if i==n: return cur[0]
        t=toks[i]; opts=[(1,C.get(t,[('['+t+']',0)]))]
        for L in (2,3):
            if i+L<=n and tuple(toks[i:i+L]) in MULTI: opts.append((L,MULTI[tuple(toks[i:i+L])]))
        for L,cands in opts:
            for sc,ctx,out,tr in cur:
                for lets,pen in cands:
                    s,c,o=beam.extend(sc,ctx,out,lets,pen,1.0)
                    beams.setdefault(i+L,[]).append((s,c,o,tr+((tuple(toks[i:i+L]),lets),)))
out=open('diag_out.txt','w',encoding='utf-8')
for f in sorted(glob.glob('t4*.txt')+glob.glob('t50r.txt')):
    for line in open(f,encoding='utf-8'):
        m=re.match(r'(C\d+[a-z]?):\s*(.*)',line)
        if not m: continue
        r=decode_trace(m.group(2).split())
        out.write(f'{f[:-4]} {m.group(1)} {r[2]}\n')
        for tk,l in r[3]:
            if len(tk)==1: cnt[tk[0]][l]+=1
for t,c in sorted(cnt.items(),key=lambda x:-sum(x[1].values())):
    tot=sum(c.values()); b=base.get(t,[('?',0)])[0][0]
    print(f'{t:5}{tot:5} key={b:3}', ' '.join(f'{l or "_"}:{n}' for l,n in c.most_common(6)))
