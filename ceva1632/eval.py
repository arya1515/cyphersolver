"""Score the decoder against Lasry's own segmentation of the four read letters.

Leave-one-document-out: the nomenclator inventory offered to the decoder for a
document is built from the other three only, so a code first seen in the held-out
letter counts as new -- which is the situation for the two unread letters.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import decode as D
from lang import lm

def gold_docs():
    g = json.load(open(os.path.join(HERE, 'gold.json'), encoding='utf-8'))
    docs = {}
    for cat, row in g:
        docs.setdefault(cat, []).extend([t for t, _ in row if t.isdigit()])
    return docs

def spans(seq):
    out, i = set(), 0
    for t in seq:
        out.add((i, t)); i += len(t)
    return out

def score(model, loo=True, **kw):
    docs = gold_docs()
    nom_of = {c: {t for t in toks if len(t) == 3} for c, toks in docs.items()}
    ok = tot = 0
    per = {}
    for cat, toks in docs.items():
        if loo:
            nomen = set().union(*[v for c, v in nom_of.items() if c != cat])
        else:
            nomen = set().union(*nom_of.values())
        _, _, got = D.decode(''.join(toks), model, nomen, **kw)
        got = [t.lstrip('#?') for t in got]
        a, b = spans(toks), spans(got)
        per[cat] = (len(a & b), len(a))
        ok += len(a & b); tot += len(a)
    return ok / tot, per

if __name__ == '__main__':
    model = lm.load('it-cinquecento')
    best = None
    for w in (0.4, 0.6, 0.8, 1.0, 1.3):
        for pk in (-1.5, -3.0, -5.0):
            for pn in (-5.0, -7.0, -9.0, -12.0):
                for pnull in (0.0, -0.2, -0.5):
                    D.P_NOMEN_KNOWN, D.P_NOMEN_NEW, D.P_NULL = pk, pn, pnull
                    r, _ = score(model, beam=120, w_lm=w)
                    if best is None or r > best[0]:
                        best = (r, w, pk, pn, pnull)
                        print('best %.4f w=%s known=%s new=%s null=%s' % best, flush=True)
    print('BEST', best)
    D.P_NOMEN_KNOWN, D.P_NOMEN_NEW, D.P_NULL = best[2], best[3], best[4]
    r, per = score(model, beam=400, w_lm=best[1])
    print('at beam 400: %.4f' % r)
    for c, (o, t) in per.items():
        print('  %-28s %4d/%4d  %.3f' % (c, o, t, o / t))
