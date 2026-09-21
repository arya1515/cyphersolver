import re,sys
L="A B C D E F G H I K L M N O P Q R S T V W X Y Z".split()
k={}
for i,c in enumerate(L): k[24-i]=c; k[36-i if i<24 else 0]=c
# row values from Mirka's table: A=24/36 ... Z=1/37 (first column descends 24..1 skipping, second 36..13 then 48..37)
k={}
t=[("A",24,36),("B",12,48),("C",23,35),("D",11,47),("E",22,34),("F",10,46),("G",21,33),("H",9,45),("I",20,32),("K",8,44),("L",19,31),("M",7,43),("N",18,30),("O",6,42),("P",17,29),("Q",5,41),("R",16,28),("S",4,40),("T",15,27),("V",3,39),("W",14,26),("X",2,38),("Y",13,25),("Z",1,37)]
for c,a,b in t: k[a]=c;k[b]=c
codes={52:"affaire",54:"Althann",85:"der/dem",86:"die",99:"[Engländer?]",103:"[Emp..?]",121:"geheim",128:"Graf",135:"hat",145:"ich",151:"[K..?]",152:"Kayser",167:"[Micosch?]",191:"[Ostendische Compagnie]",195:"[Pentenrieder]",197:"Plan",198:"Prinz",213:"[Starhemberg?]"}
for line in open('ct.txt',encoding='utf8'):
  if line.startswith('#'):continue
  pg,body=line.split('|',1); out=[]
  for tok in re.split(r'(\[[^\]]*\])',body):
    if tok.startswith('['): out.append(tok[1:-1]); continue
    w=''
    for n in map(int,tok.split()):
      if n<=48: w+=k[n]
      else:
        if w: out.append(w); w=''
        out.append('«%s»'%codes.get(n,str(n)))
    if w: out.append(w)
  print(pg.strip()+':',' '.join(out))
