"""Charles II -> Duke of Hamilton, 1650: ciphertext collation and structure.
Two witnesses: A = An Account of the Preservation of King Charles II (1766) p.86ff (as read by Tomokiyo);
                C = Camden Society, Hamilton Papers (1880), nos. 174-177 (Gardiner, from the MSS)."""
from collections import Counter
import re

RUNS = {  # (letter, position): (A, C)
    ('6Aug', 'first is'):      ("281 192 258 91 308 100 379 3 108 327 13",  "281 192 2o8 91 308 100 379 3 108 327 13"),
    ('6Aug', 'were not'):      ("6 70 199 65 330 153 237 56 190 329 290 38 3", "6 70 199 65 330 153 237 56 190 329 290 38 3"),
    ('6Aug', 'done'):          ("302 192 353 308 100 108 17 120",             "302 192 353 308 106 108 17 120"),
    ('14Aug', 'bearer'):       ("270 16 135 9 190 10",                        "270 16 135 9 190"),
    ('31Aug', 'concerning'):   ("331 288 198 196 6 190 22 58 135 256 58 256 380 55", "331 288 198 196 6 190 22 58 135 256 58 256 380 55"),
    ('31Aug', 'send to'):      ("122", "22"),
    ('27Sep', 'resolved that'):("85 237 70 9 50 40 384 4 10 308 290 304",     "85 237 70 9 50 40 384 4 10 308 290 304"),
    ('27Sep', 'by the'):       ("174 261 82 15 347 8 3",                      "174 26 82 15 30 8 3"),
    ('27Sep', 'from'):         ("122 and 223", "122 and 223"),
    ('27Sep', 'yourself'):     ("281 329 165 244 9 42 65 56 324",             "281 329 165 244 9 4 65 56 324"),
    ('27Sep', 'to get you'):   ("20 174 36 9 40 13 15 38 61 195 289 4 5 384 380 10", "20 174 36 9 40 13 15 38 61 195 289 4 5 384 380 10"),
    ('6Aug', 'commanded'):     ("163", "163"),
    ('31Aug', 'refer you to'): ("163", "163"),
    ('6Aug', 'dateline'):      ("132", "132"),
}

def toks(s): return [int(x) for x in re.findall(r'\d+', s.replace('o', '5'))]

allA = []
for k, (a, c) in RUNS.items():
    ta, tc = toks(a), toks(c)
    flag = '' if ta == tc else '   <-- differs'
    print(f"{k[0]:6} {k[1]:14} A: {a}{flag}")
    if flag: print(f"{'':21} C: {c}")
    allA += ta
print()
cnt = Counter(allA)
print('groups', len(allA), 'distinct', len(cnt), 'max', max(cnt))
print('repeats:', sorted(((n, c) for n, c in cnt.items() if c > 1), key=lambda x: -x[1]))
small = sorted(n for n in cnt if n < 100)
print('<100 :', small)
print('>=100:', sorted(n for n in cnt if n >= 100))
