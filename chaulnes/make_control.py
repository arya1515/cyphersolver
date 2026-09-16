# Matched synthetic control: encode a period French text with a random code-4-style nomenclator
# (letters with 2-3 homophones, CV syllables in step-10 columns, ~120 words, nulls), keeping ~55% in clear,
# with ~300 code groups in ~11 segments, like the Chaulnes letter.
import random, re, sys, unicodedata, collections
sys.path.insert(0, '.')
from solver import norm, CONS, VOW

def build_code(seed):
    rnd = random.Random(seed)
    code = {}  # unit -> list of numbers
    n = 2
    for ch in 'abcdefghiklmnopqrstuxyz':
        code[ch] = [n, n + 1] + ([n + 2] if ch in 'aeinrst' else [])
        n += len(code[ch])
    # syllable table: 10 columns; each consonant occupies a column run of 5 (a e i o u) starting at a random row
    base = 80
    cols = list(range(10))
    cons = list(CONS)
    rnd.shuffle(cons)
    row_next = [0] * 10
    for i, c in enumerate(cons):
        col = i % 10
        start = base + 10 * row_next[col] + col
        for j, v in enumerate(VOW):
            code[c + v] = [start + 10 * j]
        row_next[col] += 5 + rnd.randint(0, 2)
    used = {x for xs in code.values() for x in xs}
    words = collections.Counter(open('corpus_fr.txt', encoding='utf-8').read().split())
    top = [w for w, _ in words.most_common(200) if len(w) > 1][:120]
    free = [x for x in range(80, 560) if x not in used]
    rnd.shuffle(free)
    for w in top:
        code[w] = [free.pop()]
    for i in range(6):
        code['<null%d>' % i] = [free.pop()]
    return code

def encode(text, code, rnd):
    # greedy: words first (60% of the time when available), else syllables, else letters
    out = []
    words = text.split()
    for w in words:
        if w in code and rnd.random() < 0.6:
            out.append(rnd.choice(code[w])); continue
        i = 0
        while i < len(w):
            if i + 1 < len(w) and w[i:i+2] in code and w[i] in CONS and w[i+1] in VOW:
                out.append(rnd.choice(code[w[i:i+2]])); i += 2
            elif w[i] in code:
                out.append(rnd.choice(code[w[i]])); i += 1
            else:
                i += 1
        if rnd.random() < 0.03:
            out.append(rnd.choice(code['<null%d>' % rnd.randint(0, 5)]))
    return out

def main(seed=7):
    rnd = random.Random(seed)
    code = build_code(seed)
    txt = open('recueil17.txt', encoding='utf-8').read()
    # pick a stretch of an instruction text (skip the front matter)
    t = norm(txt[400000:520000])
    words = t.split()
    segs = []
    pos = rnd.randint(0, 2000)
    ngroups = 0
    lines = []
    while ngroups < 300:
        clear1 = ' '.join(words[pos:pos+rnd.randint(6, 14)]); pos += 12
        n = rnd.randint(4, 40)
        secret = ' '.join(words[pos:pos+n]); pos += n
        groups = encode(secret, code, rnd)
        ngroups += len(groups)
        clear2 = ' '.join(words[pos:pos+rnd.randint(4, 10)]); pos += 7
        lines.append(f'[S{len(lines)}] {clear1} | ' + ' '.join(map(str, groups)) + f' | {clear2}')
        segs.append((clear1, secret, groups, clear2))
    open('control.txt', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    inv = {}
    for u, xs in code.items():
        for x in xs:
            inv[x] = u
    open('control_key.txt', 'w', encoding='utf-8').write('\n'.join(f'{x}\t{u}' for x, u in sorted(inv.items())) + '\n')
    open('control_plain.txt', 'w', encoding='utf-8').write('\n'.join(s[1] for s in segs) + '\n')
    print('groups', ngroups, 'distinct', len({g for s in segs for g in s[2]}))

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
