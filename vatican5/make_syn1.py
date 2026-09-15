"""Synthetic test in the style of Meister key no.1 (Montepulciano 1539-42):
  polyphonic digits mixing a vowel with consonants, a null at (some) word ends, a single-digit code,
  2-digit syllables, a dotted series 'sa se si so' = X^ + digit (dot on the preceding digit),
  and a dotted series 'ra re ri ro' = digit with dot.  Writes syn1/cipher.txt, plain.txt, key.txt"""
import random, pathlib, re, shutil, sys
HERE = pathlib.Path(__file__).parent
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
nullrate = float(sys.argv[2]) if len(sys.argv) > 2 else 0.45
rnd = random.Random(seed)
text = (HERE / 'corpus_it.txt').read_text(encoding='utf8')
start = len(text) * 2 // 3 + rnd.randrange(100000, 400000)
words = text[start:start + 60000].split()
digits = list('0123456789'); rnd.shuffle(digits)
groups = ['ac', 'eu', 'id', 'ot', 'bfg', 'ln', 'prz', 'ms', 'hq']   # 9 letter groups
NULL = digits[9]
letter = {}
for g, d in zip(groups, digits[:9]):
    for ch in g: letter[ch] = d
# syllable codes: 2-digit for da de do, na ne ni no, ta te ti, qua que qui ; single-digit-ish for che/non
pairs = [f'{a}{b}' for a in '0123456789' for b in '0123456789' if a != b and NULL not in (a, b)]
rnd.shuffle(pairs)
syl = {}
for s in ['da', 'de', 'do', 'na', 'ne', 'ni', 'no', 'ta', 'te', 'ti', 'qua', 'que', 'qui', 'che', 'non', 'per', 'con']:
    syl[s] = pairs.pop()
# dotted series: sa se si so -> dot on the PRECEDING digit, then digit X  (encoded as: prev token gets '^', then X)
sdig = rnd.sample([d for d in '0123456789' if d != NULL], 4)
sa = dict(zip(['sa', 'se', 'si', 'so'], sdig))
# ra re ri ro -> digit with a dot on itself
rdig = rnd.sample([d for d in '0123456789' if d != NULL], 4)
ra = dict(zip(['ra', 're', 'ri', 'ro'], rdig))
toks = []; plain = []; n = 0
for w in words:
    w = re.sub(r'[^a-z]', '', w)
    if not w: continue
    i = 0; enc = []
    while i < len(w):
        done = False
        for L in (3, 2):
            s = w[i:i+L]
            if s in syl and rnd.random() < 0.8:
                enc += list(syl[s]); i += L; done = True; break
            if s in sa and rnd.random() < 0.8:
                if enc: enc[-1] = enc[-1][0] + '^'      # dot on preceding digit
                elif toks: toks[-1] = toks[-1][0] + '^'
                else: enc.append(letter['e']); enc[-1] += '^'
                enc.append(sa[s]); i += L; done = True; break
            if s in ra and rnd.random() < 0.8:
                enc.append(ra[s] + '^'); i += L; done = True; break
        if done: continue
        ch = w[i]
        if ch in letter: enc.append(letter[ch])
        i += 1
    toks += enc; plain.append(w)
    if rnd.random() < nullrate: toks.append(NULL)
    n += len(enc)
    if n >= 6500: break
d = HERE / 'syn1'; d.mkdir(exist_ok=True)
lines = [' '.join(toks[i:i+800]) for i in range(0, len(toks), 800)]
(d / 'cipher.txt').write_text('\n'.join(lines) + '\n')
(d / 'plain.txt').write_text(' '.join(plain))
(d / 'key.txt').write_text(f'letters {letter}\nnull {NULL}\nsyl {syl}\nsa(dot before) {sa}\nra(dotted) {ra}\n')
for f in ('lm5.bin', 'lm5sp.bin'):
    if not (d / f).exists(): shutil.copy(HERE / f, d / f)
print('digits', len(toks), 'words', len(plain)); print(open(d / 'key.txt').read())
