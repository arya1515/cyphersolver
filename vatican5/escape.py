"""Does IA-2 have a dictionary-escape marker, like the one Lasry found in the sibling cipher?

The Part 4 challenge (ASV Portugal IA-1, the same Vatican series) says of that cipher:

    "The digits 3 and 9 seem to have some special meaning, as they can only be preceded by a 1 or 2.
     One possibility is that they might indicate (together with the preceding digit and the following
     digit, e.g., 132, or 291), some entry into a dictionary of words, names, places and common
     prepositions, while the other digits form codes representing letters and/or syllables."

That is a three-digit escape: a marker pair opens a dictionary code. If IA-2 has the same mechanism
with different digits, then every previous attack here was doomed for a reason that is fixable -
a letter-level model was being fitted to a stream in which a large fraction of the digits are not
letters at all, and the earlier matched control (vc_syn.py) did not simulate that, which is exactly
why the control converged and the real text did not.

The test needs no key. An escape marker shows up as a digit whose PREDECESSOR distribution is far more
concentrated than chance, because it may only follow the marker digits. This script measures, for every
digit and for every ordered pair:

  1. the predecessor and successor distributions, with the concentration of each
  2. which pairs are entirely absent, since a constrained marker forbids many combinations
  3. whether the absences are more than a text of this length and composition would give anyway

Usage: python escape.py
"""
import collections, math, random, re


def load():
    t = open('ASV_i1025_SdS_Spain_IA-2.txt', encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<CLEARTEXT.*?>', '|', t, flags=re.S)
    t = re.sub(r'#[^\n]*', '', t)
    out = []
    for m in re.finditer(r'(\d)(\^?[._]?)|(\|)', t):
        out.append(('|', '') if m.group(3) else (m.group(1), m.group(2)))
    return out


def runs(seq):
    """Maximal runs of digits, not crossing a cleartext break."""
    out, cur = [], []
    for d, mk in seq:
        if d == '|':
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append(d)
    if cur:
        out.append(cur)
    return out


def conc(dist):
    """Concentration: 1 - normalised entropy. 0 = flat, 1 = single value."""
    n = sum(dist.values())
    if n < 2:
        return 0.0
    H = -sum(v / n * math.log(v / n) for v in dist.values() if v)
    return 1 - H / math.log(10)


def main():
    seq = load()
    R = runs(seq)
    s = [d for r in R for d in r]
    print('%d digits in %d runs' % (len(s), len(R)))

    bg = collections.Counter()
    for r in R:
        bg.update(zip(r, r[1:]))
    digits = sorted(set(s))
    uncond = collections.Counter(s)
    N = len(s)

    print('\n=== 1. PREDECESSOR AND SUCCESSOR CONCENTRATION')
    print('   digit  freq    conc(prev)  conc(next)   most common predecessors')
    rows = []
    for d in digits:
        prev = collections.Counter({a: v for (a, b), v in bg.items() if b == d})
        nxt = collections.Counter({b: v for (a, b), v in bg.items() if a == d})
        rows.append((conc(prev), d, uncond[d] / N, conc(prev), conc(nxt),
                     ', '.join('%s:%.0f%%' % (k, 100.0 * v / sum(prev.values()))
                               for k, v in prev.most_common(4))))
    for _, d, f, cp, cn, top in sorted(rows, reverse=True):
        print('     %s   %.4f  %.4f      %.4f      %s' % (d, f, cp, cn, top))

    print('\n=== 2. ABSENT AND RARE ORDERED PAIRS  (expected count if independent)')
    missing = []
    for a in digits:
        for b in digits:
            e = uncond[a] * uncond[b] / N
            o = bg.get((a, b), 0)
            if e >= 3 and o <= max(1, e * 0.12):
                missing.append((o, e, a + b))
    missing.sort()
    if missing:
        for o, e, p in missing:
            print('     %s observed %2d, expected %5.1f' % (p, o, e))
    else:
        print('     none: no ordered pair is strongly suppressed')

    print('\n=== 3. IS THE SUPPRESSION REAL?  (shuffle control, same digit frequencies)')
    rnd = random.Random(3)
    pool = list(s)
    cnt = []
    for _ in range(400):
        rnd.shuffle(pool)
        b2 = collections.Counter(zip(pool, pool[1:]))
        k = 0
        for a in digits:
            for b in digits:
                e = uncond[a] * uncond[b] / N
                if e >= 3 and b2.get((a, b), 0) <= max(1, e * 0.12):
                    k += 1
        cnt.append(k)
    mu = sum(cnt) / len(cnt)
    print('     real text: %d strongly suppressed pairs' % len(missing))
    print('     shuffles : mean %.2f, max %d over 400 trials' % (mu, max(cnt)))

    print("""
=== READING

Lasry's sibling cipher had digits that could ONLY follow one or two others - a near-total
suppression of most predecessor pairs. If IA-2 had the same escape, one digit here would show a
predecessor concentration far above the rest and a long list of forbidden pairs. Compare the
numbers above against the shuffle control before reading anything into them.""")


if __name__ == '__main__':
    main()
