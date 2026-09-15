"""synk2.py -- synthetic cipher in the family of Meister (1906) p.176 key no. 2 ("Cifra ultima con Mons.
Poggio"), renumbered at random, with the features observed in IA-2: null 4 after ~40% of words, no code
containing the null, 5 vowel singles, consonant-group singles (polyphonic), 8 consonant-vowel syllable
series as digit pairs, dotted variants (dot on the antecedent) for ta/qua/che series, a few nomenclature
codes. Plaintext = held-out period Italian from corpus_it.txt in cipher orthography.

usage: python synk2.py <seed> [ndigits=6550]  -> syn_k2_<seed>.json (runs), syn_k2_<seed>_key.json
"""
import sys, json, random, re, pathlib
from lmns import normalize_cipher_orthography
HERE = pathlib.Path(__file__).parent
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NDIG = int(sys.argv[2]) if len(sys.argv) > 2 else 6550
rng = random.Random(seed)
NULL = '4'
digits = [d for d in '0123456789' if d != NULL]

def make_key():
    rng.shuffle(digits)
    key = {}                       # plaintext element -> code (string of digits, '.' prefix = dot on antecedent)
    vowels = 'aeiou'
    for v, d in zip(vowels, digits[:5]): key[v] = d
    singles_left = digits[5:]      # 4 digits
    groups = ['bc', 'lp', 'nm', 'rt', 'dfg', 'sz']
    rng.shuffle(groups)
    for g, d in zip(groups[:3], singles_left[:3]): key[g] = d
    key['et'] = singles_left[3]
    used_pairs = set()
    def fresh_pair():
        while True:
            p = rng.choice(digits) + rng.choice(digits)
            if p not in used_pairs:
                used_pairs.add(p); return p
    for g in groups[3:]: key[g] = fresh_pair()
    # syllable series: prefix digit + 4 distinct suffix digits (block structure as in key 2)
    for c in 'cdlmnrs':
        pre = rng.choice(digits)
        sufs = rng.sample(digits, 4)
        for v, s in zip('aeio', sufs):
            p = pre + s
            if p in used_pairs:
                p = fresh_pair()
            used_pairs.add(p); key[c + v] = p
    # dotted series (dot on antecedent) reuse pairs of other series, like ta = .80 = na with a dot
    base_t = [key['n' + v] for v in 'aeio']; base_q = [key['s' + v] for v in 'aei']; base_c = [key['r' + v] for v in 'aei']
    for v, p in zip('aeio', base_t): key['t' + v] = '.' + p
    for w, p in zip(['qua', 'que', 'qui'], base_q): key[w] = '.' + p
    for w, p in zip(['che', 'chi', 'non'], base_c): key[w] = '.' + p
    key['nostrosignore'] = '.' + fresh_pair(); key['suamaesta'] = '.' + fresh_pair()
    key['francia'] = rng.choice(digits) * 3
    return key

def encode_word(w, key, elems):
    out = []
    i = 0
    while i < len(w):
        for L in (13, 9, 7, 3, 2, 1):
            piece = w[i:i+L]
            if piece in elems:
                out.append(key[piece]); i += L; break
        else:
            i += 1     # unencodable letter (should not happen)
    return out

def main():
    key = make_key()
    GROUPS = ['bc', 'lp', 'nm', 'rt', 'dfg', 'sz']
    letter_to_group = {ch: g for g in GROUPS for ch in g}
    elems = set(key) | set(letter_to_group)
    kfull = dict(key)
    for ch, g in letter_to_group.items(): kfull[ch] = key[g]
    raw = (HERE / 'corpus_it.txt').read_text(encoding='utf-8')
    words = raw[-60000:].split()
    start = rng.randrange(0, len(words) - 3000)
    toks = []; plain = []; units = []
    ndig = 0; i = start
    while ndig < NDIG:
        w = normalize_cipher_orthography(words[i]); i += 1
        if not w: continue
        codes = encode_word(w, kfull, elems)
        for code in codes:
            dotted = code.startswith('.'); code = code.lstrip('.')
            if dotted:
                if toks: toks[-1] = toks[-1] + '^.'
            for k, d in enumerate(code):
                toks.append(d)
            units.append(code); ndig += len(code)
        plain.append(w)
        if rng.random() < 0.4:
            toks.append(NULL); ndig += 1
    runs = [toks]
    json.dump(runs, open(HERE / f'syn_k2_{seed}.json', 'w'))
    json.dump({'key': key, 'plain': ' '.join(plain), 'units': units}, open(HERE / f'syn_k2_{seed}_key.json', 'w'))
    inv = {}
    for e, c in key.items(): inv.setdefault(c.lstrip('.'), []).append(('.' if c.startswith('.') else '') + e)
    print('digits', ndig, 'words', len(plain), 'units', len(units))
    print('key by code:', ' '.join(f'{c}={"/".join(v)}' for c, v in sorted(inv.items(), key=lambda kv: (len(kv[0]), kv[0]))))
    print('plaintext starts:', ' '.join(plain[:30]))

if __name__ == '__main__':
    main()
