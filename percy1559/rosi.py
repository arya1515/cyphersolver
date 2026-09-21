import re, collections, itertools
exec(open('pattern_search.py').read().split("txt=")[0])
txt=open('../burghley1559/sadler1.txt',encoding='utf-8',errors='ignore').read()+open('../throckmorton/sources/forbes1.txt',encoding='utf-8',errors='ignore').read().replace('ſ','s')
cnt=collections.Counter(re.findall(r'[a-z]+',txt.lower()))
for n in "knox prior lord laird lairde whitlaw kirkaldy grange james hume dowager congregation croftes merse tivdale".split(): cnt[n]+=100
vocab=set(w for w,c in cnt.items() if c>=3)
words=[w for k in lines.values() for w in k]
shapes=sorted({s[0] for w in words for s in w if s[0] in 'ABCDEFGIh'})
print(shapes)
def mk(s): return {'':0,'_':1,':':2,'.':2}.get(s[1:],None) if s[0] in 'ABCDEFGIh' and s[1:] in ('','_',':','.') else None
# precompile regex per candidate vocab length
bylen=collections.defaultdict(list)
for w in vocab: bylen[len(w)].append(w)
res=[]
for alph in ['abcdefghiklmnopqrstuwxyz','abcdefghijklmnopqrstuvwxyz']:
  cells=[alph[i:i+3] for i in range(0,len(alph),3)]
  for perm in itertools.permutations(range(len(cells)),len(shapes)):
    for mp in itertools.permutations(range(3)):
      sc=0;dec=[]
      for w in words:
        s=''
        for t in w:
          m=mk(t)
          if m is None: s+='.';continue
          c=cells[perm[shapes.index(t[0])]]; i=mp[m]
          s+= c[i] if i<len(c) else '#'
        dec.append(s)
      # quick score: words fully known that are in vocab
      for s in dec:
        if '.' not in s and s in vocab: sc+=len(s)
      if sc>=8: res.append((sc,alph[:3]=='abc' and len(alph),perm,mp,' | '.join(dec)))
res.sort(reverse=True)
for r in res[:40]: print(r)
