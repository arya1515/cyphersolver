import sys
from parse5 import load, digit_stream
m = {'3': 'i', '4': 'o', '5': 'a', '6': 'u', '8': 'e'}
runs = digit_stream(load(), keep_marks=True)
out = []
for r in runs:
    s = ''
    for t in r:
        ch = m.get(t[0], t[0])
        if '^' in t: ch = ch.upper() if ch.isalpha() else ch + '\u0307'
        s += ch
    out.append(s)
txt = '\n\n'.join(out)
open('vowelview.txt', 'w', encoding='utf8').write(txt)
print(txt[:1500])
