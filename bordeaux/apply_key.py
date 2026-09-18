import sys
key = {}
for l in open(sys.argv[1] if len(sys.argv) > 1 else 'key7537.txt', encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    t, v = l.rstrip('\n').split('\t')
    key[t] = v.rstrip('?')
sep = sys.argv[2] if len(sys.argv) > 2 else ' '
for l in open('ct2.txt', encoding='utf-8'):
    if l.startswith('#'): continue
    t = l.split(); out = []; i = 0
    while i < len(t):
        if i + 1 < len(t) and t[i] + ' ' + t[i+1] in key:
            out.append(key[t[i] + ' ' + t[i+1]]); i += 2; continue
        out.append(key.get(t[i], '[' + t[i] + ']')); i += 1
    print(sep.join(out))
