# Design-faithful control: a random 367-group "petit chiffre" whose unit inventory is a subset of Bazeries'
# Grand Chiffre de 1691 (letters with 2-3 homophones, CV syllables, words, nulls), numbered so that letters and
# nulls sit below 100 (the target letter has 46 % of its tokens below 100), everything else above; enciphered
# with the greedy habits visible in the 19 Aug 1691 despatch (word/stem entry if available, else syllable, else
# letter; nulls ~3 %).  Plaintext: Catinat to Feuquieres, Suze, 12 Jan 1691 (control_plain.txt), trimmed to 418.
# usage: python make_control_gc.py seed -> control_gc.txt, control_gc_key.txt, control_gc_units.txt
import random, sys, collections
from gc_inventory import load, norm
table, LET, SYL, WOR, NUL, UNK = load()

def build_code(rnd, n_syl=60, n_words=190):
    code = {}
    lows = list(range(1, 100)); rnd.shuffle(lows)
    for ch in 'abcdefghijlmnopqrstuvxyz':
        k = 3 if ch in 'eaisnrt' else 2
        code[ch] = [lows.pop() for _ in range(k)]
    for i in range(4):
        code['<null%d>' % i] = [lows.pop()]
    highs = list(range(100, 367)); rnd.shuffle(highs)
    syls = sorted(SYL); rnd.shuffle(syls)
    for s in syls[:n_syl]:
        code[s] = [highs.pop()]
    words = sorted(WOR); rnd.shuffle(words)
    keep = ['veill', 'pignerol', 'suze', 'turin', 'canon', 'caval', 'infanterie', 'troupe', 'regiment', 'de', 'le', 'la',
            'que', 'et', 'vous', 'les', 'ne', 'pour', 'jour', 'chemin', 'attaque', 'arriv', 'quartier']
    words = keep + [w for w in words if w not in keep]
    for w in words[:n_words]:
        code[w] = [highs.pop()]
    for i in range(6):
        code['<hnull%d>' % i] = [highs.pop()]
    return code

def encode(text, code, rnd):
    out = []; units = []
    wordkeys = sorted((k for k in code if len(k) > 1 and not k.startswith('<')), key=len, reverse=True)
    for w in text.split():
        i = 0
        while i < len(w):
            rest = w[i:]
            u = None
            for k in wordkeys:
                if len(k) >= 3 and rest.startswith(k):
                    u = k; break
            if u is None and len(rest) >= 2 and rest[:2] in code and len(rest[:2]) == 2:
                u = rest[:2]
            if u is None:
                u = w[i]
            if u not in code:
                # letter missing (k, w): skip
                i += 1; continue
            out.append(rnd.choice(code[u])); units.append(u)
            i += len(u)
            if rnd.random() < 0.03:
                nk = rnd.choice([k for k in code if k.startswith('<')])
                out.append(rnd.choice(code[nk])); units.append(nk)
    return out, units

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    plain = norm(open('control_plain.txt', encoding='utf-8').read())
    rnd = random.Random(seed)
    code = build_code(rnd)
    toks, units = encode(plain, code, rnd)
    toks, units = toks[:418], units[:418]
    with open('control_gc.txt', 'w', encoding='utf-8') as f:
        f.write('# design-faithful control (Grand Chiffre inventory), seed %d\n' % seed)
        for i in range(0, len(toks), 13):
            f.write(' '.join(map(str, toks[i:i+13])) + '\n')
    inv = {}
    for u, ns in code.items():
        for n in ns:
            inv[n] = '' if u.startswith('<') else u
    with open('control_gc_key.txt', 'w', encoding='utf-8') as f:
        for n in sorted(inv):
            f.write('%d\t%s\n' % (n, inv[n]))
    open('control_gc_units.txt', 'w', encoding='utf-8').write(' '.join(units))
    low = sum(1 for t in toks if t < 100)
    c = collections.Counter(toks)
    print('tokens', len(toks), 'distinct', len(c), 'low tokens', low, 'low distinct', len({t for t in toks if t < 100}),
          'singletons', sum(1 for v in c.values() if v == 1))
    print(' '.join(units[:60]))
