"""Synthetic test: encipher period Italian with a Meister-176/2-style variable-length polyphonic key
and write syn/cipher.txt (+ syn/key.txt) so vsolve can be tested on a known answer."""
import random, pathlib, re, shutil, sys
HERE = pathlib.Path(__file__).parent
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rnd = random.Random(seed)
text = (HERE / 'corpus_it.txt').read_text(encoding='utf8')
# take a slice from the last third (LM built on whole corpus; fine for a feasibility test)
start = len(text) * 2 // 3 + rnd.randrange(100000)
words = text[start:start + 60000].split()
VOW = 'aeiou'; CONS = 'bcdfghlmnpqrstz'
digits = list(range(10)); rnd.shuffle(digits)
vd = {v: digits[i] for i, v in enumerate(VOW)}
cons_digits = digits[5:]
cd = {}
groups = ['bc', 'dfg', 'lp', 'nm', 'rtz', 'sqh']
rnd.shuffle(groups)
for g, d in zip(groups, cons_digits + [cons_digits[0]]):
    for c in g: cd[c] = d
# syllable table: 7 consonants x 4 vowels (a e i o) as unique 2-digit codes; dotted codes for others
syl_cons = rnd.sample('cdlmnrst', 7)
pairs = [f'{a}{b}' for a in range(10) for b in range(10) if a != b]
rnd.shuffle(pairs)
syl = {}
for c in syl_cons:
    for v in 'aeio':
        syl[c + v] = pairs.pop()
dot_words = ['che', 'chi', 'non', 'qua', 'que', 'qui', 'ta', 'te', 'ti', 'to', 'per', 'con']
dot_digit = rnd.choice(cons_digits)
for w in dot_words:
    syl[w] = f'{dot_digit}^{pairs.pop()}'
out = []; n = 0; plain = []
for w in words:
    w = re.sub(r'[^a-z]', '', w)
    if not w: continue
    i = 0; enc = []
    while i < len(w):
        done = False
        for L in (3, 2):
            s = w[i:i+L]
            if s in syl and rnd.random() < 0.75:
                enc.append(syl[s]); i += L; done = True; break
        if done: continue
        ch = w[i]
        if ch in vd: enc.append(str(vd[ch]))
        elif ch in cd: enc.append(str(cd[ch]))
        i += 1
    out.append(' '.join(enc)); plain.append(w)
    n += sum(len(e.replace('^', '')) for e in enc)
    if n >= 6500: break
d = HERE / 'syn'; d.mkdir(exist_ok=True)
# vsolve tokens: digit + optional '^' meaning dot on that digit
toks = []
for e in ' '.join(out).split():
    if '^' in e:
        a, b = e.split('^'); toks.append(a + '^'); toks += list(b)
    else: toks += list(e)
lines = [' '.join(toks[i:i+800]) for i in range(0, len(toks), 800)]
(d / 'cipher.txt').write_text('\n'.join(lines) + '\n')
(d / 'plain.txt').write_text(' '.join(plain))
(d / 'key.txt').write_text('vowels ' + str(vd) + '\ncons ' + str(cd) + '\nsyl ' + str(syl) + '\n')
if not (d / 'lm5.bin').exists(): shutil.copy(HERE / 'lm5.bin', d / 'lm5.bin')
print('digits', n, 'words', len(plain)); print(open(d / 'key.txt').read())
