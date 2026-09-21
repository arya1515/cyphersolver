"""Decrypt the DECODE R6-R10 transcriptions with Lasry's reconstructed key (DOC_R*_D320x).

Tokens: digits; a digit followed by ^. / ^' / ¥ is dotted (starts a nomenclator element, which runs to the next 1).
1 is a null/separator. Regular elements are 1 or 2 digits and the split is not deterministic, so each run between
nulls is segmented by beam search under the it-cinquecento language model.
Usage: python santacroce1552/decode.py santacroce1552/decode/DOC_R6_D1624_1624.txt
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lang import lm

KEY = {'28': 'a', '38': 'a', '8': 'a', '48': 'b', '58': 'c', '68': 'd', '24': 'e', '34': 'e', '4': 'e', '44': 'f',
       '54': 'g', '64': 'h', '2': 'i', '22': 'i', '32': 'i', '42': 'l', '52': 'm', '62': 'n', '26': 'o', '36': 'o',
       '6': 'o', '46': 'p', '03': 'r', '56': 'r', '05': 's', '66': 's', '07': 't', '76': 't', '86': 't', '02': 'u',
       '04': 'u', '06': 'u', '08': 'u', '96': 'z'}
M = lm.load('it-cinquecento')


def tokens(text):
    out = []
    for m in re.finditer(r"(\d)(\s*(\^[.']|¥))?", text):
        out.append((m.group(1), bool(m.group(2))))
    return out


def segment(digits):
    """Best letter reading of a digit run; unknown pieces shown as {d}."""
    beams = [(0.0, 0, '')]  # score, position, text
    done = []
    while beams:
        nxt = []
        for sc, i, t in beams:
            if i == len(digits):
                done.append((sc, t)); continue
            opts = []
            for L in (2, 1):
                g = digits[i:i + L]
                if len(g) == L and g in KEY:
                    opts.append((L, KEY[g]))
            if not opts:
                opts = [(1, '{%s}' % digits[i])]
            for L, ch in opts:
                t2 = t + ch
                s2 = sc + (M.per_char(t2[-6:]) * min(len(t2), 6) - (M.per_char(t[-5:]) * min(len(t), 5) if t else 0)
                           if not ch.startswith('{') else sc - 8)
                nxt.append((s2, i + L, t2))
        nxt.sort(key=lambda x: -x[0])
        seen, beams = set(), []
        for b in nxt:
            k = (b[1], b[2][-5:])
            if k not in seen:
                seen.add(k); beams.append(b)
            if len(beams) >= 60:
                break
    return max(done)[1] if done else ''


def decrypt(text):
    # drop cleartext blocks, keep only cipher
    cipher = re.sub(r'<[^>]*>', ' ', text)
    cipher = '\n'.join(l for l in cipher.splitlines() if not l.startswith('#'))
    toks = tokens(cipher)
    out, run, code = [], '', None
    def flush():
        nonlocal run
        if run:
            out.append(segment(run)); run = ''
    for d, dot in toks:
        if dot:
            flush(); code = d; continue
        if d == '1':
            flush()
            if code is not None:
                out.append('[%s]' % code); code = None
            out.append(' ')
            continue
        if code is not None:
            code += d
        else:
            run += d
    flush()
    if code:
        out.append('[%s]' % code)
    return re.sub(' +', ' ', ''.join(out)).strip()


if __name__ == '__main__':
    for f in sys.argv[1:]:
        print('==', os.path.basename(f))
        for part in re.split(r'#IMAGE NAME: (\S+)\n', open(f, encoding='utf-8', errors='replace').read())[1:]:
            print(part if len(part) < 20 else decrypt(part))
