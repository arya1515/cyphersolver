import re,sys
key={}
for l in open(sys.argv[1],encoding='utf8'):
    m=re.match(r'^([\w|]+) - (.+)$',l.strip())
    if m:
        for c in m.group(1).split('|'): key[c]=m.group(2)
T=[l for l in open('transcription.txt',encoding='utf8') if not l.startswith('#')]
for l in T:
    out=[]
    for t in re.findall(r'\[[^\]]*\]|\S+',l):
        if t.startswith('['): out.append(t)
        else:
            v=key.get(t.lstrip('0') if t.isdigit() and t!='0' else t)
            out.append(v if v and len(v)==1 else (f' {v} ' if v else f'<{t}>'))
    print(''.join(out))
