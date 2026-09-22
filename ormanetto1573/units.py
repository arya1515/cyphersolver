from tok import load
import collections,os
MODE=os.environ.get('UMODE','pair')
def units(p):
    out=[];i=0
    while i<len(p):
        d,dot,u=p[i]
        if MODE=='flat':
            out.append(d+('.' if dot else ''));i+=1;continue
        if MODE=='full':
            out.append(d+('.' if dot else '')+('_' if u else ''));i+=1;continue
        if MODE=='plain':
            out.append(d);i+=1;continue
        if d=='0' and dot and i+1<len(p) and MODE in('pair','dot0'):
            out.append('0'+p[i+1][0]+('.' if p[i+1][1] else ''));i+=2;continue
        if MODE=='pair' and i+1<len(p) and p[i+1][0]=='1' and d in '245':
            out.append(d+'1');i+=2;continue
        out.append(d+('.' if dot else ''));i+=1
    return out
