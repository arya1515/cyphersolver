"""Decode a transcription of a Nevers no. 46 cipher passage.

Transcription conventions (ct files):
  plain two-digit groups separated by spaces          -> alphabet / plain-series word
  a group followed by _  (e.g. 80_)                    -> barred figure (word series B)
  a group followed by :  (e.g. 88:)                    -> two dots above (name series D)
  o+                                                   -> the sign for Monsieur
  |                                                    -> word break written in the original (if any)
  [clear text]                                         -> text in clear inside the cipher
  ?                                                    -> illegible glyph
Usage: python decode46.py ct.txt
"""
import sys, re, pathlib
HERE = pathlib.Path(__file__).parent
KEY = {}
for line in (HERE / 'key46.txt').read_text(encoding='utf-8').splitlines():
    line = line.split('#')[0].strip()
    if not line:
        continue
    ser, fig, val = line.split('\t')[:3]
    KEY.setdefault((ser, fig), val)

def decode_token(tok):
    if tok.startswith('[') and tok.endswith(']'):
        return tok[1:-1]
    if tok == 'o+':
        return 'Monsieur'
    if tok == '|':
        return ' '
    m = re.fullmatch(r'(\d+)([_:]?)', tok)
    if not m:
        return '{' + tok + '}'
    fig, mark = m.group(1), m.group(2)
    f = str(int(fig))
    if mark == '_':
        return '<' + KEY.get(('B', f), '?B' + f) + '>'
    if mark == ':':
        return '<' + KEY.get(('D', f), '?D' + f) + '>'
    if ('A', f) in KEY:
        v = KEY[('A', f)]
        if ('P', f) in KEY:
            return v  # alphabet reading first; P alternative shown in the report
        return v
    if ('N', f) in KEY and ('P', f) not in KEY:
        return '·'
    if ('P', f) in KEY:
        return '<' + KEY[('P', f)] + '>'
    if ('N', f) in KEY:
        return '·'
    return '{' + tok + '}'

def decode_line(line):
    out = []
    for tok in line.split():
        out.append(decode_token(tok))
    return ''.join(x if len(x) == 1 or x.startswith('<') or x.startswith('{') else ' ' + x + ' ' for x in out)

if __name__ == '__main__':
    src = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
    n_tok = n_ok = 0
    for line in src.splitlines():
        if not line.strip() or line.startswith('#'):
            print(line)
            continue
        dec = decode_line(line)
        toks = [t for t in line.split() if re.fullmatch(r'\d+[_:]?', t)]
        n_tok += len(toks)
        n_ok += sum(1 for t in toks if '?' not in decode_token(t) and '{' not in decode_token(t))
        print(line)
        print('   ', dec)
    print(f'# tokens {n_tok}, resolved {n_ok}')
