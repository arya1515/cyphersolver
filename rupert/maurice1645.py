"""Maurice -> Rupert, Worcester 7 July 1645 (Warburton, Memoirs of Prince Rupert, iii. 133): ciphertext and structure."""
from collections import Counter
CT = {
 'observe that': "15 26 342 148 136 13 325 162 84 212 26 334 61 340 199 39 328 353 149 49 329 26 351 397 150 100 148 212 66 336 156 217 28 229 355 82 16 15 194 229 214 84 324 131 293 252 355 150 293 148 231 22 194 228 293 323 151 351",
 'Garrison,': "6 15 148 64 229 354 37 323 217 41 398 373 150 172 170 48 227 214 293 148 66 84 270 361",
 'Accordingly,': "151 244 229 149 213 324 239 274 185 12 15",
}
allg = [int(x) for s in CT.values() for x in s.split()]
c = Counter(allg)
print('groups', len(allg), 'distinct', len(c), 'max', max(allg))
print('repeats', sorted(((n, k) for n, k in c.items() if k > 1), key=lambda x: -x[1]))
lo = sorted(n for n in c if n < 100); hi = sorted(n for n in c if n >= 100)
print('<100 (%d):' % len(lo), lo)
print('>=100 (%d):' % len(hi), hi)
# known Rupert-related keys (Tomokiyo, charlesi.htm) for comparison of ranges
print("Charles I-Rupert 1644 key: letters + a1..p5 codes, words 106..421 (nulls 81-90) -> Maurice text has no letter-digit codes, so different.")
print("Nicholas-Rupert Jul 1645 key: words 98-373 and 427-616 -> Maurice text max 398, no 4xx-6xx groups, so different.")
