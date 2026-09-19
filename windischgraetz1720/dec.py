import sys,re
def load(p):
  d={}
  for l in open(p,encoding='utf8'):
    if l.startswith('#') or not l.strip(): continue
    a,b=l.rstrip('\n').split('\t')[:2]; d[int(a)]=b
  return d
syl=load('key5017_syllabary.tsv')
try: nom=load('key5017_nomenclator.tsv')
except FileNotFoundError: nom={}
for l in open(sys.argv[1],encoding='utf8'):
  if l[0]=='#':continue
  i,c,n=l.rstrip().split('|')
  out=[]
  for x in n.split():
    k=int(x)
    out.append(syl[k] if k<=400 else '{'+nom.get(k,'?'+x)+'}')
  print(i,'|',c,'|',' '.join(out))
