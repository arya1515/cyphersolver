"""Token grammar for a Venetian letter-plus-figure cipher (Ottobon to Mocenigo, BNE Ms. 994 ff. 34-38).

Transcription convention (ct.txt, one physical line per line, tokens space-separated):
    a12   base letter a with figure 12 (superscript or inline; record the position in ct2.txt if it matters)
    a_1   base letter with a ONE-digit figure written where two would fit (Bonavoglia's f_1 convention)
    L54   capital base letters kept as capitals (the Zifra Granda distinguishes L)
    o18 t8   polywog and turned-T signs, if present, transcribed as o and t (Bonavoglia's convention)
    12    bare figure without base letter
    =et=  clear-text word inside the cipher run, between = signs
    |     end of a written line inside a folio, if the transcription joins lines
    #     comment to end of line (folio and line labels: "# f.35r l.1")
The parser returns a list of (base, figure, raw) with base '' for bare figures and figure None for bare letters.
"""
import re, sys, collections

TOK = re.compile(r'^([A-Za-z]?)_?(\d*)$')

def parse(text):
    toks = []
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        for w in line.split():
            if w == '|':
                continue
            if w.startswith('=') and w.endswith('='):
                toks.append(('CLEAR', None, w[1:-1]))
                continue
            m = TOK.match(w)
            if not m:
                raise ValueError('bad token %r' % w)
            base, fig = m.group(1), m.group(2)
            toks.append((base, int(fig) if fig else None, w))
    return toks

def cipher_only(toks):
    return [t for t in toks if t[0] != 'CLEAR']

if __name__ == '__main__':
    fn = sys.argv[1] if len(sys.argv) > 1 else 'ct.txt'
    toks = cipher_only(parse(open(fn, encoding='utf-8').read()))
    print('tokens', len(toks), 'distinct', len(set(t[2] for t in toks)))
    bases = collections.Counter(t[0] for t in toks)
    print('base letters', sorted(bases.items(), key=lambda x: -x[1]))
    figs = collections.Counter(t[1] for t in toks if t[1] is not None)
    print('figure range', min(figs), max(figs), 'distinct figures', len(figs))
