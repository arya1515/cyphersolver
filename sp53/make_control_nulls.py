# Control with nulls and a nomenclator: French period text, 3 null symbols inserted at ~8 % of positions,
# ~20 word tokens under word-signs, letters under a random homophonic key; ~130 symbols, 507 tokens.
import random, re, sys, unicodedata, collections
from homo import ALPHA
from make_control_nomen import norm_words

def make(lang, seed, ntok=507, nsym=130, nwords=30, nnull=3, pnull=0.08, frac=0.2):
    rnd = random.Random(seed)
    src = {'en': 'letterbooksofsir00pouluoft.txt', 'fr': 'lettresinstructi56mary.txt'}[lang]
    words = norm_words(open(src, encoding='utf-8', errors='ignore').read())
    pos = rnd.randint(50000, len(words) - 2000)
    nletters = nsym - nwords - nnull
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
    nulls = [nums.pop() for _ in range(nnull)]
    codes = nums[:]
    inv = collections.defaultdict(list)
    for n, ch in key.items(): inv[ch].append(n)
    toks = []; plain = []; wordmap = {}; i = pos
    while len(toks) < ntok:
        wd = words[i]; i += 1
        if rnd.random() < frac and len(wd) > 2 and codes:
            if wd not in wordmap: wordmap[wd] = codes.pop()
            toks.append(wordmap[wd]); plain.append('[' + wd + ']')
        else:
            for ch in wd:
                if ch in inv:
                    toks.append(rnd.choice(inv[ch])); plain.append(ch)
                    if rnd.random() < pnull: toks.append(rnd.choice(nulls)); plain.append('_')
    toks = toks[:ntok]; plain = plain[:ntok]
    open(f'control_{lang}_nulls.txt', 'w').write('# control with nulls and nomenclator\n' + ';'.join(f'{x:02d}' for x in toks) + ';\n')
    open(f'control_{lang}_nulls_key.txt', 'w').write('\n'.join(f'{n}\t{ch}' for n, ch in sorted(key.items())) +
        '\n' + '\n'.join(f'{n}\tNULL' for n in nulls) + '\n' + '\n'.join(f'{n}\t[{wd}]' for wd, n in sorted(wordmap.items(), key=lambda x: x[1])) + '\n')
    open(f'control_{lang}_nulls_plain.txt', 'w').write(''.join(plain) + '\n')
    print(lang, 'tokens', len(toks), 'distinct', len(set(toks)), 'nulls', plain.count('_'), 'words', sum(1 for p in plain if p.startswith('[')))

if __name__ == '__main__':
    make('fr', int(sys.argv[1]) if len(sys.argv) > 1 else 13)
