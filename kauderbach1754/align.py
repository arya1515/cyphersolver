import real,collections,math
def realign(S,iters=4,pen=6.0):
  # pair model
  P=collections.Counter(s[i:i+2] for s in S for i in range(0,len(s)-1,2))
  for it in range(iters):
    tot=sum(P.values()); lp={k:math.log((v+0.5)/(tot+50)) for k,v in P.items()}; floor=math.log(0.5/(tot+50))
    out=[]
    for s in S:
      # DP over positions: state = next pair starts at i; transitions: take pair (2), or skip 1 digit (penalty)
      n=len(s); best=[-1e18]*(n+1); bp=[None]*(n+1); best[0]=0
      for i in range(n):
        if best[i]<-1e17: continue
        if i+2<=n:
          v=best[i]+lp.get(s[i:i+2],floor)
          if v>best[i+2]: best[i+2]=v; bp[i+2]=(i,'P')
        v=best[i]-pen
        if v>best[i+1]: best[i+1]=v; bp[i+1]=(i,'S')
      i=n; toks=[]
      while i>0:
        j,t=bp[i]; toks.append(s[j:i] if t=='P' else '*'+s[j:i]); i=j
      out.append(toks[::-1])
    P=collections.Counter(t for tk in out for t in tk if not t.startswith('*'))
  return out
if __name__=='__main__':
  L=real.load(); S=[s for f,s in L]
  out=realign(S)
  sk=collections.Counter(t for tk in out for t in tk if t.startswith('*'))
  print(sum(sk.values()),sk.most_common(12), sum(len(t) for t in out))
  P=collections.Counter(t for tk in out for t in tk if not t.startswith('*'))
  print(len(P),P.most_common(70))
  import json; json.dump([[f,tk] for (f,_),tk in zip(L,out)],open('pairs.json','w'))
