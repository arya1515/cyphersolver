# Apply Lasry's SP106-3 key (DECODE R932 DOC D3079) to the raw FL transcription (D2358), independently of his plaintext.
import re
key = {}
for line in open('goring1645/decode/DOC_D3079_3079.txt', encoding='utf-8'):
    m = re.match(r'^([\d|]+) - (\S+)', line.strip())
    if m:
        for n in m.group(1).split('|'): key[int(n)] = m.group(2)
raw = open('goring1645/decode/DOC_D2358_2358.txt', encoding='utf-8').read()
for page in raw.split('#IMAGE NAME: ')[2:]:
    name, body = page.split('\n', 1)
    body = '\n'.join(l for l in body.splitlines() if not l.startswith('#'))
    toks = re.sub(r'(?<=\S) (?=\S)', '', body.replace('^', '')).replace('\n', '.').split('.')
    out = []
    for t in toks:
        t = t.strip()
        if not t: continue
        if t.isdigit():
            n = int(t); out.append(key.get(n, '_' if 60 <= n <= 79 else f'<{n}>'))
        else: out.append(f'[{t}]')
    print(name, ' '.join(out).replace(' ', '').replace('_', ' '), '\n')
