import json,random,math,numpy as np,hc2,sys
cols=json.load(open(sys.argv[1]))
langs=sys.argv[2].split(',')
sym=[x['sh']+str(min(x['nd'],3)) for C in cols for x in C if x['sh']!='?']
syms=sorted(set(sym)); idx={s:i for i,s in enumerate(syms)}; S=np.array([idx[s] for s in sym])
keyc=['akt','blu','cmw','dnx','eoy','fpz','gq','hr','is']
def tf(i,k):
  r,c=divmod(i,3)
  for _ in range(k%4): r,c=c,2-r
  if k>=4: c=2-c
  return r*3+c
for lg in langs:
  arr=hc2.prep(json.load(open(f'q_{lg}.json')))
  for k in range(8):
    opts=[[ord(c)-97 for c in keyc[tf('ABCDEFGHI'.index(s[0]),k)]] for s in syms]
    best=-1e9
    for r in range(3):
      m=np.array([random.choice(o) for o in opts])
      def sc(m):
        L=m[S]; return arr[((L[:-3]*26+L[1:-2])*26+L[2:-1])*26+L[3:]].sum()
      cur=sc(m)
      for it in range(4000):
        i=random.randrange(len(syms)); old=m[i]; m[i]=random.choice(opts[i]); n=sc(m)
        T=max(0.05,3*(1-it/4000))
        if n>=cur or random.random()<math.exp((n-cur)/T): cur=n
        else: m[i]=old
      if cur>best: best=cur; bm=m.copy()
    print(lg,k,round(best/len(sym),3),''.join(chr(97+bm[idx[s]]) for s in sym)[:100])
