# Polyphonic decoder for the League cipher of 1592-93 (Tomokiyo, mayenne.htm): each symbol stands for two
# letters (a/n, b/o, c/p, d/q, e/r, f/s, g/t, h/u, i/x, l/y, m/z) plus the code groups que, qui, pour.
# Input: class string using the first letter of each pair (a b c d e f g h i l m); tokens {que} {qui} {pour};
# '|' = word break known from the image; '?' = illegible (any letter). Beam search over the sp53 French 6-gram LM.
import sys, os, re, math, pickle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sp53'))
from homo import LM
PAIRS = {'a':'an','b':'bo','c':'cp','d':'dq','e':'er','f':'fs','g':'gt','h':'hu','i':'ix','l':'ly','m':'mz'}
INV = {ch: k for k, v in PAIRS.items() for ch in v}
def encode(text):
    out = []
    t = re.sub(r'[^a-z ]', '', text.lower().replace('j','i').replace('v','u').replace('w','uu').replace('k','c'))
    for ch in t:
        if ch == ' ': continue
        out.append(INV[ch])
    return ''.join(out)
def tokens(s):
    return re.findall(r'\{[a-z]+\}|[a-m?|]', s)
def decode(s, lm, beam=2000, nbest=5):
    toks = tokens(s)
    beams = [('', 0.0)]
    for tk in toks:
        if tk == '|': continue
        if tk.startswith('{'): opts = [tk[1:-1]]
        elif tk == '?': opts = list('abcdefghilmnopqrstuxyz')
        else: opts = list(PAIRS[tk])
        new = []
        for txt, sc in beams:
            for o in opts:
                s2 = sc; t2 = txt
                for ch in o:
                    s2 += lm.logp(t2[-5:], ch); t2 += ch
                new.append((t2, s2))
        new.sort(key=lambda x: -x[1])
        beams = new[:beam]
    return beams[:nbest]
if __name__ == '__main__':
    lm = LM(os.path.join(os.path.dirname(__file__), '..', 'sp53', 'fr6.pkl'))
    if sys.argv[1] == 'test':
        text = open(sys.argv[2], encoding='utf-8').read()
        text = re.sub(r'[^a-zA-Z ]', ' ', text)
        words = text.split()[int(sys.argv[3]):int(sys.argv[3]) + int(sys.argv[4])]
        plain = ' '.join(words).lower()
        enc = encode(plain)
        truth = re.sub(r'[^a-z]', '', plain.replace('j','i').replace('v','u').replace('w','uu').replace('k','c'))
        res = decode(enc, lm, beam=int(sys.argv[5]) if len(sys.argv) > 5 else 2000)
        best = res[0][0]
        acc = sum(a == b for a, b in zip(best, truth)) / len(truth)
        print('truth', truth); print('best ', best); print('acc', round(acc, 3), 'len', len(truth))
    else:
        s = open(sys.argv[1], encoding='utf-8').read() if os.path.exists(sys.argv[1]) else sys.argv[1]
        s = re.sub(r'\s+', '', s)
        for t, sc in decode(s, lm, beam=int(sys.argv[2]) if len(sys.argv) > 2 else 2000):
            print(round(sc, 1), t)
