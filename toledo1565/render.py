"""Render transcription.txt as continuous Spanish: decoded figure runs in *italics*."""
import re, json
KEY = json.load(open('key.json', encoding='utf-8'))
K = {int(k): v for k, v in KEY['codes'].items()}
pat = re.compile(r'(?<![\w])\d{2,}(?: \d+)*')

def dec(m):
    d = m.group(0).replace(' ', '')
    return '*' + ''.join(K.get(int(d[i:i+2]), '?') for i in range(0, len(d) - 1, 2)) + '*'

out, page = [], None
for line in open('transcription.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('#'): continue
    if line.startswith('=='):
        page = line[3:].strip(); out.append(f'\n### {page}\n'); continue
    out.append(pat.sub(dec, line))
text = '\n'.join(out)
# join the manuscript's hyphenated line breaks and merge italic runs split across words
text = re.sub(r'([a-z]):?\n', r'\1\n', text)
text = text.replace('*\n*', '*\n*')
open('reading_raw.md', 'w', encoding='utf-8').write(text)
print(text)
