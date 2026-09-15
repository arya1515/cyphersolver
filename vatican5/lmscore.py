"""Score a no-space letter string with the same 5-gram LM as lm5.bin (via solver6.LM). usage: lmscore.py file"""
import sys, re
from solver6 import LM
lm = LM()
txt = open(sys.argv[1], encoding='utf8', errors='replace').read()
if 'PLAINTEXT:' in txt: txt = txt.split('PLAINTEXT:')[1]
s = re.sub(r'[^a-z]', '', txt.lower().replace('v', 'u').replace('j', 'i').replace('k', 'c').replace('y', 'i').replace('w', 'u').replace('x', 's'))
tot, hist = 0.0, ''
for ch in s:
    tot += lm.lp(hist, ch); hist = (hist + ch)[-4:]
print(f'{sys.argv[1]}: chars={len(s)} total={tot:.1f} nats/char={tot/len(s):.3f}')
