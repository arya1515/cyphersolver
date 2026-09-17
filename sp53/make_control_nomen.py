# Control with a nomenclator: period text, ~frac of words replaced by word-signs drawn from a pool of nwords codes,
# remaining letters under a random homophonic key; total distinct symbols ~ nsym. Writes control_<lang>_nomen*.txt.
import random, re, sys, unicodedata, collections
from homo import ALPHA

def norm_words(t):
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    t = t.replace('j', 'i').replace('w', 'vv')
    return [w for w in re.split(r'[^a-z]+', t) if w]

def make(lang, seed, ntok=507, nsym=130, nwords=40, frac=0.25):
    rnd = random.Random(seed)
    src = {'en': 'letterbooksofsir00pouluoft.txt', 'fr': 'lettresinstructi56mary.txt'}[lang]
    words = norm_words(open(src, encoding='utf-8', errors='ignore').read())
    pos = rnd.randint(50000, len(words) - 2000)
    nletters = nsym - nwords
    freq = collections.Counter(''.join(words[:100000]))
    w = {ch: freq[ch] ** 0.5 for ch in ALPHA}; tot = sum(w.values())
    counts = {ch: max(1, round(nletters * w[ch] / tot)) for ch in ALPHA}
    while sum(counts.values()) > nletters:
        ch = max(counts, key=lambda c: counts[c]); counts[ch] -= 1
    while sum(counts.values()) < nletters:
        counts[rnd.choice(ALPHA)] += 1
    nums = list(range(1, nsym + 1)); rnd.shuffle(nums)
    key = {}
    for ch in ALPHA:
        for _ in range(counts[ch]): key[nums.pop()] = ch
    codes = nums[:]           # remaining numbers are word-signs
    inv = collections.defaultdict(list)
    for n, ch in key.items(): inv[ch].append(n)
    toks = []; plain = []; wordmap = {}
    i = pos
    while len(toks) < ntok:
        wd = words[i]; i += 1
        if rnd.random() < frac and len(wd) > 2:
            if wd not in wordmap:
                if not codes: continue
                wordmap[wd] = codes.pop() if rnd.random() < 0.5 else rnd.choice(list(wordmap.values()) or codes)
            toks.append(wordmap[wd]); plain.append('[' + wd + ']')
        else:
            for ch in wd:
                if ch in inv: toks.append(rnd.choice(inv[ch])); plain.append(ch)
    toks = toks[:ntok]
    open(f'control_{lang}_nomen.txt', 'w').write('# control with nomenclator\n' + ';'.join(f'{x:02d}' for x in toks) + ';\n')
    open(f'control_{lang}_nomen_key.txt', 'w').write('\n'.join(f'{n}\t{ch}' for n, ch in sorted(key.items())) +
        '\n' + '\n'.join(f'{n}\t[{wd}]' for wd, n in sorted(wordmap.items(), key=lambda x: x[1])) + '\n')
    open(f'control_{lang}_nomen_plain.txt', 'w').write(''.join(plain) + '\n')
    nw = sum(1 for p in plain if p.startswith('['))
    print(lang, 'tokens', len(toks), 'distinct', len(set(toks)), 'word tokens', nw, 'word codes used', len(set(wordmap.values())))

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for lang in ('en', 'fr'): make(lang, seed)
