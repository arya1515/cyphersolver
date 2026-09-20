"""Produce the reading of the two letters Lasry left undeciphered (R75, R84)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import decode as D, indomain

D.P_NOMEN_KNOWN, D.P_NOMEN_NEW, D.P_NULL = -1.5, -20.0, 0.0

def main():
    model, n = indomain.build(w=0.6)
    nomen = D.load_nomen()
    sys.stderr.write('in-domain chars %d, known nomenclator codes %d\n' % (n, len(nomen)))
    seen = {}
    for tag in ('r75', 'r84'):
        lines, toks_all = [], []
        for line in open(os.path.join(HERE, tag + '.digits'), encoding='utf-8'):
            s = ''.join(c for c in line if c.isdigit())
            if not s:
                continue
            _, text, toks = D.decode(s, model, nomen, beam=600, w_lm=0.4)
            lines.append(text); toks_all.append(toks)
        open(os.path.join(HERE, tag + '.read.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
        json.dump(toks_all, open(os.path.join(HERE, tag + '.tokens.json'), 'w'), indent=0)
        codes = [t[1:] for ts in toks_all for t in ts if t.startswith('#')]
        new = [c for c in codes if c not in nomen]
        sys.stderr.write('%s: %d digits, %d nomenclator hits (%d not in Lasry\'s 95)\n'
                         % (tag, sum(len(''.join(t.lstrip('#?') for t in ts)) for ts in toks_all),
                            len(codes), len(new)))
        seen[tag] = codes
        print('=' * 25, tag)
        print('\n'.join(lines))
    json.dump(seen, open(os.path.join(HERE, 'nomen_seen.json'), 'w'), indent=1)

main()
