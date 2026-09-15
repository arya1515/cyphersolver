"""Do the dots mark unit boundaries? A segmentation anchor, using Elio's documented mechanics.

Lasry, Simonetta and Biermann (HistoCrypt 2025) describe the polyphonic-syllabic design Antonio Elio
built for Paul III's chancery. The detail that matters operationally:

    "Each symbol used to encode a syllable has a dual meaning. For example, the symbol used to encode
     'de' also encodes the syllable 'do'. The second choice ('do') is indicated by adding a dot above
     THE PREVIOUS CIPHER SYMBOL."

Meister's key no. 1 of 1539-42 says the same in the chancery's own words: "Con il punto sopra
l'antecedente."

So a dot is not a property of the symbol it sits on. It is a flag attached to the END of one unit that
modifies the NEXT unit. If IA-2's units are two digits wide, a dotted digit must therefore be the
SECOND digit of its unit - an odd offset counting from the start of a run - and the digit after it must
open a new unit.

That is a testable prediction, and it needs no key. If it holds, the 203 marked digits become 203
anchor points for segmenting the stream, which is the single thing every attack here has lacked.

Usage: python dots3.py
"""
import collections, random, re

import escape as E


def load_marked():
    """Digits with their marks, preserving position, not crossing cleartext breaks."""
    t = open('ASV_i1025_SdS_Spain_IA-2.txt', encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<CLEARTEXT.*?>', '|', t, flags=re.S)
    t = re.sub(r'#[^\n]*', '', t)
    out = []
    for m in re.finditer(r'(\d)(\^?[._]?)|(\|)', t):
        out.append(('|', '') if m.group(3) else (m.group(1), m.group(2)))
    return out


def segments(seq, null='4'):
    segs, cur = [], []
    for d, mk in seq:
        if d == '|' or d == null:
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append((d, mk))
    if cur:
        segs.append(cur)
    return segs


def main():
    seq = load_marked()
    segs = segments(seq)
    print('%d segments between nulls' % len(segs))

    # ---------------------------------------------------------------- 1. parity of dotted offsets
    ev = od = 0
    tot_ev = tot_od = 0
    dotted_digits = collections.Counter()
    after = collections.Counter()
    before = collections.Counter()
    for s in segs:
        for i, (d, mk) in enumerate(s):
            if i % 2 == 0:
                tot_ev += 1
            else:
                tot_od += 1
            if mk:
                dotted_digits[d] += 1
                if i % 2 == 0:
                    ev += 1
                else:
                    od += 1
                if i + 1 < len(s):
                    after[s[i + 1][0]] += 1
                if i > 0:
                    before[s[i - 1][0]] += 1
    n = ev + od
    exp_ev = n * tot_ev / (tot_ev + tot_od)
    print('\n=== 1. PARITY OF DOTTED POSITIONS inside null-delimited segments')
    print('   dotted digits: %d   at even offsets %d, odd offsets %d' % (n, ev, od))
    print('   expected even if dots fell anywhere: %.1f' % exp_ev)
    print('   Elio predicts dotted digits sit at ODD offsets (second digit of a two-digit unit).')
    sd = (n * (tot_ev / (tot_ev + tot_od)) * (tot_od / (tot_ev + tot_od))) ** 0.5
    print('   z = %+.2f' % ((ev - exp_ev) / sd if sd else 0))

    # ---------------------------------------------------------------- 2. which digits carry dots
    print('\n=== 2. WHICH DIGITS CARRY DOTS, AND WHAT FOLLOWS')
    allc = collections.Counter(d for d, m in seq if d != '|')
    N = sum(allc.values())
    print('   digit  dotted  overall  enrichment')
    for d, c in dotted_digits.most_common():
        print('     %s   %5d  %7d  %.2f' % (d, c, allc[d], (c / n) / (allc[d] / N)))
    print('   digit AFTER a dotted digit : %s'
          % ' '.join('%s:%.3f' % (k, v / sum(after.values())) for k, v in sorted(after.items())))
    print('   digit BEFORE a dotted digit: %s'
          % ' '.join('%s:%.3f' % (k, v / sum(before.values())) for k, v in sorted(before.items())))
    print('   overall digit frequency    : %s'
          % ' '.join('%s:%.3f' % (k, v / N) for k, v in sorted(allc.items())))

    # ---------------------------------------------------------------- 3. distance between dots
    print('\n=== 3. GAPS BETWEEN CONSECUTIVE DOTS')
    pos = [i for i, (d, m) in enumerate((x for x in seq if x[0] != '|')) if m]
    gaps = [b - a for a, b in zip(pos, pos[1:])]
    gc = collections.Counter(gaps)
    print('   %d dots, mean gap %.1f' % (len(pos), sum(gaps) / len(gaps)))
    ev_g = sum(v for k, v in gc.items() if k % 2 == 0)
    od_g = sum(v for k, v in gc.items() if k % 2 == 1)
    print('   gap parity: even %d, odd %d' % (ev_g, od_g))
    print('   If units are two digits wide and dots sit at unit ends, gaps should be EVEN.')
    print('   gap histogram: %s' % ' '.join('%d:%d' % (k, v) for k, v in sorted(gc.items()) if k <= 14))


if __name__ == '__main__':
    main()
