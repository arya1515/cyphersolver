"""Matched control for solve_regions.py. Builds a random key of the given REGIONS design and enciphers 16th/17th-c.
French with the target's clear/cipher run pattern. Region kinds as in solve_regions.py; for the control the
generator fills: La = alphabetical letters with frequency-weighted homophones; Lf = same letters, shuffled onto the
numbers; Sa = consonant blocks with vowels in order; Sc = consonant blocks with vowels scrambled; Sf = random CV per
number. Numbers are drawn at random inside each range (density ~ that of the target: DENSITY env, default 0.35).
Encipherment: CV pair -> syllable with prob PSYL if the key has it, else a letter (letters must exist in some L region).
env: SEED REGIONS PSYL DENSITY CORPUS ; writes control<seed>.txt and control<seed>_key.txt
"""
import random, os, sys, glob
from solve_regions import parse, clean, parse_regions, LET, CONS, MIX
seed = int(os.environ.get('SEED', '1')); rnd = random.Random(seed)
REGIONS = os.environ.get('REGIONS', '52-399:Sa,400-489:La'); PSYL = float(os.environ.get('PSYL', '0.7'))
DENSITY = float(os.environ.get('DENSITY', '0.35'))
files = sys.argv[1:] or ['ct_shared.txt']
items = parse(files)
runs = []; cur = None
for k, a in items:
    if k == 'P':
        if cur and cur[0] == 'P': cur[1] += chr(97 + a)
        else: cur = ['P', chr(97 + a)]; runs.append(cur)
    else:
        if cur and cur[0] == 'C': cur[1] += 1
        else: cur = ['C', 1]; runs.append(cur)
weights = {'e': 5, 'a': 4, 's': 4, 'i': 3, 'n': 3, 't': 3, 'r': 3, 'u': 3, 'o': 3, 'l': 3, 'd': 2, 'c': 2, 'm': 2, 'p': 2,
           'q': 1, 'b': 1, 'f': 1, 'g': 1, 'h': 1, 'x': 1, 'y': 1, 'z': 1}
letkey = {}; sylkey = {}
for lo, hi, kind in parse_regions(REGIONS):
    span = list(range(lo, hi + 1))
    if kind in ('La', 'Lf'):
        n = max(len(LET), int(len(span) * DENSITY))
        pool = []
        for l in LET: pool += [l] * weights[l]
        while len(pool) < n: pool.append(rnd.choice('eaistnrulo'))
        pool = pool[:n]
        nums = sorted(rnd.sample(span, n))
        if kind == 'La': pool = sorted(pool, key=LET.index)
        else: rnd.shuffle(pool)
        for l, num in zip(pool, nums): letkey.setdefault(l, []).append(num)
    elif kind in ('Sa', 'Sc'):
        per = len(span) / len(CONS); pos = lo
        for c in CONS:
            width = max(3, int(round(per + rnd.uniform(-per / 3, per / 3))))
            slots = list(range(pos, min(hi + 1, pos + width))); pos += width
            vow = [v for v in 'aeiou' if rnd.random() < 0.85]
            if len(slots) >= len(vow) and vow:
                chosen = sorted(rnd.sample(slots, len(vow)))
                if kind == 'Sc': rnd.shuffle(vow)
                for v, num in zip(vow, chosen): sylkey[c + v] = num
            if pos > hi: break
    elif kind == 'Ma':
        # one-part series: walk the interleaved vocabulary in order, giving each unit 0..3 slots (letters weighted)
        units = [''.join(chr(97 + x) for x in u) for u in MIX]
        pos = lo
        for u in units:
            if len(u) == 1: k = max(1, round(weights[u] * 0.6)) if u in weights else 1
            else: k = 1 if rnd.random() < 0.8 else 0
            gap = rnd.randint(0, 2)
            pos += gap
            for _ in range(k):
                if pos > hi: break
                if len(u) == 1: letkey.setdefault(u, []).append(pos)
                else: sylkey[u] = pos   # last homophone wins; syllables get one slot
                pos += 1
        if pos < hi * 0.8: print('warning: Ma design used only up to', pos)
    elif kind == 'Sf':
        syls = [c + v for c in CONS for v in 'aeiou']; rnd.shuffle(syls)
        n = min(len(syls), int(len(span) * DENSITY)); nums = rnd.sample(span, n)
        for s, num in zip(syls[:n], nums): sylkey[s] = num
src = ' '.join(open(f, encoding='utf-8', errors='ignore').read() for f in sorted(glob.glob(os.environ.get('CORPUS', '../ducroc/corpus/cath0*.txt'))))
src = clean(src)
# pick a stretch that is not OCR garbage: require a plausible vowel share
while True:
    start = rnd.randrange(len(src) // 6, len(src) * 5 // 6); text = src[start:start + 5000]
    v = sum(text.count(c) for c in 'aeiou') / len(text)
    if 0.40 < v < 0.50 and 'iiii' not in text[:600]: break
p = 0; out = []
def enc(n):
    global p
    toks = []
    while len(toks) < n:
        pair = text[p:p + 2]
        if len(pair) == 2 and pair in sylkey and rnd.random() < PSYL: toks.append(str(sylkey[pair])); p += 2
        else:
            ch = text[p]
            if ch in letkey: toks.append(str(rnd.choice(letkey[ch])))
            p += 1
    return toks
for r in runs:
    if r[0] == 'P': out.append('[' + r[1] + ']')
    else: out.append(' '.join(enc(r[1])))
open(f'control{seed}.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
open(f'control{seed}_key.txt', 'w', encoding='utf-8').write(
    ' '.join(f'{n}={s}' for s, n in sorted(sylkey.items(), key=lambda x: x[1])) + '\n' +
    ' '.join(f'{n}={l}' for l, ns in letkey.items() for n in ns) + '\n' + text[:p] + '\n')
print('control', seed, REGIONS, 'tokens', sum(r[1] for r in runs if r[0] == 'C'), 'plain used', p)
