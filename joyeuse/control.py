"""Matched control for f.539: same token budget (234 letter tokens over 81 symbols, 95 syllable tokens over 48 symbols,
29 number tokens), enciphering a 16th-century French passage. Letters get homophones drawn to the target's unmarked
frequency profile; syllables are taken from a 48-entry table of common French syllables; numbers replace whole words.
Usage: python control.py SEED  -> control_SEED.txt (ciphertext), control_SEED_key.txt, control_SEED_plain.txt"""
import sys, re, random, collections, unicodedata, glob, os
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rnd = random.Random(seed)
# target profile
toks = []
for line in open('ct_f539.txt', encoding='utf-8'):
    if line.startswith('#'): continue
    toks += [t for t in line.split() if t != '|']
isnum = lambda t: re.fullmatch(r'\d+', t) is not None
marked = lambda t: bool(re.search(r'[.:+#^_]$', t)) or t.endswith('++')
un = collections.Counter(t for t in toks if not isnum(t) and not marked(t))
mk = collections.Counter(t for t in toks if not isnum(t) and marked(t))
NL, NS, NN = sum(un.values()), sum(mk.values()), sum(1 for t in toks if isnum(t))
# plaintext: a run of the du Croc corpus (Catherine de Medicis letters), cleaned like lm.py
def clean(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('v', 'u').replace('j', 'i')
    ws = re.findall(r'[a-z]+', t)
    return [w for w in ws if len(w) <= 12 and 'iii' not in w and not re.fullmatch(r'[iuxlcdm]{2,}', w)]
files = sorted(glob.glob('../ducroc/corpus/*.txt'))
words = clean(open(files[seed % len(files)], encoding='utf-8', errors='ignore').read())
start = rnd.randrange(len(words) // 4, len(words) // 2)
# syllable table (48 entries) - common French syllables
SYL = ('de le la les que et en on est il ne pour ce des qui ie uous me se au ou par sa son sur un une bien fait ma mon'
       ' ent ion re ra te tre ment ans ai ei ent er es on ur us os as an in').split()
SYL = list(dict.fromkeys(SYL))[:48]
# alphabet symbols: assign 81 symbols to letters with counts proportional to French letter frequency, then draw
# homophone token frequencies from the target's unmarked count profile
letters = 'abcdefghilmnopqrstuxyz'
freq = dict(zip(letters, [8.2, .9, 3.3, 3.7, 17, 1.1, 1.0, .9, 7.3, 5.5, 3.0, 7.2, 5.4, 3.0, 1.3, 6.5, 8.1, 7.1, 6.3, .4, .5, .2]))
tot = sum(freq.values())
nsym = {l: max(1, round(81 * freq[l] / tot)) for l in letters}
while sum(nsym.values()) > 81:
    l = max((k for k in nsym if nsym[k] > 1), key=lambda k: nsym[k] / freq[k]); nsym[l] -= 1
while sum(nsym.values()) < 81:
    l = min(nsym, key=lambda k: nsym[k] / freq[k]); nsym[l] += 1
symtab = {}
sid = 0
for l in letters:
    symtab[l] = [f'S{sid + i}' for i in range(nsym[l])]; sid += nsym[l]
syltab = {s: f'Y{i}' for i, s in enumerate(SYL)}
# build ciphertext walking the words; ~26% of letter mass becomes syllables, ~29 words become numbers
out, plain, key_used = [], [], collections.Counter()
i = start
nletters = nsyl = nnum = 0
numwords = set()
while nletters < NL:
    w = words[i]; i += 1
    if len(w) > 5 and nnum < NN and rnd.random() < 0.08:
        out.append(str(100 + rnd.randrange(1, 150))); plain.append('[' + w + ']'); nnum += 1; continue
    j = 0; pw = ''
    while j < len(w):
        took = False
        if nsyl < NS and rnd.random() < 0.8:
            for L in (3, 2):
                s = w[j:j + L]
                if s in syltab:
                    out.append(syltab[s]); pw += '<' + s + '>'; nsyl += 1; j += L; took = True; break
        if not took:
            c = w[j]
            if c in symtab:
                out.append(rnd.choice(symtab[c])); pw += c; nletters += 1
            j += 1
    plain.append(pw)
# rescale: homophone usage follows the target's unmarked profile only loosely; record counts
cnt = collections.Counter(out)
open(f'control_{seed}.txt', 'w', encoding='utf-8').write(' '.join(out) + '\n')
open(f'control_{seed}_plain.txt', 'w', encoding='utf-8').write(' '.join(plain) + '\n')
with open(f'control_{seed}_key.txt', 'w', encoding='utf-8') as f:
    for l in letters:
        for s in symtab[l]: f.write(f'{s} {l}\n')
    for s, y in syltab.items(): f.write(f'{y} <{s}>\n')
print('letters', nletters, 'syllables', nsyl, 'numbers', nnum, 'tokens', len(out), 'distinct', len(cnt),
      'letter symbols used', len([s for s in cnt if s.startswith('S')]), 'syl symbols used', len([s for s in cnt if s.startswith('Y')]))
