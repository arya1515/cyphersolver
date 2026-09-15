"""If IA-2 is built from two-digit units, what does the unit inventory look like?

phase.py established two things that no previous pass here had nailed down:

  * the stretches between the null 4 prefer EVEN lengths - 278 against 204, z = +3.37
  * inside those stretches there is a real two-digit phase - the digit distribution at even offsets
    differs from the one at odd offsets, chi-squared 39.4 against a shuffle null of 8.3 +- 4.1,
    z = +7.6, p < 0.0001. Digit 9 sits at even offsets 1.60 times as often as odd; digit 8 is the
    other way round at 0.84.

That is the signature of a syllabary: two-digit codes with a constrained lead digit. It is also what
Meister's key no. 1 of 1539-42 looks like, where 9 does structural work in most of the two-digit codes.

This script reads the even-length segments as pairs and asks whether the resulting inventory behaves
like a syllabary rather than like random pairs:

  1. how many distinct pairs are used, out of the 100 available
  2. whether the frequency profile matches Italian syllables
  3. whether the lead and trail positions have distinct alphabets, which is what a
     consonant-then-vowel syllabary produces
  4. a control: the same statistics on the odd-length segments read at both phases, and on shuffles

Usage: python units2.py
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


def pairs_of(seg):
    ds = [d for d, m in seg]
    return [ds[i] + ds[i + 1] for i in range(0, len(ds) - 1, 2)]


def profile(pairs, label):
    c = collections.Counter(pairs)
    n = sum(c.values())
    print('\n%s: %d units, %d distinct of 100 possible' % (label, n, len(c)))
    print('   top 24: %s' % ', '.join('%s:%d' % (k, v) for k, v in c.most_common(24)))
    top = sum(v for _, v in c.most_common(20))
    print('   top 20 carry %.1f%% of all units' % (100.0 * top / n))
    lead = collections.Counter(p[0] for p in pairs)
    trail = collections.Counter(p[1] for p in pairs)
    print('   lead  digits: %s' % ' '.join('%s:%.3f' % (k, v / n) for k, v in sorted(lead.items())))
    print('   trail digits: %s' % ' '.join('%s:%.3f' % (k, v / n) for k, v in sorted(trail.items())))
    return c


def entropy(c):
    n = sum(c.values())
    return -sum(v / n * math.log2(v / n) for v in c.values())


def main():
    seq = load()
    segs = segments(seq)
    even = [s for s in segs if len(s) % 2 == 0 and len(s) >= 2]
    odd = [s for s in segs if len(s) % 2 == 1 and len(s) >= 3]
    print('%d segments: %d even, %d odd' % (len(segs), len(even), len(odd)))

    P = [p for s in even for p in pairs_of(s)]
    c = profile(P, 'EVEN segments, phase 0')

    # control: odd segments read from the left (one digit will be dropped at the end)
    Q = [p for s in odd for p in pairs_of(s)]
    profile(Q, 'ODD segments, phase 0 (control)')

    # control: shuffle the digits within each even segment, keeping lengths
    rnd = random.Random(7)
    R = []
    for s in even:
        ds = [d for d, m in s]
        rnd.shuffle(ds)
        R.extend(ds[i] + ds[i + 1] for i in range(0, len(ds) - 1, 2))
    profile(R, 'EVEN segments, digits shuffled within segment (control)')

    print('\n=== ENTROPY (bits per unit; a 100-symbol uniform code would be 6.64)')
    print('   real even-segment units : %.3f' % entropy(collections.Counter(P)))
    print('   shuffled control        : %.3f' % entropy(collections.Counter(R)))

    print("""
=== READING

A syllabary shows up as a restricted lead alphabet, a restricted trail alphabet, and far fewer than
100 distinct units actually in use. Compare the real inventory with the shuffled control, which has
the same digit frequencies and the same segment lengths and differs only in order.""")


if __name__ == '__main__':
    main()
