"""Per-record German LM score (mean log-prob per char) and '?' rate of the current decipherment: python score.py"""
import re
from decode import loadkey, decode_record
from solve import model
from parse import ORDER
m = model()
h, s = loadkey()
for r in ORDER:
    txt = ''.join(re.findall(r'\[([^\]]*)\]', decode_record(r, h, s))).lower()
    clean = re.sub(r'[^a-z]', '', txt)
    print(r, len(txt), f'{m.per_char(clean):.3f}', f'{txt.count("?")/max(1,len(txt)):.3f}')
