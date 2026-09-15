"""Emit docs/ctc_tw.js: a 10000-character string indexed by 4-digit code (Unihan kTaiwanTelegraph,
falling back to kMainlandTelegraph), '□' where no character."""
import csv, os
here = os.path.dirname(os.path.abspath(__file__))
tab = ['□'] * 10000
for name in ('cn.csv', 'tw.csv'):  # tw overrides cn
    for row in csv.DictReader(open(os.path.join(here, name), encoding='utf-8')):
        for code in row['code'].split():
            tab[int(code)] = row['character']
s = ''.join(tab)
open(os.path.join(here, '..', 'docs', 'ctc_tw.js'), 'w', encoding='utf-8').write(
    '// Standard Chinese telegraph code (Unihan kTaiwanTelegraph, cn fallback); index = 4-digit code\nconst CTC=Array.from(' + repr(s).replace("'", '"') + ');\n')
print(len(s), sum(c != '□' for c in s))
