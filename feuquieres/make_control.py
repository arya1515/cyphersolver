# Matched synthetic control for the Feuquieres letter: encode a period French military letter of the same
# length with a random two-part "petit chiffre" of the design inferred for the target: letters with 2-3
# homophones scattered over 1-99, CV syllables (1-2 numbers each) and ~60 words scattered over 100-366,
# nulls in both blocks; encoding policy tuned to ~46% letter tokens and ~160 distinct groups over ~418 tokens.
# usage: python make_control.py control_plain.txt seed -> control.txt, control_key.txt
import random, re, sys, collections, os
from solver import norm, CONS, VOW
PW = float(os.environ.get('PW', '0.8'))   # prob. of using a word entry when available
PS = float(os.environ.get('PS', '0.9'))   # prob. of using a syllable / letter-group entry when available

def build_code(rnd):
    code = {}
    lows = list(range(1, 100)); rnd.shuffle(lows)
    for ch in 'abcdefghijklmnopqrstuvxyz':
        k = 3 if ch in 'eaisnrtoul' else 2
        code[ch] = [lows.pop() for _ in range(k)]
    for i in range(4):
        code['<null%d>' % i] = [lows.pop()]
    highs = list(range(100, 367)); rnd.shuffle(highs)
    for c in CONS:
        for v in VOW:
            k = 2 if c + v in ('de', 'le', 'la', 'que', 're', 'ne', 'se', 'te', 'me') else 1
            code[c + v] = [highs.pop() for _ in range(k)]
    for u in ['en', 'on', 'an', 'in', 'ou', 'oi', 'ai', 'au', 'eu', 'ent', 'ment', 'tion', 'que', 'qui']:
        code[u] = [highs.pop()]
    words = """de la le les et que vous je ne pas pour dans par avec sur qui est sont il ils nous ont a au aux
    monsieur roy troupes ennemis cavalerie infanterie dragons canon chevaux jour soir ordre lettre garnison
    regiment bataillons hommes marche place ville chasteau mulets pain vivres poudre des du un une ce cette
    mais si on en y me se sa son ses mon ma mes vostre vos leur leurs tout tous toute point plus bien fort
    faire fait estre este avoir ay dire mander mandez escrire lettres honneur serviteur tres humble obeissant
    compagnies gardes officiers prisonniers matin quartiers pays temps costé costé nouvelle nouvelles homme
    gens affaire affaires quelque quelques comme aussi encore lorsque quand jusques depuis avant apres""".split()
    for w in words:
        if len(highs) > 8 and w not in code:
            code[w] = [highs.pop()]
    for i in range(6):
        code['<hnull%d>' % i] = [highs.pop()]
    return code

def encode(text, code, rnd):
    out = []; units = []
    for w in text.split():
        i = 0
        while i < len(w):
            rest = w[i:]
            if rest in code and len(rest) > 1 and rnd.random() < PW:
                u = rest
            elif i + 1 < len(w) and w[i] in CONS and w[i+1] in VOW and rnd.random() < PS:
                u = w[i:i+2]
            elif rest[:3] in ('ent', 'que', 'qui') and rnd.random() < PS:
                u = rest[:3]
            elif rest[:2] in ('en', 'on', 'ou', 'oi', 'ai', 'au', 'an', 'in') and rnd.random() < PS:
                u = rest[:2]
            else:
                u = w[i]
            if u not in code:
                u = w[i]
            out.append(rnd.choice(code[u])); units.append(u)
            i += len(u)
            if rnd.random() < 0.02:
                nk = rnd.choice([k for k in code if k.startswith('<')])
                out.append(rnd.choice(code[nk])); units.append(nk)
    return out, units

if __name__ == '__main__':
    plain = norm(open(sys.argv[1], encoding='utf-8').read())
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rnd = random.Random(seed)
    code = build_code(rnd)
    toks, units = encode(plain, code, rnd)
    # trim to 418 tokens
    toks, units = toks[:418], units[:418]
    with open('control.txt', 'w', encoding='utf-8') as f:
        f.write('# synthetic control, seed %d\n' % seed)
        for i in range(0, len(toks), 13):
            f.write(' '.join(map(str, toks[i:i+13])) + '\n')
    inv = {}
    for u, ns in code.items():
        for n in ns:
            inv[n] = '' if u.startswith('<') else u
    with open('control_key.txt', 'w', encoding='utf-8') as f:
        for n in sorted(inv):
            f.write('%d\t%s\n' % (n, inv[n]))
    with open('control_units.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(units))
    low = sum(1 for t in toks if t < 100)
    print('tokens', len(toks), 'distinct', len(set(toks)), 'low tokens', low, 'low distinct', len({t for t in toks if t < 100}))
