# Matched controls for no.78: (a) alphabetical-block homophonic key over 1..141 (letters in order, block sizes
# drawn to give ~132 used symbols), (b) random homophonic key with the same symbol counts. Period English
# (Poulet letter-books) or French (Labanoff) plaintext, 507 tokens. Writes control_<lang>_<kind>.txt and _key/_plain.
import random, re, sys, unicodedata, collections
from homo import ALPHA

def norm(t):
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    t = t.replace('j', 'i').replace('w', 'vv')
    return re.sub(r'[^a-z]', '', t)

def make(lang, kind, seed, ntok=507, nsym=141):
    rnd = random.Random(seed)
    src = {'en': 'letterbooksofsir00pouluoft.txt', 'fr': 'lettresinstructi56mary.txt'}[lang]
    t = norm(open(src, encoding='utf-8', errors='ignore').read())
    pos = rnd.randint(200000, len(t) - 5000)
    plain = t[pos:pos + ntok]
    # homophone counts per letter roughly proportional to sqrt(frequency), total nsym
    freq = collections.Counter(t[:400000])
    w = {ch: (freq[ch] ** 0.5) for ch in ALPHA}
    tot = sum(w.values())
    counts = {ch: max(1, round(nsym * w[ch] / tot)) for ch in ALPHA}
    while sum(counts.values()) > nsym:
        ch = max(counts, key=lambda c: counts[c]); counts[ch] -= 1
    while sum(counts.values()) < nsym:
        ch = rnd.choice(ALPHA); counts[ch] += 1
    key = {}
    if kind == 'blocks':
        n = 1
        for ch in ALPHA:
            for _ in range(counts[ch]): key[n] = ch; n += 1
    else:
        nums = list(range(1, nsym + 1)); rnd.shuffle(nums)
        for ch in ALPHA:
            for _ in range(counts[ch]): key[nums.pop()] = ch
    inv = collections.defaultdict(list)
    for n, ch in key.items(): inv[ch].append(n)
    toks = [rnd.choice(inv[ch]) for ch in plain]
    open(f'control_{lang}_{kind}.txt', 'w').write('# control\n' + ';'.join(f'{x:02d}' for x in toks) + ';\n')
    open(f'control_{lang}_{kind}_key.txt', 'w').write('\n'.join(f'{n}\t{ch}' for n, ch in sorted(key.items())) + '\n')
    open(f'control_{lang}_{kind}_plain.txt', 'w').write(plain + '\n')
    print(lang, kind, 'tokens', len(toks), 'distinct', len(set(toks)))

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for lang in ('en', 'fr'):
        for kind in ('blocks', 'homo'):
            make(lang, kind, seed)
