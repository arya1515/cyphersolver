"""Tokenise R72: pairs, or 3 digits + mark '7' (nomenclator). Prints code counts."""
import re, collections
raw = open('decode/DOC_R72_D1824_1824.txt', encoding='utf8').read()
body = raw.split('#IMAGE NAME: 1.png')[-1].split('<CLEARTEXT')[0]
d = []
for t in body.split():
    t = t.replace('_', '').rstrip(',.')
    if not t or t == '|': continue
    t = t.split('/')[0].rstrip('?')
    if t in ('t', '+'): t = '7'
    d.extend(list(t) if t.isdigit() else ['?'])
def tokens():
    out = []; i = 0
    while i < len(d):
        if i + 3 < len(d) and d[i+3] == '7' and d[i+1] != '7' and d[i] != '7':
            out.append(''.join(d[i:i+3]) + '^'); i += 4
        else:
            out.append(''.join(d[i:i+2])); i += 2
    return out
T = tokens()
if __name__ == '__main__':
    c = collections.Counter(T)
    print(len(T)); print(sorted(c.items(), key=lambda x: -x[1]))
