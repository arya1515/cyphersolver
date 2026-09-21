"""Decrypt DECODE R72 (SofPe transcription, DOC_R72_D1824) with Lasry's reconstructed key (DOC_R72_D3190).
Transcription gives single digits; '7' after three digits is the nomenclator mark (Lasry's '^').
Parsing is a DP: 2-digit letter codes (second digit even) or 3 digits + mark; unknown tokens cost 1."""
import re, sys
key = {}
for l in open('decode/DOC_R72_D3190_3190.txt', encoding='utf8'):
    m = re.match(r'^([\d|]+)(\+?)\s+- (.+)$', l.strip())
    if m:
        for c in m.group(1).split('|'):
            key[c + ('^' if m.group(2) else '')] = m.group(3).split('|')[0]
key['744^'] = key.pop('744', 'egina')
raw = open('decode/DOC_R72_D1824_1824.txt', encoding='utf8').read()
body = raw.split('#IMAGE NAME: 1.png')[-1].split('<CLEARTEXT')[0]
toks = []
for t in body.split():
    t = t.replace('_', '').rstrip(',.')
    if not t or t == '|': continue
    t = t.split('/')[0].rstrip('?')   # take the transcriber's first reading
    if t in ('t', '+'): t = '7'       # 't/+' is the mark
    toks.extend(list(t) if t.isdigit() else ['?'])
n = len(toks); INF = 1e9
best = [INF]*(n+1); back = [None]*(n+1); best[0] = 0
for i in range(n):
    if best[i] >= INF: continue
    opts = []
    if i+4 <= n and toks[i+3] == '7':
        c = ''.join(toks[i:i+3]) + '^'
        opts.append((4, (c, key.get(c, '<%s>' % c)), 0 if c in key else 0.6))
    if i+2 <= n:
        c = ''.join(toks[i:i+2])
        opts.append((2, (c, key.get(c, '[%s]' % c)), 0 if c in key else 1))
    opts.append((1, (toks[i], '{%s}' % toks[i]), 1.5))
    for k, s, cost in opts:
        if best[i] + cost < best[i+k]:
            best[i+k] = best[i] + cost; back[i+k] = (i, s)
out = []; j = n
while j: i, s = back[j]; out.append(s); j = i
out.reverse()
import json; json.dump([list(o) for o in out],open('r72_parsed.json','w'))
print(len(toks), 'digits,', len(out), 'tokens, cost', best[n])
out = [o[1] for o in out]
print(' '.join(o if len(o) == 1 else ' '+o+' ' for o in out).replace('   ', ' '))
