# Variant scans: suffix rules (parse right-to-left) and prefix rules with 1xx three-digit tokens.
import sys,itertools,time,seg
def parse_suffix(u,U,letters='null'):
    toks=[]
    for x in u:
        if x[0] in '%:+-': toks.append('#'+x)
        elif x.isalpha():
            if letters=='null': continue
            toks.append('L'+x)
        else:
            r=x[::-1]; out=[]; i=0
            while i<len(r):
                if r[i] in U and i+1<len(r): out.append(r[i:i+2][::-1]); i+=2
                else: out.append(r[i]); i+=1
            toks+=out[::-1]
    return toks
def dangling_suffix(u,U):
    d=0
    for x in u:
        if x.isdigit() and x[0] in U and len(parse_suffix([x],U)[0])==1: d+=1
    return d
if __name__=='__main__':
    src,mode=sys.argv[1],sys.argv[2]; u=seg.units(open(src).read()); t0=time.time(); res=[]
    for k in range(0,11):
        for S in itertools.combinations('0123456789',k):
            S=set(S)
            if mode=='suffix':
                if dangling_suffix(u,S)>3: continue
                toks=parse_suffix(u,S)
            else:
                if seg.dangling(u,S)>3: continue
                toks=seg.parse(u,S,set(),True)
            nd=len(set(t for t in toks if t[0]!='#'))
            if not 12<=nd<=90: continue
            r=seg.solve(toks,2,40000)
            if r is None: continue
            res.append((r[0],''.join(sorted(S)),nd,r[4],r[1]))
            print(f'{r[0]:.3f} {mode}={"".join(sorted(S)) or "-"} nsym={nd} win={r[4]} {r[1][:70]}',flush=True)
    res.sort(reverse=True); print('TOP')
    for r in res[:15]: print(r)
    print('time',time.time()-t0)
