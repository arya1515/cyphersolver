"""Decipher every transcription with key.json and write read/<record>.txt.

Clear text is kept in {braces}; deciphered passages are written in [square brackets]; a sign with no value prints '?'.

    python decode.py            # all records
    python decode.py R3811      # one record, also printed
"""
import json, os, sys
from parse import files, tokens_of
from solve2 import value

HERE = os.path.dirname(os.path.abspath(__file__))


def loadkey(path=os.path.join(HERE, 'key.json')):
    k = json.load(open(path, encoding='utf-8'))
    h = {int(a[1:]): b for a, b in k.items() if a.startswith('H')}
    s = {a: b for a, b in k.items() if not a.startswith('H')}
    return h, s


def decode_record(rec, h, s):
    out = []
    for f in files([rec]):
        out.append('### ' + os.path.basename(f)[:-4])
        for line in open(f, encoding='utf-8'):
            t = line.strip()
            if not t or t == '#' or t.startswith('# '):
                continue
            if t.startswith('##'):
                out.append(t); continue
            parts, cur = [], []
            for it in tokens_of(t):
                if it[0] == 'clear':
                    if cur:
                        parts.append('[' + ''.join(cur) + ']'); cur = []
                    parts.append('{' + it[1] + '}')
                else:
                    tok = it[1]
                    if tok.startswith('~') or tok in ('/', '#ins'):
                        continue
                    v = value(tok, h, s) if '?' not in tok else '?'
                    cur.append(v if v != '?' else '?')
            if cur:
                parts.append('[' + ''.join(cur) + ']')
            out.append(' '.join(parts))
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    h, s = loadkey()
    os.makedirs(os.path.join(HERE, 'read'), exist_ok=True)
    recs = sys.argv[1:] or ['R3812', 'R3811', 'R3813', 'R3814', 'R3815', 'R4625', 'R4645', 'R4734', 'R4736']
    for r in recs:
        txt = decode_record(r, h, s)
        open(os.path.join(HERE, 'read', r + '.txt'), 'w', encoding='utf-8').write(txt)
        if len(sys.argv) > 1:
            print(txt)
