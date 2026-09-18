import glob,re,unicodedata,collections,pickle,math
txt=[]
for f in glob.glob('corpus/pg*.txt'):
    t=open(f,encoding='utf8',errors='ignore').read()
    a=t.find('*** START'); b=t.find('*** END')
    t=t[a:b]
    t=t[t.find('\n'):]
    txt.append(t)
t=' '.join(txt).lower()
t=unicodedata.normalize('NFD',t)
t=''.join(c for c in t if unicodedata.category(c)!='Mn')
t=t.replace("'",' ').replace('’',' ')
t=re.sub(r'[^a-z]+',' ',t)
t=re.sub(r' +',' ',t)
print(len(t))
open('it19.txt','w').write(t)
