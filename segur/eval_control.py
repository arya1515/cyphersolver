"""Compare the solver's BEST key from a control log with the control's true key. usage: eval_control.py N"""
import sys, ast, re
n = sys.argv[1]
klines = open(f'control{n}_key.txt', encoding='utf-8').read().split('\n')
truekey = ast.literal_eval(klines[0]); trueblk = ast.literal_eval(klines[1])   # cons -> block start
trueblk_inv = {v: k for k, v in trueblk.items()}
log = open(f'run_control{n}.log', encoding='utf-8').read()
key = ast.literal_eval(re.search(r'^KEY (.*)$', log, re.M).group(1))
blk = ast.literal_eval(re.search(r'^BLOCKS (.*)$', log, re.M).group(1))
# letter symbols weighted by occurrence in the control ciphertext
from collections import Counter
toks = []
for line in open(f'control{n}.txt', encoding='utf-8'):
    if line.startswith('#'): continue
    line = re.sub(r'\[[^\]]*\]', ' ', line)
    toks += [t for t in line.split() if t.isdigit()]
c = Counter(int(t) for t in toks)
ok = tot = 0
for num, cnt in c.items():
    if num in truekey:
        tot += cnt; ok += cnt * (truekey[num] == key.get(num, '?'))
print(f'letter tokens right {ok}/{tot} = {ok/tot:.1%}')
bok = sum(1 for b, cns in blk.items() if trueblk_inv.get(b) == cns)
print(f'blocks right {bok}/12; true', {v: k for k, v in trueblk.items()}, 'found', blk)
print('scores', re.findall(r'^\d+ (-[\d.]+)$', log, re.M))
