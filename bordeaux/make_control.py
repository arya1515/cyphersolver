# Matched synthetic control for the 1653 Bordeaux cipher: same symbol inventory and design, a Bordeaux despatch
# (Guizot vol. 2 appendix, 28 June 1654) as plaintext, ~810 tokens.
import re, random, unicodedata, collections, sys
from solver import CONS, VOW, load_tokens, series_of, LETFREQ, OVERBAR, UMLAUT

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DESIGN = sys.argv[2] if len(sys.argv) > 2 else 'A'
NOISE = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0   # fraction of syllable tokens whose diacritic is misread   # A: syllables over ' then ¨; B: ' numbers are letters, syllables ¨ only
random.seed(seed)
raw = open('guizot_docs_raw.txt', encoding='utf-8').read()
i = raw.find("J'ai laiss")
txt = raw[i:i + 12000]
txt = unicodedata.normalize('NFD', txt); txt = ''.join(c for c in txt if unicodedata.category(c) != 'Mn').lower()
words = re.findall(r'[a-z]+', txt)

real = load_tokens('ciphertext.txt')
cnt = collections.Counter(real)
letsyms = sorted({t for t in cnt if (lambda s, n: s == 'g' or s in '-=' or (s == '0' and n <= 45) or (DESIGN == 'B' and s == "'"))(*series_of(t))})
letters = list(LETFREQ)
alloc = {c: 1 for c in letters}
w = [LETFREQ[c] for c in letters]
for _ in range(len(letsyms) - len(letters)):
    alloc[random.choices(letters, w)[0]] += 1
random.shuffle(letsyms)
key = {}
homs = collections.defaultdict(list)
k = 0
for c in letters:
    for _ in range(alloc[c]):
        key[letsyms[k]] = c; homs[c].append(letsyms[k]); k += 1
U = sorted(set([c + v for c in CONS if c != 'q' for v in VOW] + ['qua', 'que', 'qui', 'quo'] +
               ['est', 'et', 'il', 'on', 'pour', 'des', 'ou']))
slots = [f"{n}'" for n in range(25, 100)] + [f"{n}{UMLAUT}" for n in range(1, 100)]
if DESIGN == 'B':
    slots = [f"{n}{UMLAUT}" for n in range(5, 100)]
    slots = [s for s in slots if random.random() > 0.08]
else:
    slots = [s for s in slots if random.random() > 0.25]
syl = {}
for u, s in zip(U, slots):
    key[s] = u; syl[u] = s
wc = collections.Counter(w_ for w_ in words if len(w_) >= 6)
nomen = {}
for j, (w_, _) in enumerate(wc.most_common(9)):
    code = f"{79 + 2*j}{OVERBAR}"
    nomen[w_] = code; key[code] = w_
PSYL = 0.32 if DESIGN == 'B' else 0.92
out = []
plain = []
for w_ in words:
    if len(out) >= 810:
        break
    plain.append(w_)
    if w_ in nomen:
        out.append(nomen[w_]); continue
    i = 0
    while i < len(w_):
        done = False
        if random.random() < PSYL:
            for L in (3, 2):
                if w_[i:i+L] in syl and (L == 2 or w_[i:i+L] in ('qua', 'que', 'qui', 'quo')):
                    out.append(syl[w_[i:i+L]]); i += L; done = True; break
        if not done:
            out.append(random.choice(homs[w_[i]])); i += 1
if NOISE:
    alt = {"'": UMLAUT, UMLAUT: "'"}
    for j, t in enumerate(out):
        s_, n_ = series_of(t)
        if s_ in alt and random.random() < NOISE:
            out[j] = f'{n_}' + (alt[s_] if random.random() < 0.5 else '')
name = f'control{seed}' + ('B' if DESIGN == 'B' else '') + (f'N{int(NOISE*100)}' if NOISE else '')
open(name + '.txt', 'w', encoding='utf-8').write('# synthetic control, see make_control.py\n' +
    '\n'.join(' '.join(out[j:j+13]) for j in range(0, len(out), 13)) + '\n')
open(name + '_key.txt', 'w', encoding='utf-8').write('\n'.join(f'{k}\t{v}' for k, v in sorted(key.items())) + '\n')
open(name + '_plain.txt', 'w', encoding='utf-8').write(' '.join(plain) + '\n')
c2 = collections.Counter(out)
print(name, len(out), 'tokens', len(c2), 'distinct;', 'letters', sum(v for t, v in c2.items() if t in letsyms),
      'syl', sum(v for t, v in c2.items() if series_of(t)[0] in ("'", UMLAUT)), 'distinct syl slots',
      sum(1 for t in c2 if series_of(t)[0] in ("'", UMLAUT)))
