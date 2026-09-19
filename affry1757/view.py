import json,sys,re
def load(k):
    L={}
    cur=None
    for line in open(f'cipher_{k}.txt'):
        if line.startswith('#'): cur=line[2:].strip()
        else: L[cur]=fix([int(x) for x in line.split()])
    return L
def fix(g):
    import json,os
    k=json.load(open('key_M.json',encoding='utf8')) if os.path.exists('key_M.json') else {}
    out=[]
    for x in g:
        if x<=1199: out.append(x); continue
        s=str(x);best=None
        for i in range(1,len(s)):
            a,b=s[:i],s[i:]
            if a[0]=='0' or b[0]=='0' or int(a)>1199 or int(b)>1199: continue
            sc=(a in k)+(b in k)
            if best is None or sc>best[0]: best=(sc,int(a),int(b))
        out+= [best[1],best[2]] if best and best[0]>=1 else [x]
    return out
def show(k,rec,a=0,b=None,width=12):
    key={int(x):v for x,v in json.load(open(f'key_{k}.json',encoding='utf8')).items()}
    g=load(k)[rec][a:b]
    for i in range(0,len(g),width):
        seg=g[i:i+width]
        print('%4d '%(a+i)+' '.join('%-7s'%x for x in seg))
        print('     '+' '.join('%-7s'%key.get(x,'.')[:7] for x in seg))
def plain(k,rec):
    key={int(x):v for x,v in json.load(open(f'key_{k}.json',encoding='utf8')).items()}
    return ' '.join(key.get(x,'[%d]'%x) for x in load(k)[rec])
if __name__=='__main__':
    k,rec=sys.argv[1],sys.argv[2]; a=int(sys.argv[3]) if len(sys.argv)>3 else 0; b=int(sys.argv[4]) if len(sys.argv)>4 else None
    show(k,rec,a,b)
