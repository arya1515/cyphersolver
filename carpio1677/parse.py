import re,glob,collections
def load(f):
    out=[];cur=None
    for line in open(f,encoding='utf8',errors='replace'):
        if line.startswith('#IMAGE NAME'): continue
        if line.startswith('#') : continue
        line=re.sub(r'<[^>]*>','',line)
        for t in line.split('.'):
            t=t.strip()
            if not t: continue
            s=t.replace(' ','').replace('?','')
            if not s: continue
            if '+' in s: s=s.replace('+','')+'*'
            out.append(s)
    return out
if __name__=='__main__':
    C=collections.Counter()
    for f in sorted(glob.glob('img/DOC*.txt')):
        t=load(f); C.update(t); print(f,len(t))
    print(C.most_common(120))
