import re
raw = open(r'c:\Users\dbour\cypher\colbert\louisxiv0.htm', 'rb').read().decode('utf-8', 'ignore')
out = []
for m in re.finditer(r'Colbert\s+(\d+(?:bis)?)\s*\(\s*<A HREF="([^"]+)"', raw, re.I):
    out.append(f'{m.group(1)}\t{m.group(2)}')
open(r'c:\Users\dbour\cypher\colbert\arks.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
