import sys,re,json,math,collections
Q=json.load(open('../richelieu/fr_quadgrams.json'))
T3=collections.Counter()
for k,v in Q.items(): T3[k[:3]]+=v
def lp(q):
    v=Q.get(q)
    if v: return math.log10(v/T3[q[:3]])
    return math.log10(0.3/(T3.get(q[:3],0)+50))
C={}; MULTI={}
def parse(spec):
    out=[]
    for i,x in enumerate(spec.split(',')):
        x=x.strip(); pen=0 if i==0 else 1.0
        if '!' in x: x,p=x.split('!'); pen=float(p)
        out.append((x.replace('_',''),pen))
    return out
for line in open('cands.txt',encoding='utf-8'):
    if line.startswith('//'): continue
    line=line.split(' //')[0].strip()
    if not line: continue
    tok,spec=line.split(None,1)
    if '+' in tok and len(tok)>1: MULTI[tuple(tok.split('+'))]=parse(spec)
    else: C[tok]=parse(spec)
def extend(sc,ctx,out,lets,pen,PEN):
    s=sc-pen*PEN; c=ctx; o=out
    for ch in lets:
        if not ch.isalpha(): o+=ch; continue
        s+=lp(c+ch) if c.strip() else 0; c=(c+ch)[-3:]; o+=ch
    return s,c,o
def decode(toks,B=300,PEN=1.0,ret_all=False):
    n=len(toks)
    beams={0:[(0.0,'   ','')]}
    for i in range(n+1):
        if i not in beams: continue
        cur=sorted(beams.pop(i),key=lambda x:-x[0])
        # dedupe
        seen={}; 
        for b in cur:
            k=(b[1],b[2][-6:])
            if k not in seen: seen[k]=b
        cur=list(seen.values())[:B]
        if i==n: return cur[0]
        t=toks[i]
        opts=[(1,C.get(t,[('['+t+']',0)]))]
        for L in (2,3):
            if i+L<=n and tuple(toks[i:i+L]) in MULTI: opts.append((L,MULTI[tuple(toks[i:i+L])]))
        for L,cands in opts:
            for sc,ctx,out in cur:
                for lets,pen in cands:
                    beams.setdefault(i+L,[]).append(extend(sc,ctx,out,lets,pen,PEN))
if __name__=='__main__':
  for f in sys.argv[1].split(','):
    for line in open(f,encoding='utf-8'):
      m=re.match(r'(C\d+[a-z]?):\s*(.*)',line)
      if m: print(m.group(1), decode(m.group(2).split())[2])
