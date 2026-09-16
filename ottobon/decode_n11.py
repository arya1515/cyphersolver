"""Read a ct.txt through Franceschi's Ziffra N.11 alphabet (ASVe CX Cifre b.4 r.16 c.74; Bonavoglia 2022 Fig. 7-8;
table in refs/n11_alphabet.json). Tokens on base letters a c d f g h with figures 1-20 are letters; everything else
(other base letters, figures > 20) belongs to the nomenclator and is printed in brackets.
Usage: python decode_n11.py ct.txt"""
import sys, json, os, collections
from parse import parse, cipher_only
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.join(HERE, 'refs', 'n11_alphabet.json')))

def decode(toks):
    out = []
    for base, fig, raw in toks:
        if base == 'CLEAR':
            out.append('=%s=' % raw); continue
        out.append(KEY.get(raw, '[%s]' % raw))
    return out

if __name__ == '__main__':
    text = open(sys.argv[1], encoding='utf-8').read()
    toks = parse(text)
    dec = decode(toks)
    print(''.join(dec))
    c = collections.Counter(t[2] for t in cipher_only(toks))
    hit = sum(v for k, v in c.items() if k in KEY); tot = sum(c.values())
    print('\nalphabet hits %d / %d tokens (%.0f %%)' % (hit, tot, 100.0 * hit / max(tot, 1)))
    letters = collections.Counter(KEY[k] for k in c.elements() if k in KEY)
    print('letter profile', letters.most_common())
