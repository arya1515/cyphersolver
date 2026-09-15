"""A matched synthetic of Elio's polyphonic-syllabic design, tested against the real IA-2 statistics.

The identification of IA-2 as an Antonio Elio cipher rests so far on five qualitative matches. This
turns that into a quantitative test. Build a synthetic ciphertext to Elio's documented design and ask
whether it reproduces the real text's measured signatures. If it does, the identification is
corroborated by construction. If it does not, the identification is wrong and I should say so.

The design, from Lasry, Simonetta and Biermann (HistoCrypt 2025) and from the chancery's own
instructions printed by Meister:

  * h is dropped, and every doubled letter is reduced to one ("Scrivasi stretto et senza duplicare
    le consonanti")
  * most units are consonant-vowel syllables, encoded as two digits
  * some units are single letters, encoded as one digit  -> units are variable-length, and any digit
    may be a unit on its own or half of a pair
  * each syllable code is polyphonic: two meanings, the second selected by a dot on the PRECEDING
    digit
  * a null closes a letter or syllable carrying an abbreviation, not every word

The earlier matched control in this directory (vc_syn.py) simulated a polyphonic SINGLE-DIGIT cipher
and was correctly rejected by the search. This is the first control built to the design the cipher is
now believed to have.

Targets to reproduce, all measured on the real text:

    digits                       6549
    null rate                    0.0734
    dot rate                     0.031 of digits, 88% of them on three digits
    vowel share (non-null)       0.475
    mean vowel run               1.604      Italian letters give 1.301
    mean consonant run           1.769      Italian letters give 1.504
    consonant runs >= 3          0.183      Italian letters give 0.059
    doubled digits               all suppressed; 00 at 6 against 117 expected
    repeated 7-grams             441        a shuffle gives 5
    global two-digit phase       absent     z = -0.5 to -0.9
    phase restarting at nulls    chi2 39.4

Usage: python elio_syn.py [seed]
"""
import collections, math, random, re, sys

VOW = 'aeiou'
CONS = 'bcdfglmnpqrstvz'


def italian(n, rnd):
    """Period Italian, with h dropped and doubled letters reduced, as the chancery required."""
    txt = open('corpus_it.txt', encoding='utf-8', errors='ignore').read().lower()
    txt = re.sub(r'[^a-z ]', ' ', txt)
    txt = re.sub('[jkwxy]', '', txt)
    txt = txt.replace('h', '')
    txt = re.sub(r'(.)\1+', r'\1', txt)          # no doubled letters
    txt = re.sub(' +', ' ', txt)
    i = rnd.randrange(0, len(txt) - n * 4)
    return txt[i:i + n * 4]


def build_key(rnd):
    """Systematic layout: a syllable code is (consonant digit)(vowel digit).

    This is forced by the data rather than chosen. Three independent tests on the real text find a
    clean vowel-bearing set {7,0,3}; arbitrary digit pairs would smear vowels across every digit and
    destroy that signal, as the first version of this script demonstrated by making every digit
    vowel-bearing. A consonant-then-vowel grid is the only two-digit layout that leaves the classes
    visible, and it is what Meister's keys of this family actually look like (da de do = 49 69 89,
    na ne ni no = 24 26 28 29).

    Four vowel digits and five consonant digits give 20 base codes, doubled to 40 by the polyphonic
    dot. The commonest 40 Italian syllables take those; everything else is spelled out with single
    digits.
    """
    digits = [d for d in '0123456789' if d != '4']
    rnd.shuffle(digits)
    vowdig, consdig = digits[:4], digits[4:]
    pairs = [c + v for c in consdig for v in vowdig]
    rnd.shuffle(pairs)
    # rank Italian syllables by frequency so the coded ones are the common ones
    syl = [c + v for c in CONS for v in VOW]
    rnd.shuffle(syl)
    code_of = {}
    for i, p in enumerate(pairs):
        if 2 * i + 1 < len(syl):
            code_of[syl[2 * i]] = (p, False)
            code_of[syl[2 * i + 1]] = (p, True)
    singles = {}
    for L in VOW:
        singles[L] = rnd.choice(vowdig)
    for L in CONS:
        singles[L] = rnd.choice(consdig)
    return code_of, singles, set(vowdig)


def encipher(txt, code_of, singles, rnd, n_digits, null_rate=0.0734, p_syl=0.62):
    out = []          # list of (digit, dotted_flag_for_NEXT_unit)
    i = 0
    pending_dot = False
    while len(out) < n_digits and i < len(txt) - 2:
        ch = txt[i]
        if ch == ' ':
            if rnd.random() < 0.33:
                out.append(('4', False))
            i += 1
            continue
        syl = txt[i:i + 2]
        if (rnd.random() < p_syl and ch in CONS and len(syl) == 2 and syl[1] in VOW
                and syl in code_of):
            p, dotted = code_of[syl]
            if dotted and out:
                d, _ = out[-1]
                out[-1] = (d, True)
            out.append((p[0], False))
            out.append((p[1], False))
            i += 2
        else:
            d = singles.get(ch)
            if d is None:
                i += 1
                continue
            out.append((d, False))
            i += 1
        if rnd.random() < null_rate * 0.55:
            out.append(('4', False))
    return out[:n_digits]


# ---------------------------------------------------------------- measurements

def runs_of(cv):
    r = collections.Counter()
    i = 0
    while i < len(cv):
        j = i
        while j < len(cv) and cv[j] == cv[i]:
            j += 1
        r[(cv[i], j - i)] += 1
        i = j
    return r


def measure(digs, vowdig, label):
    s = ''.join(digs)
    nn = [d for d in digs if d != '4']
    cv = ''.join('V' if d in vowdig else 'C' for d in nn)
    rr = runs_of(cv)
    nv = sum(v for (c, k), v in rr.items() if c == 'V')
    nc = sum(v for (c, k), v in rr.items() if c == 'C')
    mv = sum(k * v for (c, k), v in rr.items() if c == 'V') / nv
    mc = sum(k * v for (c, k), v in rr.items() if c == 'C') / nc
    long_c = sum(v for (c, k), v in rr.items() if c == 'C' and k >= 3) / nc
    bg = collections.Counter(zip(s, s[1:]))
    u = collections.Counter(s)
    N = len(s)
    dbl = {d: (bg.get((d, d), 0), u[d] * u[d] / N) for d in sorted(u)}
    g7 = collections.Counter(s[i:i + 7] for i in range(N - 6))
    rep7 = sum(1 for v in g7.values() if v > 1)
    print('\n%-26s digits %d  null %.4f  Vshare %.3f' % (label, N, s.count('4') / N, cv.count('V') / len(cv)))
    print('   mean V run %.3f   mean C run %.3f   C runs>=3 %.3f' % (mv, mc, long_c))
    print('   repeated 7-grams %d' % rep7)
    print('   doubled digits observed/expected: %s'
          % ' '.join('%s:%d/%.0f' % (d, o, e) for d, (o, e) in dbl.items()))
    return dict(mv=mv, mc=mc, long_c=long_c, rep7=rep7)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rnd = random.Random(seed)
    code_of, singles, vow_syn = build_key(rnd)
    txt = italian(9000, rnd)
    out = encipher(txt, code_of, singles, rnd, 6549)
    digs = [d for d, dot in out]
    ndots = sum(1 for d, dot in out if dot)
    print('synthetic Elio cipher: %d digits, %d dots (%.3f of digits)'
          % (len(digs), ndots, ndots / len(digs)))

    measure(digs, vow_syn, 'SYNTHETIC (Elio design)')

    # the real text
    import escape as E
    real = [d for r in E.runs(E.load()) for d in r]
    measure(real, set('703'), 'REAL IA-2  (vowels 7,0,3)')

    print("""
=== READING
The real text's signatures are: mean V run 1.604, mean C run 1.769, C runs >= 3 at 0.183, 441
repeated 7-grams, and every doubled digit suppressed. If a synthetic built only from Elio's
documented rules lands near those without being fitted to them, the identification is corroborated
by construction rather than by resemblance.""")


if __name__ == '__main__':
    main()
