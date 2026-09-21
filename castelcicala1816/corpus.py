import re,glob,collections,json
OTHER={'R9586','R9588'}
def parse(f):
    toks=[]
    for l in open(f,encoding='utf-8'):
        if l.startswith(('#','P:','C:')) or not l.strip(): continue
        for t in l.split():
            m=re.match(r'^([0-9?]+)',t)
            if m and re.search(r'\d',m.group(1)): toks.append(m.group(1))
    return toks
C={}
for f in sorted(glob.glob('transcripts/R*.txt')):
    import os; r=os.path.basename(f)[:-4]
    C[r]=parse(f)
if __name__=='__main__':
    cnt=collections.Counter()
    for r,t in C.items():
        if r in OTHER: continue
        cnt.update(x for x in t if '?' not in x)
        print(r,len(t),sum('?' in x for x in t))
    print('tokens',sum(cnt.values()),'types',len(cnt))
    big=[x for x in cnt if int(x)>2460]; print('over2460',len(big),big[:30])
    print(cnt.most_common(60))
