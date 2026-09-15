"""Read the Vatican Part 5 ciphertext under a constrained polyphonic key.

Two jobs:
  consensus  - do independent runs of vc.py agree? A polyphonic key is only believable if separate
               searches land in the same place. Measures the Rand index (fraction of letter pairs grouped
               the same way) between the best key and each other run. Chance for this constrained space is
               computed by shuffling within the vowel and consonant pools.
  decode     - beam-search the best letter sequence for a key, using the Italian 5-gram model, with 4 as a
               space. Polyphonic ciphers have no unique decode, so the language model picks the reading.

Usage:
    python vc_read.py consensus
    python vc_read.py decode "7=ao 0=e 3=i 1=u 8=tr 5=ns 2=ls 6=cm 9=dv"
"""
import collections, itertools, json, math, random, re, sys

from parse5 import load, digit_stream

AL = 'abcdefghilmnopqrstuvz'
VOWELS = set('aeiou')
NULL = 4


def parse_key(s):
    key = {}
    for part in s.split():
        d, ls = part.split('=')
        for c in ls:
            if c in AL:
                key.setdefault(int(d), []).append(c)
    return key


def key_from_log_line(line):
    m = re.search(r':\s*(-?[\d.]+)\s+(.*)$', line.strip())
    if not m:
        return None
    return float(m.group(1)), parse_key(m.group(2))


def groups_of(key):
    g = {}
    for d, ls in key.items():
        for c in ls:
            g[c] = d
    return g


def rand_index(a, b):
    ga, gb = groups_of(a), groups_of(b)
    same = tot = 0
    for x, y in itertools.combinations(AL, 2):
        if x not in ga or y not in ga or x not in gb or y not in gb:
            continue
        tot += 1
        same += (ga[x] == ga[y]) == (gb[x] == gb[y])
    return same / tot if tot else 0.0


def chance_rand(trials=2000, seed=0):
    """Rand index between two random keys drawn from the same constrained space."""
    rnd = random.Random(seed)
    vd, cd = [7, 0, 3, 1], [8, 5, 2, 6, 9]
    vals = []
    for _ in range(trials):
        ks = []
        for _ in range(2):
            k = collections.defaultdict(list)
            for c in AL:
                k[rnd.choice(vd if c in VOWELS else cd)].append(c)
            ks.append(dict(k))
        vals.append(rand_index(ks[0], ks[1]))
    return sum(vals) / len(vals)


def consensus():
    import glob
    rows = []
    for f in sorted(glob.glob('vc_s*.log')):
        for ln in open(f, encoding='utf-8', errors='ignore'):
            r = key_from_log_line(ln)
            if r:
                rows.append((r[0], r[1], f))
    if not rows:
        print('no vc_s*.log results yet')
        return
    rows.sort(key=lambda x: -x[0])
    best = rows[0][1]
    ch = chance_rand()
    print('%d runs; chance Rand index in this constrained space = %.3f' % (len(rows), ch))
    print('%-11s %-7s %s' % ('score', 'rand', 'key'))
    for sc, k, f in rows:
        print('%-11.1f %-7.2f %s' % (sc, rand_index(k, best), fmt(k)))
    top = [rand_index(k, best) for sc, k, f in rows[:8]]
    print('\nmean Rand of top 8 vs best: %.3f   (chance %.3f)' % (sum(top) / len(top), ch))


def fmt(key):
    return ' '.join('%d=%s' % (d, ''.join(sorted(key.get(d, []))) or '-')
                    for d in (7, 0, 3, 1, 8, 5, 2, 6, 9))


def decode(key, beam=400):
    ng = json.load(open('it_ngrams.json', encoding='utf-8'))
    g5 = ng.get('5', {})
    g4 = ng.get('4', {})
    g3 = ng['3']
    t3 = sum(g3.values())

    def lp(ctx, ch):
        for tbl, k in ((g5, ctx[-4:] + ch), (g4, ctx[-3:] + ch)):
            if len(k) == (5 if tbl is g5 else 4) and k in tbl:
                pre = k[:-1]
                tot = sum(tbl.get(pre + x, 0) for x in AL + ' ')
                if tot > 3:
                    return math.log((tbl[k] + 0.3) / (tot + 3))
        k3 = ctx[-2:] + ch
        tot = sum(g3.get(ctx[-2:] + x, 0) for x in AL + ' ')
        return math.log((g3.get(k3, 0) + 0.3) / (tot + 8)) if tot else math.log(1e-6)

    runs = digit_stream(load())
    out = []
    for r in runs:
        states = {('    ', ''): 0.0}
        for i, t in enumerate(r):
            d = t[0]
            bad = ('^' in t or '_' in t or '?' in t) or (i > 0 and ('^' in r[i - 1] or '_' in r[i - 1]))
            opts = [' '] if int(d) == NULL else (['?'] if bad else key.get(int(d), ['?']))
            nxt = {}
            for (ctx, txt), sc in states.items():
                for ch in opts:
                    s2 = sc + (lp(ctx, ch) if ch not in '? ' else (math.log(0.02) if ch == '?' else lp(ctx, ' ')))
                    k = ((ctx + ch)[-4:], '')
                    key2 = (k[0], len(txt) + 1)
                    if key2 not in nxt or nxt[key2][0] < s2:
                        nxt[key2] = (s2, txt + ch)
            states = {}
            for (c2, _), (s2, txt2) in sorted(nxt.items(), key=lambda kv: -kv[1][0])[:beam]:
                states[(c2, txt2)] = s2
            states = dict(sorted(states.items(), key=lambda kv: -kv[1])[:beam])
        if states:
            bestk = max(states, key=lambda k: states[k])
            out.append(bestk[1])
    return out


def main():
    if len(sys.argv) < 2 or sys.argv[1] == 'consensus':
        consensus()
    elif sys.argv[1] == 'decode':
        key = parse_key(sys.argv[2])
        print('key:', fmt(key))
        for i, seg in enumerate(decode(key)):
            print('\n--- run %d' % i)
            print(seg[:1200])


if __name__ == '__main__':
    main()
