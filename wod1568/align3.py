import sys,itertools
MAIN="g x ob r3 Z pm x x x2 f x2 Z g D x2 e XX 3 x zl x ob x3 x2 x x2 Z zl o d pm g x ob".split()
TAIL="o Z D x2 zl".split()
P="andsayshemustneidishaifitbeonmeinisoruthir"[::-1]
def solve(C,P,maxnull,maxmulti,maxL=2):
    out=[]
    def go(i,j,m,mu,nu):
        if len(out)>50:return
        if i==len(C):
            if j==len(P): out.append(dict(m))
            return
        s=C[i]
        if s in m:
            v=m[s]
            if P.startswith(v,j): go(i+1,j+len(v),m,mu,nu)
            return
        for L in range(0,maxL+1):
            if L==0 and nu>=maxnull: continue
            if L>1 and mu>=maxmulti: continue
            if j+L>len(P): break
            m[s]=P[j:j+L]; go(i+1,j+L,m,mu+(L>1),nu+(L==0)); del m[s]
    go(0,0,{},0,0); return out
if __name__=="__main__":
   for C,name in ((MAIN,'main'),(MAIN+TAIL,'all')):
    for a in range(len(P)):
      for b in range(a+8,len(P)+1):
        r=solve(C,P[a:b],4,3)
        if r: print(name,P[a:b],r[0])
  