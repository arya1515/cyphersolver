"""Test Meister (1906) p.176-177 key no. 2 -- 'Cifra ultima con Mons. Poggio mandata per il Montepulciano'
[1538-1542] -- against the Vatican Challenge Part 5 ciphertext.

Key (as printed):
  a e i o u | bc dfg lp nm rt sz et
  3 5 7 9 0 | 8?  01  2  4  6  1
  ca ce ci co = 21 22 23 24    ra re ri ro = 88 89 08 00
  da de di do = 12 14 16 18    sa se si so = 84 85 86 87
  la le li lo = 62 64 61 66    ta te ti to = .80 .81 .82 .83   (dot over preceding digit)
  ma me mi mo = 04 06 03 05    qua que qui = .84 .85 .86
  na ne ni no = 80 81 82 83    che chi non = .87 .88 .89
  N.S. = .08   S.Mta = .00   Francia = 000
"""
import sys, re
from parse5 import load, digit_stream

SINGLE = {'3': 'a', '5': 'e', '7': 'i', '9': 'o', '0': 'u', '8': '[bc]', '2': '[lp]', '4': '[nm]', '6': '[rt]', '1': '[sz/et]'}
DOUBLE = {'01': '[dfg]',
          '21': 'ca', '22': 'ce', '23': 'ci', '24': 'co', '88': 'ra', '89': 're', '08': 'ri', '00': 'ro',
          '12': 'da', '14': 'de', '16': 'di', '18': 'do', '84': 'sa', '85': 'se', '86': 'si', '87': 'so',
          '62': 'la', '64': 'le', '61': 'li', '66': 'lo', '04': 'ma', '06': 'me', '03': 'mi', '05': 'mo',
          '80': 'na', '81': 'ne', '82': 'ni', '83': 'no'}
DOTTED = {'80': 'ta', '81': 'te', '82': 'ti', '83': 'to', '84': 'qua', '85': 'que', '86': 'qui',
          '87': 'che', '88': 'chi', '89': 'non', '08': 'N.S.', '00': 'S.Mta'}

def decode(tokens, prefer_double=True):
    """tokens: list like ['7','3^.','8','0',...]. Returns list of (ciphergroup, plaintext)."""
    out, i, n = [], 0, len(tokens)
    while i < n:
        d = tokens[i][0]; mark = tokens[i][1:]
        dotted = '^' in mark
        # dot on preceding digit => next two digits form a dotted-series code
        if dotted and i + 2 < n:
            pair = tokens[i+1][0] + tokens[i+2][0]
            if pair in DOTTED:
                out.append((d + '·', SINGLE.get(d, '?')))
                out.append((pair, DOTTED[pair])); i += 3; continue
        if i + 2 < n and tokens[i][0] + tokens[i+1][0] + tokens[i+2][0] == '000':
            out.append(('000', 'Francia')); i += 3; continue
        pair = tokens[i][0] + tokens[i+1][0] if i + 1 < n else None
        if prefer_double and pair in DOUBLE:
            out.append((pair, DOUBLE[pair])); i += 2; continue
        if d in SINGLE:
            out.append((d + ('·' if dotted else ''), SINGLE[d])); i += 1; continue
        if pair in DOUBLE:
            out.append((pair, DOUBLE[pair])); i += 2; continue
        out.append((d, '?')); i += 1
    return out

if __name__ == '__main__':
    pages = load()
    runs = digit_stream(pages)
    which = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    toks = runs[which][:limit]
    for pref in (True, False):
        dec = decode(toks, prefer_double=pref)
        print(f'\n=== run {which}, prefer_double={pref}')
        print(' '.join(p for _, p in dec))
        print(' '.join(f'{c}={p}' for c, p in dec[:80]))
