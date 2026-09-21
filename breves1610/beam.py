"""Beam search: each cipher sign has a candidate set of plaintext letters read off the
DECODE R2077 key image (BnF fr. 3642); the fr-1600-letters model picks the best path."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lang import lm

M = lm.load('fr-1600-letters', spaces=False)
ALL = 'abcdefghilmnopqrstuxyz'
C = {  # sign -> candidates (key reading; '*' = unknown)
 '3': 'ac', 'J': 'ao', 'x': 'aq', '8': 'a', 'b': 'bms', 'e': 'bnq', 'l': 'blx', 'u': 'c', '5': 'c',
 't': 'd', 'z': 'dp', '9': 'e', 'q': 'e', 'r': 'eg', 'ß': 'e', 'p': 'f', 'o': 'f', 'g': 'fgln', 'f': 'hnb',
 'k': 'io', 'm': 'il', 'a': 'ms', 'c': 'mn', 'd': 'mp', 'h': 'nr', 'n': 'o', 'y': 'q', 'ǂ': 're',
 'qq': 't', 'ǂǂ': 't', 's': ALL, 'pp': ALL, 'll': ALL,
}
if len(sys.argv) > 2 and sys.argv[2] == 'free':
    for k in ('y', 'a', 'd', 'c', 'b'):
        C[k] = ALL

def solve(tokens, beam=3000, pre=''):
    B = [(0.0, pre)]
    for t in tokens:
        nb = []
        for s, txt in B:
            for ch in C[t]:
                nt = txt + ch
                nb.append((M.score(nt), nt))
        nb.sort(reverse=True)
        B = nb[:beam]
    return [(round(s, 1), t[len(pre):]) for s, t in B[:8]]

RUNS = {
 'N1': ('quelepapeavec', 'b J r c J y'),
 'N2d': ('', 'qq 3 s pp b x z l c m t y qq r'),
 'S1a': ('deladifficulte', 'h z ǂǂ d a d a y c y o q t qq r ll'),
 'S2a': ('devoirestre', 'z u k a d y r f q 8 t l d z h t u t'),
}
for k, (pre, toks) in RUNS.items():
    if len(sys.argv) > 1 and sys.argv[1] not in (k, 'all'):
        continue
    toks = [t for t in toks.split() if t in C or print('skip', t)]
    print(k, solve(toks, pre=pre))
