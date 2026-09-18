"""Cumulative alignment of a cipher figure stream against a known plaintext.

The two sides of the f.18/f.19 crib are not line-for-line, so labelling has to be driven by
landmarks rather than by line number. The code groups are the landmarks: each one is a word whose
position in the plaintext can be located, which re-synchronises the streams. Between two landmarks
the figures and the letters are matched by a DP that allows a figure to stand for one letter
(ordinary homophone), two letters (a doubled figure such as the ss found on f.18r), or for a box to
have been merged by the segmenter and cover several letters.

Usage:
    python align.py cipher_f18.txt f19_plain.txt
where the cipher file is one line of space-separated figure tokens per manuscript line (code
groups written as their numbers) and the plaintext file is the clear text, free-form.
"""
import sys, re, json, unicodedata

CODES = {'12': 'il', '13': 'qui', '14': 'que', '17': 'car', '24': 'nostre', '25': 'nous',
         '26': 'uous', '34': 'ainsi', '35': 'parceque', '40': 'lui', '43': 'point',
         '47': 'tous', '48': 'aussi', '51': 'pas', '52': 'plustost'}

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    t = t.replace('v', 'u').replace('j', 'i').replace('w', 'u')
    return re.sub(r'[^a-z]', '', t)

def landmarks(figs, plain_words):
    """Pair each code figure with the next matching word in the plaintext, in order."""
    out = []
    wi = 0
    for fi, f in enumerate(figs):
        if f not in CODES: continue
        want = norm(CODES[f])
        j = wi
        while j < len(plain_words) and norm(plain_words[j]) != want:
            j += 1
        if j < len(plain_words):
            out.append((fi, j)); wi = j + 1
    return out

def letter_offsets(words):
    off = []; n = 0
    for w in words:
        off.append(n); n += len(norm(w))
    off.append(n)
    return off

def align(figs, plain):
    words = plain.split()
    offs = letter_offsets(words)
    letters = ''.join(norm(w) for w in words)
    lm = landmarks(figs, words)
    print(f'figures {len(figs)}  letters {len(letters)}  landmarks {len(lm)}')
    if not lm:
        print('no landmarks: cannot anchor'); return []
    segs = []
    prev_f, prev_l = 0, 0
    for fi, wj in lm + [(len(figs), len(words))]:
        lo = offs[wj] if wj < len(offs) else len(letters)
        nf = fi - prev_f
        nl = lo - prev_l
        segs.append({'figs': (prev_f, fi), 'letters': (prev_l, lo), 'n_fig': nf, 'n_let': nl,
                     'ratio': round(nl / nf, 2) if nf else None,
                     'text': letters[prev_l:lo]})
        if fi < len(figs):
            prev_f = fi + 1
            prev_l = lo + len(norm(CODES.get(figs[fi], '')))
    return segs

if __name__ == '__main__':
    figs = []
    for line in open(sys.argv[1], encoding='utf-8'):
        figs += line.split()
    plain = open(sys.argv[2], encoding='utf-8').read()
    for s in align(figs, plain):
        print(f"  figs {s['figs']}  n={s['n_fig']:3d}   letters n={s['n_let']:3d}"
              f"  ratio={s['ratio']}   {s['text'][:60]}")
