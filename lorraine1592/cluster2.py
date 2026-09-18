"""Cluster the deskewed, line-ordered glyphs of fr. 3621 no. 97 and emit ciphertext as cluster ids."""
import sys, math
sys.path.insert(0,'.')
from deskew import load, best_shear, lines
from cluster import mask, shifts, dist

if __name__=='__main__':
    thr=float(sys.argv[1]) if len(sys.argv)>1 else 0.16
    w,h,g,cs=load('/tmp/lor.bmp')
    s=best_shear(cs)
    ls=lines(cs,s,12)
    flat=[c for l in ls for c in l]
    print(f'shear {s} lines {len(ls)} glyphs {len(flat)}', file=sys.stderr)
    ms=[mask(c) for c in flat]; sh=[shifts(m) for m in ms]
    leaders=[]; lab=[]
    for i,m in enumerate(ms):
        best,bi=None,-1
        for j,(lm,_) in enumerate(leaders):
            d=dist(sh[i],lm)
            if best is None or d<best: best,bi=d,j
        if best is not None and best<thr: leaders[bi][1].append(i); lab.append(bi)
        else: leaders.append([m,[i]]); lab.append(len(leaders)-1)
    sizes=sorted((len(x) for _,x in leaders), reverse=True)
    print(f'clusters {len(leaders)}  top sizes {sizes[:20]}', file=sys.stderr)
    A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-*/=<>()[]{}!?@#$%^&~'
    k=0
    for l in ls:
        print(''.join(A[lab[k+i]] if lab[k+i]<len(A) else '.' for i in range(len(l)))); k+=len(l)
