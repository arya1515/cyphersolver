import re,glob,collections,math,json,sys
lang,pat=sys.argv[1],sys.argv[2]
c=collections.Counter()
for f in glob.glob(pat):
    t=open(f,encoding='utf8',errors='ignore').read().lower()
    t=t.translate(str.maketrans('àâäáéèêëíìîïóòôöúùûüçñ','aaaaeeeeiiiioooouuuucn'))
    t=re.sub('[^a-z]','',t)
    for i in range(len(t)-3): c[t[i:i+4]]+=1
T=sum(c.values()); json.dump({k:round(math.log10(v/T),3) for k,v in c.items() if v>1},open(f'q_{lang}.json','w'))
print(lang,T,len(c))
