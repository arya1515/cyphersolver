import sys,re,functools
K={}
for l in open('decode/DOC_R60_D3247_3247.txt',encoding='utf8'):
    m=re.match(r'^([\d|]+) - (.*)$',l.strip())
    if m:
        for c in m[1].split('|'): K[c]=m[2].split('|')[0]
s=sys.argv[1]
@functools.lru_cache(None)
def best(i):
    if i==len(s): return (0,'')
    opts=[]
    for n in (1,2,3):
        c=s[i:i+n]
        if len(c)<n: continue
        if n==3:
            if c in K and i+4<=len(s): r=best(i+4); opts.append((r[0],'['+K[c]+']'+r[1]))
            continue
        if c in K:
            r=best(i+n); v=K[c]; opts.append((r[0]+(0.3 if v=='<NULL>' else 0),('' if v=='<NULL>' else v)+r[1]))
    if i+2<=len(s): r=best(i+2); opts.append((r[0]+3,'?'+s[i:i+2]+'?'+r[1]))
    if i+1==len(s): r=(0,"");opts.append((3,"?"+s[i]))
    return min(opts)
print(best(0))
