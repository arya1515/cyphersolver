import re
def load(fn):
    toks=[]
    for line in open(fn,encoding='utf-8'):
        if line.startswith('#'): continue
        line=re.sub(r'\[[^\]]*\]',' | ',line)
        line=line.replace('INS',' ').replace('/INS',' ')
        for t in line.split():
            if t=='|': toks.append('|'); continue
            toks.append(t.rstrip('?'))
    return toks
def all_tokens():
    out={}
    for f in ['ct_233.txt','ct_239.txt','ct_288.txt']:
        out[f]=load(f)
    return out
