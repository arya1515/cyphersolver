"""Ormonde-Maltravers cipher (1634-35): structural analysis + regular-alphabet test + hill-climb.

Run:  python analyze.py            (all sections)
      python analyze.py --climb N  (N hill-climb restarts, default 40)
"""
import json, math, random, re, sys
from collections import Counter

random.seed(1)
CT = open('ciphertext.txt', encoding='utf-8').read()

# ---------- 1. parse cipher runs (sequences of comma-separated figures) ----------
runs = []
for m in re.finditer(r'(?<![\w])(\d{1,3}(?:,?\s+\d{1,3})+)(?![\w])', CT):
    if m.group(1).startswith(('1634', '1635')):
        continue
    nums = [int(x) for x in re.findall(r'\d+', m.group(1))]
    pre = CT[max(0, m.start() - 40):m.start()].replace('\n', ' ').split()[-4:]
    post = CT[m.end():m.end() + 40].replace('\n', ' ').split()[:3]
    runs.append((nums, ' '.join(pre), ' '.join(post)))
allnums = [n for r in runs for n in r[0]]
print('=== RUNS ===')
for nums, pre, post in runs:
    print(f'  ...{pre} [{" ".join(map(str, nums))}] {post}...')
print(f'\n{len(runs)} runs, {len(allnums)} figures, {len(set(allnums))} distinct; max={max(allnums)}')

# ---------- 2. frequencies / ranges ----------
cnt = Counter(allnums)
print('\n=== FREQUENCY (count>1) ===')
print('  ', {k: v for k, v in sorted(cnt.items()) if v > 1})
print('\n=== DISTRIBUTION BY RANGE ===')
for lo, hi in [(1, 30), (31, 60), (61, 90), (91, 111), (112, 300)]:
    xs = sorted(k for k in cnt if lo <= k <= hi)
    print(f'  {lo:3d}-{hi:3d}: {len(xs):2d} distinct  {xs}')

# figures that only occur adjacent to a >=112 figure or at the edge of a run => candidate nulls
edge = Counter(); total = Counter()
for nums, _, _ in runs:
    for i, n in enumerate(nums):
        total[n] += 1
        nb = [nums[j] for j in (i - 1, i + 1) if 0 <= j < len(nums)]
        if i in (0, len(nums) - 1) or any(x >= 112 for x in nb):
            edge[n] += 1
print('\n=== 91-111 figures: position (edge/next-to-word-code) ===')
for n in sorted(k for k in cnt if 91 <= k <= 111):
    print(f'  {n}: {edge[n]}/{total[n]} occurrences at run edge or beside a >=112 code')

# ---------- 3. repeated bigrams ----------
big = Counter()
for nums, _, _ in runs:
    for a, b in zip(nums, nums[1:]):
        big[(a, b)] += 1
print('\n=== REPEATED BIGRAMS ===', [(k, v) for k, v in big.items() if v > 1])
print('  44 79 / 79 44 both occur: "44 79" in Crosby (r o), "79 44" in councellor (o r)')

# ---------- 4. regular-alphabet hypothesis derived from cribs ----------
# Cribs (doubled letters use *consecutive* figures -> each letter owns a consecutive block):
#   28 69 49 50 70 44 89       = l e t t e r (s)          "brought no letters from the Lord Deputy"
#   11 79 85 35 12 69 28 29 79 44 = c o u n c e l l o r   "is to be a councellor"  (Ormonde sworn PC Jan 1635)
#   10 44 79 47 8 59           = C r o s b y              (Sir Piers Crosby, "like to go worser with him")
#   65 35 21 26 59             = a n g ? y                "he was angry with the Lord Deputy"
CONS = 'bcdfghklmnpqrstwxyz'      # 19 consonants, 17th-c. 24-letter alphabet (i=j, u=v)
VOWS = 'aeiou'

def grid(start=7, size=3, vstart=64, vsizes=(3, 6, 6, 6, 6)):
    """Regular key: consonants b..z in blocks of `size` from `start`; vowels from `vstart`."""
    key = {}
    n = start
    for c in CONS:
        for _ in range(size):
            key[n] = c; n += 1
    n = vstart
    for v, s in zip(VOWS, vsizes):
        for _ in range(s):
            key[n] = v; n += 1
    return key

def decode(nums, key, words=None):
    out = []
    for n in nums:
        if n in key: out.append(key[n])
        elif 91 <= n <= 111: out.append('.')          # null
        else: out.append(f'<{words.get(n, n) if words else n}>')
    return ' '.join(out) if any(len(x) > 1 for x in out) else ''.join(out)

WORDS = {186: 'Lord Deputy', 143: 'the King?', 174: 'Ormonde', 221: 'Parliament', 270: 'Crosby(new)',
         113: 'with?', 185: '?185', 149: '?149', 218: '?218'}
key = grid()
print('\n=== REGULAR GRID (consonants 3 each from 7; vowels from 64) ===')
for lo in range(7, 91, 3):
    seg = [f'{n}={key[n]}' for n in range(lo, min(lo + 3, 91)) if n in key]
    print('  ' + '  '.join(seg))
print('\n=== DECODE WITH GRID ===')
for nums, pre, post in runs:
    print(f'  ...{pre} [{decode(nums, key, WORDS)}] {post}...')

# ---------- 5. exhaustive test of regular grids: which (start,size) make the letter-runs words? ----------
lm = json.load(open('../beale/en_lm.json'))
QUAD = lm['quad']; QTOT = sum(QUAD.values()); QFLOOR = math.log10(0.01 / QTOT)
def qscore(s):
    s = re.sub('[^a-z]', '', s)
    return sum(math.log10(QUAD[s[i:i+4]] / QTOT) if s[i:i+4] in QUAD else QFLOOR for i in range(len(s) - 3))
letter_runs = [[65, 35, 21, 26, 59], [28, 69, 49, 50, 70, 44, 89], [10, 44, 79, 47, 8, 59],
               [11, 79, 85, 35, 12, 69, 28, 29, 79, 44]]
print('\n=== SCAN OF REGULAR GRIDS (consonants b..z from `start` in blocks of `size`, then vowels a,e,i,o,u in blocks of `vs`) ===')
res = []
for start in range(1, 12):
    for size in (2, 3, 4):
        for vs in (2, 3, 4, 5, 6):
            vstart = start + len(CONS) * size
            k = grid(start, size, vstart, (vs,) * 5)
            if max(k) > 111:
                continue
            if any(n not in k for r in letter_runs for n in r):      # every figure must be covered
                continue
            txt = ' '.join(decode(r, k) for r in letter_runs)
            res.append((qscore(txt), start, size, vs, txt))
for sc, start, size, vs, txt in sorted(res, reverse=True)[:8]:
    print(f'  start={start:2d} size={size} vs={vs}  q={sc:7.1f}   {txt}')
print(f'  ({len(res)} grids tested)')

# ---------- 6. hill-climb (homophonic, letters only, figures < 91) ----------
def climb(restarts=40, iters=4000):
    syms = sorted({n for r in letter_runs for n in r})
    ALPHA = 'abcdefghiklmnopqrstuwxyz'
    best_all = (-1e9, None)
    for r in range(restarts):
        m = {s: random.choice(ALPHA) for s in syms}
        cur = qscore(' '.join(''.join(m[n] for n in run) for run in letter_runs))
        T = 2.0
        for it in range(iters):
            s = random.choice(syms); old = m[s]; m[s] = random.choice(ALPHA)
            sc = qscore(' '.join(''.join(m[n] for n in run) for run in letter_runs))
            if sc > cur or random.random() < math.exp((sc - cur) / T):
                cur = sc
            else:
                m[s] = old
            T = max(0.05, T * 0.999)
        if cur > best_all[0]:
            best_all = (cur, dict(m))
    sc, m = best_all
    return sc, [''.join(m[n] for n in run) for run in letter_runs]

if __name__ == '__main__':
    n = int(sys.argv[sys.argv.index('--climb') + 1]) if '--climb' in sys.argv else 40
    print(f'\n=== UNCONSTRAINED HILL-CLIMB on the 4 letter-runs ({n} restarts) ===')
    sc, words = climb(n)
    print(f'  best q={sc:.1f}: {words}')
    print(f'  true-key q={qscore(" ".join(decode(r, key) for r in letter_runs)):.1f}: '
          f'{[decode(r, key) for r in letter_runs]}')
    print('  (28 symbols / 28 letters: the climb just fits common quadgrams; no signal without the block structure)')
