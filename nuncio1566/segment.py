"""Divide decrypt_raw.txt into words for the DECODE decryption files.

Beam search over the unspaced decoder output, inserting a space before a letter where the spaced Italian model
(lang/, it-cinquecento) prefers it. Nomenclator words ([CHE]) and unread groups ([60.], ?) are kept as tokens.
Writes ../decode_updates/decryptions/R<id>.txt.   usage: python segment.py
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from lang import lm

M = lm.load('it-cinquecento', spaces=True)
A, K, IDX = M.A, M.order, M.index
LP = M.lp.reshape(-1, A)
MOD = A ** (K - 1)
SP = IDX[' ']
SPACE_COST = -0.3


def seg(run, beam=40):
    chars = [IDX[c] for c in lm.norm(run, 'early', True) if c in IDX and c != ' ']
    text = [c for c in lm.norm(run, 'early', True) if c in IDX and c != ' ']
    st = {0: (0.0, '')}
    for x, ch in zip(chars, text):
        nxt = {}
        for ctx, (sc, out) in sorted(st.items(), key=lambda kv: -kv[1][0])[:beam]:
            for sp in (False, True):
                c, s, o = ctx, sc, out
                if sp and o:
                    s += float(LP[c, SP]) + SPACE_COST; c = (c * A + SP) % MOD; o += ' '
                s += float(LP[c, x]); c = (c * A + x) % MOD; o += ch
                if c not in nxt or s > nxt[c][0]:
                    nxt[c] = (s, o)
        st = nxt
    return max(st.values())[1] if st else ''


def clean(stream):
    out = []
    for tok in re.split(r'(\[[^\]]+\]|\?+)', stream):
        if not tok:
            continue
        if tok.startswith('?'):
            out.append('[?]' if len(tok) == 1 else '[...]')
        elif tok.startswith('['):
            g = tok[1:-1]
            out.append('<' + g + '>' if re.fullmatch(r'[0-9]+\.', g) else g.lower())
        else:
            out.append(seg(tok))
    s = ' '.join(out)
    return re.sub(r'\s+', ' ', s).strip()


def wrap(s, n=100):
    lines, cur = [], ''
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    return lines + [cur] if cur else lines


def main():
    recs = {}
    blocks = open(os.path.join(HERE, 'decrypt_raw.txt'), encoding='utf-8').read().split('== ')[1:]
    for b in blocks:
        head, body = b.split('\n', 1)
        rec, img = head.split()[:2]
        recs.setdefault(rec, []).append((img.replace('.jpg', ''), body.strip()))
    outdir = os.path.join(HERE, '..', 'decode_updates', 'decryptions')
    for rec, pages in recs.items():
        parts = []
        for img, body in pages:
            parts.append('[f. ' + img + ']')
            parts.extend(wrap(clean(body)))
        open(os.path.join(outdir, rec + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(parts) + '\n')
        print(rec, len(pages), 'page(s)')


if __name__ == '__main__':
    main()
