"""Apply the reconstructed THE=972 code table to Armstrong's coded passages.

Sources merged (later overrides earlier):
  code972_partial.json  cryptiana's table from the 4 May 1806 known plaintext (base)
  pairs.txt             pencil interlinear decodes harvested from DUSMF M34 roll 13 (H/M confidence)
  INFER                 readings inferred here from context + alphabetical position (marked ?)
Usage:  python decode972.py [ps|feb|all|table]
"""
import json, re, sys
from collections import defaultdict

tab = defaultdict(list)
for k, v in json.load(open('code972_partial.json', encoding='utf-8')).items():
    for r in v:
        tab[int(k)].append((r.strip(), 'C'))
for line in open('pairs.txt', encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    n, r, src, conf = line.rstrip('\n').split('\t')
    tab[int(n)].append((r, conf))

# context + alphabetical-position inferences (this session).  Evidence in NOTES.md.
INFER = {
    # PS 30 Aug 1808
    1394: 'ru', 1273: 'el', 250: 'ought', 148: 'consul', 130: 'America', 720: 'bir', 970: 'th',
    992: 'qua', 1048: 'fi(ed)', 584: 'than', 1202: 'above', 1052: 'fit', 934: 'o', 510: 'mea',
    1320: 'like', 384: 'ward', 1483: 'ish',
    # 555 = 're' (0195R5 sco-re) — in the PS Armstrong evidently dropped a digit: 1555 = man
    # 22 Feb 1808
    297: 'resolve', 946: 'Gu', 26: 'Denmark', 758: 'dep', 825: 'nce', 1224: 'arm', 1257: 'duct',
    752: 'dan', 1572: 'morning', 396: 'while', 943: 'upon', 193: 'govern', 1082: 'rt',
    305: 'Russia', 947: 'only', 765: 'does', 1132: 'sist', 655: 'pli', 1126: 'sh', 917: 'half',
}
for n, r in INFER.items():
    tab[n].append((r, '?'))


def best(n):
    """Pick highest-confidence reading: H > C > M > ?"""
    if n not in tab:
        return None
    order = {'H': 0, 'C': 1, 'M': 2, '?': 3}
    def key(x):
        r, c = x
        # cryptiana's 'x...?' guesses and '(null/punct)' misreads rank below our inferences
        if ('...' in r or 'null' in r or '?' in r) and c != '?':
            return 4
        return order[c]
    return sorted(tab[n], key=key)[0]


def render(text):
    out = []
    for tok in re.findall(r'\d{1,4}|[^\d\s]+', text):
        if tok.isdigit():
            b = best(int(tok))
            if b is None:
                out.append(f'{{{tok}}}')
            else:
                r, c = b
                mark = '' if c in 'HC' else ('?' if c == 'M' else '*')
                out.append(f'{r}{mark}')
        else:
            out.append(tok)
    return ' '.join(out)


# PS as read from the LOC manuscript (mjm 10/0521): Founders prints 1218 for 1216.  Final group is 555 in the MS;
# 555 = 're' elsewhere, so it is taken as Armstrong's slip for 1555 'man' (see NOTES.md).
PS = """1394 1116 1273 250 1165 1405 | 972 148 1459 1482 1201 821 130 821 | 1429 720 970 | and | 1482 |
much better | 992 1319 1048 584 687 249 736 1013 | 750 967 | In a word | 1459 1482 1202 | 1561 |
in general. Next to | 927 1090 1052 | 832 1482 934 510 860 | but | 1459 1482 | 1320 384 1280 1216 1481 1483 [555=>1555]"""

FEB = """972 1394 1090 1354 946 985 608 899 1482 1228 1492 297 1001 Russia is to seize Finland, while
France & Denmark take possession of Sweden 26 736 1587 916 369 630 1478 860 1090 758 1282 1284 825 .
And it is certainly amongst the most cruel circumstances of the British attack on her Capital that
1484 1436 1078 368 1463 337 1354 1463 1358 1217 631 463 1354 470 1257 1217 593 383 821 1463 1247 1181
967 860 1479 972 1224 1116 1354 1069 962 396 972 . 752 1483 61 385 . 590 1572 1373 380 1478 . 537 1467 1247
631 578 . 1116 1165 509 943 590 . 988 1304 . 1217 985 351 1431 972 . 769 803 . 1354 1467 193 514 1217 .
972 511 1116 579 821 1429 . 1484 1165 . 1201 1157 1082 972 1090 578 . 882 . 1257 1480 . 1479 26 1354 1201
191 690 . 962 . 1354 968 1494 . 1244 1387 of Hamburg waited in the antichamber ...
Yet wonderful to tell 305 1587 947 765 . 1587 . 87 . 1478 . 804 1158 . 860 . 1225 . 1132 . 1116 927 . 1090
803 . 1247 655 . 1126 1478 . 550 917 1354 . 972 236 . Can Finland compensate ...
they are in a State of the 523 . 1247 1182 967 . 933 1088 . 1078 . 431 ."""

SEP07 = """circumstances of the present moment 1280 . [ ]18 415 1165 1020 632 972 187 1116 1217 410 391 796 1319
[ ]69 1116 392 1503 415 653 772 . It so happens that there is no one even to 1226 1201 287 945 166 ... 988 1304"""

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('ps', 'all'):
        print('== PS 30 Aug 1808 ==\n' + render(PS) + '\n')
    if what in ('feb', 'all'):
        print('== 22 Feb 1808 ==\n' + render(FEB) + '\n')
    if what in ('sep', 'all'):
        print('== 3414 ==\n' + render(SEP07) + '\n')
    if what == 'table':
        for n in sorted(tab):
            print(n, '; '.join(f'{r}[{c}]' for r, c in tab[n]))
