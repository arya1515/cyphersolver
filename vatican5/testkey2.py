"""Score a fixed key (Meister p.176-177 no.2, Poggio) with the lattice LM, and print a sample decode."""
import sys
from solver6 import LM, Solver, UNUSED
from parse5 import load, digit_stream

KEY2 = {'3': 'a', '5': 'e', '7': 'i', '9': 'o', '0': 'u', '8': 'c', '2': 'l', '4': 'n', '6': 'r', '1': 'et',
        '21': 'ca', '22': 'ce', '23': 'ci', '24': 'co', '88': 'ra', '89': 're', '08': 'ri', '00': 'ro',
        '12': 'da', '14': 'de', '16': 'di', '18': 'do', '84': 'sa', '85': 'se', '86': 'si', '87': 'so',
        '62': 'la', '64': 'le', '61': 'li', '66': 'lo', '04': 'ma', '06': 'me', '03': 'mi', '05': 'mo',
        '80': 'na', '81': 'ne', '82': 'ni', '83': 'no',
        '·80': 'ta', '·81': 'te', '·82': 'ti', '·83': 'to', '·84': 'qua', '·85': 'que', '·86': 'qui',
        '·87': 'che', '·88': 'chi', '·89': 'non', '·08': 'ns', '·00': 'smta'}

lm = LM(); runs = digit_stream(load())
S = Solver(runs, lm, chunk=80, seed=1, lam=2.0, pairletters=True, mu=0.0)
key = {s: UNUSED for s in S.symbols}
for s in S.symbols:
    if s in KEY2: key[s] = KEY2[s]
    elif len(s.replace('·', '')) == 1 and s[0] in KEY2: key[s] = KEY2[s[0]]   # dotted single -> same letter
S.init_key(key)
print('key2 total (lam=2):', round(S.total(), 1))
print(S.plaintext()[:1500])
# random baseline
import random
tot = 0
for seed in range(3):
    R = Solver(runs, lm, chunk=80, seed=seed, lam=2.0, pairletters=True, mu=0.0); R.init_key({}); tot += R.total()
print('random key baseline (lam=2):', round(tot / 3, 1))
