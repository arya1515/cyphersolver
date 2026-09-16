"""Matched control: encipher a passage of 16th-c. French with a random key of the hypothesised structure and
write it in the ct_*.txt format (with the same clear-text interleaving pattern as the target files)."""
import random, re, sys, unicodedata, glob
from solve import parse, clean, BLOCK0, NBLK
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rnd = random.Random(seed)
# target shape: count letter tokens per cipher run and clear runs, from the real files
import os
files = os.environ.get('CTFILES', 'ct_233.txt,ct_239.txt,ct_288.txt').split(',')
items, syms = parse(files)
runs = []  # list of (kind, length) kind C=cipher run (count of letter+syll tokens), P=plain text string
cur = None
for it in items:
    if it[0] == 'P':
        if cur and cur[0] == 'P': cur[1] += chr(97 + it[1])
        else: cur = ['P', chr(97 + it[1])]; runs.append(cur)
    elif it[0] in 'LS':
        if cur and cur[0] == 'C': cur[1] += 1
        else: cur = ['C', 1]; runs.append(cur)
    else:
        if cur and cur[0] == 'C': cur[1] += 0
        runs.append(['N', 1]); cur = None
ncipher = sum(r[1] for r in runs if r[0] == 'C')
# letter symbol profile: number of homophones per letter drawn to match the target's symbol count (~52 used in 1..63)
nsyms = len(syms)
letters = 'abcdefghilmnopqrstuxyz'
weights = {'e': 6, 'a': 4, 'i': 3, 's': 3, 'n': 3, 't': 3, 'r': 3, 'u': 3, 'o': 3, 'l': 3, 'd': 2, 'c': 2, 'm': 2, 'p': 2,
           'q': 1, 'b': 1, 'f': 1, 'g': 1, 'h': 1, 'x': 1, 'y': 1, 'z': 1}
nnull = 6
pool = []
for l, w in weights.items(): pool += [l] * w
while len(pool) + nnull < nsyms: pool.append(rnd.choice('eaistnrulo'))
pool = pool[:nsyms - nnull] + ['-'] * nnull
nums = list(range(1, BLOCK0)); rnd.shuffle(nums); nums = nums[:nsyms]
key = dict(zip(nums, pool))                       # number -> letter or '-'
homs = {}
for n, l in key.items(): homs.setdefault(l, []).append(n)
cons = rnd.sample('bcdflmnprstgqhxz', NBLK)      # block consonants
blk = {c: BLOCK0 + 5 * k for k, c in enumerate(cons)}
# plaintext source: a stretch of the du Croc corpus (Catherine de Medicis letters) chosen at random
src = ' '.join(open(f, encoding='utf-8', errors='ignore').read() for f in sorted(glob.glob('../ducroc/corpus/cath0*.txt')))
src = clean(src)
start = rnd.randrange(len(src) // 4, len(src) // 2); text = src[start:start + 4000]
pos = 0
def encipher(n_tokens):
    global pos
    out = []; plain = ''
    while len(out) < n_tokens:
        ch = text[pos]
        if ch in blk and pos + 1 < len(text) and text[pos + 1] in 'aeiou' and rnd.random() < 0.75:
            out.append(str(blk[ch] + 'aeiou'.index(text[pos + 1]))); plain += ch + text[pos + 1]; pos += 2
        elif ch in homs:
            out.append(str(rnd.choice(homs[ch]))); plain += ch; pos += 1
        else: pos += 1
        if rnd.random() < nnull / 60 and '-' in homs: out.append(str(rnd.choice(homs['-'])))
    return out, plain
lines = []; plains = []
for r in runs:
    if r[0] == 'P': lines.append('[' + r[1] + ']')
    elif r[0] == 'C':
        toks, plain = encipher(r[1]); lines.append(' '.join(toks)); plains.append(plain)
    else: lines.append('pi')
open(f'control{seed}.txt', 'w', encoding='utf-8').write('# control seed %d\n' % seed + '\n'.join(lines) + '\n')
open(f'control{seed}_key.txt', 'w', encoding='utf-8').write(repr(key) + '\n' + repr(blk) + '\n' + '\n'.join(plains) + '\n')
print('written control%d.txt; cipher tokens %d; plain letters %d' % (seed, ncipher, sum(len(p) for p in plains)))
