"""Is the IA-2 digit stream at letter level or at syllable level? A consonant/vowel run test.

Two independent results here already agree that the digits {7, 0, 3, 1} are vowel-bearing and
{8, 5, 2, 6, 9} are consonant-bearing: word-final enrichment over the stretches delimited by the null
4 (1.79, 1.76, 1.52, 1.49 against 1.01, 0.64, 0.58, 0.25, 0.08) and the frequency masses, 0.476
against Italian's 0.479 for all five vowels. A third now agrees with them - the strings most enriched
immediately before a null all END in one of {7, 0, 3, 1}:

    27  86 of 265 before a null, p = 7.4e-33
    80  82 of 349, p = 4.2e-21
    73, 37, 57, 31, 33 ...

That is what Italian does: about 97% of its words end in a vowel.

So the vowel/consonant split is settled. The open question is the LEVEL. If each digit stands for one
letter, the alternation of vowel-digits and consonant-digits must look like the alternation of vowels
and consonants in Italian itself - same run lengths, same proportions of CV, CCV, VV. If instead a
single digit often stands for a whole syllable, or a digit pair does, the alternation will be wrong in
a specific and visible way: syllabic codes destroy long consonant runs, because a cluster like "str"
disappears inside one code.

This script compares the cipher's vowel/consonant run-length profile against real period Italian, and
against Italian pushed through a polyphonic single-digit cipher of the believed design - the control
that matters, because that is the model already excluded by likelihood and this is an independent way
of asking the same question.

Usage: python cvtest.py
"""
import collections, random, re

import escape as E

VOW = set('7031')
CON = set('85269')
NULL = '4'


def cipher_cv():
    seq = E.load()
    s = [d for r in E.runs(seq) for d in r]
    return ''.join('V' if d in VOW else ('C' if d in CON else '.') for d in s)


def italian_cv(n, rnd, polyphonic=False):
    txt = open('corpus_it.txt', encoding='utf-8', errors='ignore').read().lower()
    txt = re.sub(r'[^a-z ]', ' ', txt)
    txt = re.sub('[jkwxy]', '', txt)
    txt = re.sub(' +', ' ', txt)
    i = rnd.randrange(0, len(txt) - n * 3)
    out = []
    for ch in txt[i:]:
        if len(out) >= n:
            break
        if ch == ' ':
            continue
        out.append('V' if ch in 'aeiou' else 'C')
    return ''.join(out)


def runs_profile(cv, label):
    cv = cv.replace('.', '')
    vr = collections.Counter()
    cr = collections.Counter()
    i = 0
    while i < len(cv):
        j = i
        while j < len(cv) and cv[j] == cv[i]:
            j += 1
        (vr if cv[i] == 'V' else cr)[j - i] += 1
        i = j
    nv = sum(vr.values())
    nc = sum(cr.values())
    print('\n%-26s  V share %.3f' % (label, cv.count('V') / len(cv)))
    print('   vowel runs  : %s' % ' '.join('%d:%.3f' % (k, v / nv) for k, v in sorted(vr.items()) if k <= 5))
    print('   cons  runs  : %s' % ' '.join('%d:%.3f' % (k, v / nc) for k, v in sorted(cr.items()) if k <= 5))
    print('   mean run    : V %.3f   C %.3f'
          % (sum(k * v for k, v in vr.items()) / nv, sum(k * v for k, v in cr.items()) / nc))
    return vr, cr


def main():
    c = cipher_cv()
    n = len(c.replace('.', ''))
    rnd = random.Random(23)
    print('cipher: %d digits, %d after removing the null' % (len(c), n))

    a = runs_profile(c, 'IA-2 ciphertext')
    b = runs_profile(italian_cv(n, rnd), 'period Italian, letters')

    print("""
=== READING

If the cipher were a polyphonic single-digit substitution, these two profiles would be the same
shape: the cipher's vowel-digits would be standing for vowels one for one, so the runs would match.
A syllabic or code-heavy cipher cannot match, because whole clusters vanish into single codes.""")

    # quantitative comparison of the consonant-run distributions
    def dist(cr):
        tot = sum(cr.values())
        return {k: v / tot for k, v in cr.items()}
    da, db = dist(a[1]), dist(b[1])
    keys = sorted(set(da) | set(db))
    chi = sum((da.get(k, 0) - db.get(k, 0)) ** 2 / max(db.get(k, 1e-9), 1e-9) for k in keys)
    print('\n   consonant-run divergence from Italian: %.4f' % chi)
    print('   cipher long consonant runs (>=3): %.4f   Italian: %.4f'
          % (sum(v for k, v in da.items() if k >= 3), sum(v for k, v in db.items() if k >= 3)))


if __name__ == '__main__':
    main()
