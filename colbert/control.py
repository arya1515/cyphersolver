"""Matched control for solve_mono.py: encipher 17th-c. French with a random key of the hypothesised design and the
same clear/cipher run pattern as the target file(s). Writes control<seed>.txt and control<seed>_key.txt.

Design (REGION=SL default): syllables occupy numbers in [SLO, SPLIT) in consonant-block order, vowels a e i o u in order,
each block a random subset of its five vowels plus random spare slots (unused numbers); letters occupy [SPLIT, SHI]
in alphabetical order with homophone counts weighted by frequency. Encipherment: a CV pair is written as a syllable
with probability PSYL when the key has it, else letter by letter.
env: SEED SPLIT SLO SHI PSYL CORPUS
"""
import random, re, sys, os, glob, unicodedata
from solve_mono import parse, clean, CONS, VOW, LET
seed = int(os.environ.get('SEED', '1')); rnd = random.Random(seed)
SPLIT = int(os.environ.get('SPLIT', '400')); SLO = int(os.environ.get('SLO', '50')); SHI = int(os.environ.get('SHI', '489'))
PSYL = float(os.environ.get('PSYL', '0.75'))
files = sys.argv[1:] or ['ct_shared.txt']
items = parse(files)
# run pattern
runs = []; cur = None
for k, a in items:
    if k == 'P':
        if cur and cur[0] == 'P': cur[1] += chr(97 + a)
        else: cur = ['P', chr(97 + a)]; runs.append(cur)
    else:
        if cur and cur[0] == 'C': cur[1] += 1
        else: cur = ['C', 1]; runs.append(cur)
# syllable key: numbers SLO..SPLIT-1 spread over consonant blocks
nsyl_slots = SPLIT - SLO
blocks = list(CONS)
per = nsyl_slots / len(blocks)
sylkey = {}
pos = SLO
for c in blocks:
    width = max(3, int(round(per + rnd.uniform(-per / 3, per / 3))))
    slots = list(range(pos, min(SPLIT, pos + width))); pos += width
    vow = [v for v in VOW if rnd.random() < 0.85]
    # vowels in order, placed on increasing slots, leaving gaps
    if len(slots) >= len(vow) and vow:
        chosen = sorted(rnd.sample(slots, len(vow)))
        for v, n in zip(vow, chosen): sylkey[c + v] = n
    if pos >= SPLIT: break
# letter key: SPLIT..SHI alphabetical with homophones
weights = {'e': 5, 'a': 4, 's': 4, 'i': 3, 'n': 3, 't': 3, 'r': 3, 'u': 3, 'o': 3, 'l': 3, 'd': 2, 'c': 2, 'm': 2, 'p': 2,
           'q': 1, 'b': 1, 'f': 1, 'g': 1, 'h': 1, 'x': 1, 'y': 1, 'z': 1}
nlet = SHI - SPLIT + 1
pool = []
for l in LET: pool += [l] * weights[l]
while len(pool) < nlet: pool.append(rnd.choice('eaistnrulo'))
pool = sorted(pool[:nlet], key=lambda l: LET.index(l))
letkey = {}
for l, n in zip(pool, range(SPLIT, SHI + 1)): letkey.setdefault(l, []).append(n)
# plaintext
src = ' '.join(open(f, encoding='utf-8', errors='ignore').read() for f in sorted(glob.glob(os.environ.get('CORPUS', '../ducroc/corpus/cath0*.txt'))))
src = clean(src)
start = rnd.randrange(len(src) // 4, len(src) // 2); text = src[start:start + 5000]
p = 0; out = []; keyrows = []
def enc(n):
    global p
    toks = []
    while len(toks) < n:
        pair = text[p:p + 2]
        if len(pair) == 2 and pair in sylkey and rnd.random() < PSYL:
            toks.append(str(sylkey[pair])); p += 2
        else:
            ch = text[p]
            if ch in letkey: toks.append(str(rnd.choice(letkey[ch]))); p += 1
            else: p += 1   # letter not in key (w, k): skip
    return toks
for r in runs:
    if r[0] == 'P': out.append('[' + r[1] + ']');
    else: out.append(' '.join(enc(r[1])))
open(f'control{seed}.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
open(f'control{seed}_key.txt', 'w', encoding='utf-8').write(
    ' '.join(f'{n}={s}' for s, n in sorted(sylkey.items(), key=lambda x: x[1])) + '\n' +
    ' '.join(f'{n}={l}' for l, ns in letkey.items() for n in ns) + '\n' + text[:p] + '\n')
print('control', seed, 'tokens', sum(r[1] for r in runs if r[0] == 'C'), 'plain used', p)
