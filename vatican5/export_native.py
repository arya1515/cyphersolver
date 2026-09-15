"""Export data for the native (C#) solver:
  lm5.bin   : float32 array [22^4 contexts][21 letters] of log P(letter | 4 previous letters), index 21 = start pad
  cipher.txt: one run per line, tokens separated by spaces (digit + optional '^' dot flag)
"""
import struct, pathlib, itertools, array
from solver6 import LM
from parse5 import load, digit_stream
HERE = pathlib.Path(__file__).parent
ALPHA = 'abcdefghilmnopqrstuz'   # 20 letters + we add index 20 = 'v'? no: v->u already. 20 letters.
L = len(ALPHA); PAD = L                          # pad index 20 -> total 21 symbols in context
lm = LM()
out = array.array('f')
ctx_syms = ALPHA + '#'
n = 0
for h in itertools.product(range(L + 1), repeat=4):
    # history string: drop pads (pads only at the start)
    hs = ''.join(ALPHA[i] for i in h if i != PAD)
    for c in range(L):
        out.append(lm.lp(hs, ALPHA[c]))
    n += 1
(HERE / 'lm5.bin').write_bytes(out.tobytes())
print('contexts', n, 'floats', len(out))
with open(HERE / 'cipher.txt', 'w') as f:
    for r in digit_stream(load()):
        f.write(' '.join((t[0] + ('^' if '^' in t else '')) for t in r) + '\n')
print('runs written')
