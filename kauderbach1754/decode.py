import json,re,sys,math,collections
K=json.load(open(sys.argv[1])) if len(sys.argv)>1 and sys.argv[1].endswith(".json") else {}
D=json.load(open('pairs.json'))
P=collections.Counter(t for f,tk in D for t in tk if not t.startswith('*'))
tot=sum(P.values()); lp={k:math.log(v/tot) for k,v in P.items()}; floor=math.log(0.3/tot); pen=6.0
def align1(s):
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
  return toks[::-1]
def dec_file(f,show=False):
  t=open(f,encoding='utf-8-sig').read(); t=re.sub(r'#.*','',t)
  parts=re.split(r'(<CLEARTEXT[^>]*>)',t); out=[]
  for p in parts:
    if p.startswith('<CLEARTEXT'):
      out.append('['+p[13:-1].strip()+']'); continue
    for chunk in re.split(r'[,%]',p):
      d=re.sub(r'[^0-9]','',chunk).replace('5','').replace('8','')
      if not d: continue
      tk=align1(d)
      out.append(''.join((K.get(x,'<'+x+'>')+('·' if show else '')) if not x.startswith('*') else '{'+x[1:]+'}' for x in tk))
  return ' '.join(out)
if __name__=='__main__':
  for f in sys.argv[2:]:
    print('=====',f); print(dec_file(f))
