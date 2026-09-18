"""Cluster the segmented glyphs of fr. 3621 no. 97 by shape and emit the ciphertext as cluster ids.
Shape metric as calibrated for sormano1529: blurred binary mask, cosine distance, shift-tolerant."""
import sys, math, json
sys.path.insert(0,'.')
from glyphs import read_bmp
from lines import run
from stitch import stitch
from glyphs2 import merge_overlaps
N=12

def mask(c):
    cw=c['x1']-c['x0']+1; ch=c['y1']-c['y0']+1
    a=[[0.0]*N for _ in range(N)]
    for (x,y) in c['px']:
        a[min(N-1,(y-c['y0'])*N//ch)][min(N-1,(x-c['x0'])*N//cw)]=1.0
    b=[[0.0]*N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            s=0.0;k=0
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<N and 0<=xx<N: s+=a[yy][xx];k+=1
            b[y][x]=s/k
    v=[b[y][x] for y in range(N) for x in range(N)]
    n=math.sqrt(sum(t*t for t in v)) or 1.0
    return [t/n for t in v]

def shifts(v):
    out=[]
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            q=[0.0]*(N*N)
            for i in range(N):
                for j in range(N):
                    si,sj=i-dy,j-dx
                    q[i*N+j]=v[si*N+sj] if 0<=si<N and 0<=sj<N else 0.0
            n=math.sqrt(sum(t*t for t in q)) or 1.0
            out.append([t/n for t in q])
    return out

def dist(sa,vb):
    return min(1.0-sum(p*q for p,q in zip(va,vb)) for va in sa)

if __name__=='__main__':
    thr=float(sys.argv[1]) if len(sys.argv)>1 else 0.30
    w,h,g,cs,strips=run('/tmp/lor.bmp')
    act=stitch(strips)
    seq=[]
    for a in sorted(act,key=lambda a:a['y']):
        gl=sorted(a['g'],key=lambda c:c['x0']); gl=merge_overlaps(gl,frac=0.6)
        gl=[c for c in gl if c['n']>=45]
        if gl: seq.append(gl)
    flat=[c for l in seq for c in l]
    print('lines',len(seq),'glyphs',len(flat), file=sys.stderr)
    ms=[mask(c) for c in flat]; sh=[shifts(m) for m in ms]
    leaders=[]; lab=[]
    for i,m in enumerate(ms):
        best,bi=None,-1
        for j,(lm,_) in enumerate(leaders):
            d=dist(sh[i],lm)
            if best is None or d<best: best,bi=d,j
        if best is not None and best<thr:
            leaders[bi][1].append(i); lab.append(bi)
        else:
            leaders.append([ms[i],[i]]); lab.append(len(leaders)-1)
    print(f'clusters {len(leaders)} at thr={thr}', file=sys.stderr)
    sizes=sorted((len(m) for _,m in leaders), reverse=True)
    print('cluster sizes', sizes[:35], file=sys.stderr)
    A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-*/=<>()[]{}!?@#$%^&~'
    k=0; out=[]
    for l in seq:
        row=''.join(A[lab[k+i]] if lab[k+i]<len(A) else '.' for i in range(len(l)))
        out.append(row); k+=len(l)
    print('\n'.join(out))
