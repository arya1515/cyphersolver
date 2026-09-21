import re,json,sys,collections
seq=json.load(open('seq.json'))
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
    return pt.replace('u/v','v').replace('u|v','v')
def render(i,w=24):
    l=''.join(tok(c,p) for _,c,p in seq[max(0,i-w):i]); r=''.join(tok(c,p) for _,c,p in seq[i+1:i+1+w])
    return l[-60:],r[:60]
idx=collections.defaultdict(list)
for i,(it,ct,pt) in enumerate(seq):
    if re.fullmatch(r'1\d{3}',ct) and ct not in extra: idx[ct].append(i)
targets=sys.argv[1:] or sorted(idx,key=lambda g:-len(idx[g]))
n=int(__import__('os').environ.get('N','4'))
for g in targets:
    print('==',g,len(idx[g]))
    for i in idx[g][:n]:
        l,r=render(i); print('  %2d %60s [%s] %s'%(seq[i][0],l,g,r))
