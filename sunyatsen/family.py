"""Brute-force the family of *systematic* code condensers (20 consonants x 5 vowels)
against the Tanaka->Sun telegram, scoring decoded 4-digit codes with a Chinese LM.

Family (cf. Yamada's two known tables):
  consonant order = alphabetical b..z rotated by r (0..19), forward or reversed
  vowel order      = any permutation of a e i o u
  fill             = cons-major (n = 5*ci + vi) or vowel-major (n = 20*vi + ci)
  offset           = 0 (00..99) or 1 (01..99, 00 = 100th)
  additive         = 0, +111, -111 on the 4-digit code (mod 10000)
"""
import csv, json, math, itertools, os, sys, collections
here = os.path.dirname(os.path.abspath(__file__))
from parse import parse, groups, CONS, VOW

# --- codebook -------------------------------------------------------------
code2ch = {}
for name in ('tw.csv', 'cn.csv'):
    with open(os.path.join(here, name), encoding='utf-8') as f:
        for row in csv.DictReader(f):
            for code in row['code'].split():
                code2ch.setdefault(code, row['character'])
lm = json.load(open(os.path.join(here, 'lm_zh.json'), encoding='utf-8'))
uni = lm['uni']; tot = sum(uni.values())
UNK = math.log(1e-8)
def lp(ch):
    return math.log((uni.get(ch, 0) + 0.5) / tot)
def score_codes(codes):
    s = 0.0
    for c in codes:
        ch = code2ch.get(c)
        s += lp(ch) if ch else UNK
    return s

# --- ciphertext segments --------------------------------------------------
tokens = parse(groups)
segs, cur = [], []
for t in tokens:
    if t.startswith('?'):
        if cur: segs.append(cur); cur = []
    else:
        cur.append(t)
if cur: segs.append(cur)
segs = [s for s in segs if len(s) >= 2]
# segment 0 starts the message: alignment fixed
ALIGN = [(0,)] + [(0, 1)] * (len(segs) - 1)

def decode_segments(table, additive):
    """table: dict syllable -> int 0..99. Returns list of (codes) per segment/alignment."""
    out = []
    for seg, aligns in zip(segs, ALIGN):
        nums = [table[s] for s in seg]
        best = None
        for a in aligns:
            codes = []
            for i in range(a, len(nums) - 1, 2):
                n = (nums[i] * 100 + nums[i + 1] + additive) % 10000
                codes.append('%04d' % n)
            sc = score_codes(codes)
            if best is None or sc > best[0]:
                best = (sc, codes)
        out.append(best)
    return out

def make_table(cons_order, vow_order, fill, offset):
    t = {}
    for ci, c in enumerate(cons_order):
        for vi, v in enumerate(vow_order):
            n = 5 * ci + vi if fill == 'cons' else 20 * vi + ci
            t[c + v] = (n + offset) % 100
    return t

if __name__ == '__main__':
    sys.stdout = open(os.path.join(here, 'family_out.txt'), 'w', encoding='utf-8')
    base = list(CONS)
    results = []
    cons_orders = []
    for r in range(20):
        rot = base[r:] + base[:r]
        cons_orders.append(('rot%d' % r, rot)); cons_orders.append(('rev%d' % r, rot[::-1]))
    for (cname, co) in cons_orders:
        for vo in itertools.permutations(VOW):
            for fill in ('cons', 'vow'):
                for off in (0, 1):
                    tbl = make_table(co, vo, fill, off)
                    for add in (0, 111, -111):
                        dec = decode_segments(tbl, add)
                        sc = sum(d[0] for d in dec)
                        results.append((sc, cname, ''.join(vo), fill, off, add, dec))
    results.sort(key=lambda x: -x[0])
    print('keys tried', len(results))
    for sc, cname, vo, fill, off, add, dec in results[:15]:
        txt = ' | '.join(''.join(code2ch.get(c, '□') for c in d[1]) for d in dec)
        print('%.1f %s %s %s off%d add%d  %s' % (sc, cname, vo, fill, off, add, txt))
    # baseline: random-ish scores distribution
    scs = [r[0] for r in results]
    print('mean %.1f  sd %.1f  max %.1f' % (sum(scs)/len(scs), (sum((x-sum(scs)/len(scs))**2 for x in scs)/len(scs))**0.5, max(scs)))
