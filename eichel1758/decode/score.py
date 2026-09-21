import re,glob,sys
ct=[]
for l in open('DOC_R595_D1900_1900.txt',encoding='utf-8-sig'):
    if l[0].isdigit():
        for t in re.split(r'\.\s|\s\s',l):
            d=re.sub(r'\D','',t)
            if d: ct.append(int(d))
def load(f):
    k={}
    for l in open(f,encoding='utf-8-sig',errors='replace'):
        l=l.strip()
        m=re.match(r'^([\d|]+)\s*[-–=]\s*(.+)$',l) or re.match(r'^(.+?)\s*[-–=]\s*([\d|]+)$',l)
        if not m: continue
        a,b=m.groups()
        if not re.fullmatch(r'[\d|]+',a): a,b=b,a
        for n in a.split('|'):
            if n: k.setdefault(int(n),b)
    return k
if __name__=='__main__':
  for f in sorted(glob.glob('DOC_R*.txt')):
    if '595' in f: continue
    k=load(f)
    if not k: print(f,'unparsed'); continue
    cov=sum(c in k for c in ct)/len(ct)
    print(f,len(k),min(k),max(k),f'{cov:.2f}')
