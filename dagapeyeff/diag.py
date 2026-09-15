"""Remaining hypotheses for the D'Agapeyeff challenge.

Ruled out so far: one-to-one Polybius of English (frequency profile, order-independent, 0/3000
English samples as flat); a transposition (substitution-invariant search scores no better than on
random shuffles); the book's null rule at every period and offset.

Still untested, and all cheap:
  1. a plaintext in some other language - D'Agapeyeff was Russian-born and the book is English, but
     French, German, Italian, Spanish, Latin and transliterated Russian are all worth a fit;
  2. a numeric or tabular plaintext, which would use far fewer distinct symbols;
  3. polyalphabetic structure - if the square changed on a period, the index of coincidence taken on
     every n-th cell would rise at the true period;
  4. any repeated n-gram at all, which every natural-language cipher of this length should show.
"""
import collections, itertools, math, random, re, sys

from ct import DIGITS

FREQ = {
 'english': 'e12.7 t9.06 a8.17 o7.51 i6.97 n6.75 s6.33 h6.09 r5.99 d4.25 l4.03 c2.78 u2.76 m2.41 w2.36 f2.23 g2.02 y1.97 p1.93 b1.29 v0.98 k0.77 j0.15 x0.15 q0.10 z0.07',
 'french':  'e14.7 a7.6 i7.5 s7.9 n7.1 r6.6 t7.2 o5.4 l5.5 u6.3 d3.7 c3.3 m3.0 p3.0 g0.9 b0.9 v1.6 h0.7 f1.1 q1.4 y0.3 x0.4 j0.5 k0.05 w0.04 z0.1',
 'german':  'e17.4 n9.8 i7.6 s7.3 r7.0 a6.5 t6.2 d5.1 h4.8 u4.4 l3.4 c3.1 g3.0 m2.5 o2.5 b1.9 w1.9 f1.7 k1.2 z1.1 p0.8 v0.8 j0.3 y0.04 x0.03 q0.02',
 'italian': 'e11.8 a11.7 i11.3 o9.8 n6.9 l6.5 r6.4 t5.6 s5.0 c4.5 d3.7 p3.1 u3.0 m2.5 v2.1 g1.6 h1.5 f1.1 b1.0 q0.5 z0.9 j0.01 k0.01 w0.01 x0.01 y0.01',
 'spanish': 'e13.7 a12.5 o8.7 s8.0 n6.7 r6.9 i6.2 l5.0 d5.9 t4.6 c4.0 u3.9 m3.2 p2.5 b1.4 g1.0 v0.9 y0.9 q0.9 h0.7 f0.7 z0.5 j0.4 x0.2 k0.01 w0.01',
 'latin':   'i11.4 e11.0 a8.0 u8.5 t8.0 s7.6 r6.7 n6.3 o5.4 m5.3 c4.0 l2.9 p3.0 d2.7 q1.5 b1.5 g1.2 v1.0 f0.9 h0.9 x0.6 y0.1 z0.1 j0.01 k0.01 w0.01',
 'russian_translit': 'o10.9 e8.5 a8.0 i7.4 n6.7 t6.3 s5.5 r4.7 v4.5 l4.4 k3.5 m3.2 d3.0 p2.8 u2.6 y1.9 g1.7 z1.6 b1.6 c1.5 h1.2 f0.3 j0.9 x0.4 q0.1 w0.1',
 'digits_uniform': ' '.join('%s10.0' % d for d in '0123456789'),
}


def parse(spec):
    out = {}
    for tok in spec.split():
        out[tok[0]] = float(tok[1:])
    return out


def cells(body=392):
    d = DIGITS[:body]
    return [d[i:i + 2] for i in range(0, len(d), 2)]


def best_case_chi2(counts, table):
    n = sum(counts)
    ev = sorted(table.values(), reverse=True)
    obs = sorted(counts, reverse=True)
    obs += [0] * (len(ev) - len(obs))
    obs = obs[:len(ev)]
    tot = sum(ev)
    exp = [n * v / tot for v in ev]
    return sum((o - e) ** 2 / max(e, 1e-9) for o, e in zip(obs, exp))


def ic(seq):
    c = collections.Counter(seq)
    n = len(seq)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1)) if n > 1 else 0


def main():
    seq = cells()
    counts = list(collections.Counter(seq).values())
    print('=== 1-2. frequency fit against candidate plaintext languages')
    print('   (best case over all keys; lower is better; English 196-letter samples median 7.3)')
    rows = []
    for name, spec in FREQ.items():
        rows.append((best_case_chi2(counts, parse(spec)), name))
    for v, name in sorted(rows):
        print('   %-20s %7.1f' % (name, v))

    print('\n=== 3. polyalphabetic test: IC of every n-th cell')
    print('   flat IC across periods means no periodic key')
    base = ic(seq)
    print('   whole text IC = %.4f' % base)
    for p in range(2, 16):
        parts = [seq[i::p] for i in range(p)]
        vals = [ic(x) for x in parts if len(x) > 3]
        print('   period %2d  mean IC %.4f' % (p, sum(vals) / len(vals)))

    print('\n=== 4. repeated n-grams of cells')
    for k in (2, 3, 4):
        g = collections.Counter(tuple(seq[i:i + k]) for i in range(len(seq) - k + 1))
        rep = {a: b for a, b in g.items() if b > 1}
        print('   %d-grams repeated: %d  %s' % (k, len(rep), sorted(rep.items(), key=lambda x: -x[1])[:5]))
    # what English gives
    txt = re.sub('[^a-z]', '', open('../beale/lmcorpus/pg1342.txt', encoding='utf-8', errors='ignore').read().lower())
    rnd = random.Random(2)
    for k in (3, 4):
        tot = 0
        for _ in range(300):
            i = rnd.randrange(0, len(txt) - 196)
            s = txt[i:i + 196]
            g = collections.Counter(s[j:j + k] for j in range(len(s) - k + 1))
            tot += sum(1 for v in g.values() if v > 1)
        print('   English 196 letters: %d-grams repeated on average %.1f' % (k, tot / 300))


if __name__ == '__main__':
    main()
