import re,json,sys,collections
seq=json.load(open('seq.json',encoding='utf-8'))
known={}
for ln in open('decode/keep/lasry_key_S364.txt',encoding='utf-8',errors='replace'):
    m=re.match(r'^([\d|]+)\s*-\s*(.+)$',ln.strip())
    if m:
        for c in m.group(1).split('|'): known[c]=m.group(2).strip()
extra={}
try:
    for ln in open('key_extra.txt',encoding='utf-8'):
        m=re.match(r'^(\d+)\s*=\s*(\S+)',ln.strip())
        if m: extra[m.group(1)]=m.group(2)
except IOError: pass
def tok(ct,pt):
    if ct in extra: return '{'+extra[ct]+'}'
    if pt=='_': return ' '
    if not pt or pt.endswith('?'): return '?'
    if pt.startswith('<'): return '{'+ct+'}'
    return pt.replace('u/v','v').replace('quale/mentre','quale').replace('possa/parlare','possa')
def render(i,w=22):
    l=''.join(tok(c,p) for _,c,p in seq[max(0,i-w):i])
    r=''.join(tok(c,p) for _,c,p in seq[i+1:i+1+w])
    return l[-70:],r[:70]
idx=collections.defaultdict(list)
for i,(cat,ct,pt) in enumerate(seq):
    if re.fullmatch(r'4\d{3}',ct) and ct not in known and ct not in extra: idx[ct].append(i)
order=sorted(idx,key=lambda g:-len(idx[g]))
targets=sys.argv[1:] if len(sys.argv)>1 else order
for g in targets:
    if g not in idx: continue
    print('=== %s  (%d)'%(g,len(idx[g])))
    for i in idx[g][:6]:
        l,r=render(i)
        print('   %s >>%s<< %s'%(l,g,r))
