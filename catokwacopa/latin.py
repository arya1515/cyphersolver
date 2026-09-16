"""Latin reading of Catokwacopa lines: same exact-interleaving search as search.py, Latin vocabulary from
The Latin Library texts in latin/, no English positional prior (flat), no name list.
Usage: python latin.py 17 29
"""
import collections, glob, math, os, re, sys
import search

def latin_vocab(min_count=2):
    cnt = collections.Counter()
    for f in glob.glob(os.path.join('latin', '*.txt')):
        t = open(f, encoding='utf-8', errors='ignore').read().lower().replace('j', 'i').replace('v', 'u')
        cnt.update(re.findall('[a-z]+', t))
    cnt = {w: c for w, c in cnt.items() if c >= min_count and (len(w) > 1 or w in ('a', 'e', 'o'))}
    tot = sum(cnt.values())
    print('latin vocab', len(cnt), 'tokens', tot)
    return {w: math.log(c / tot) for w, c in cnt.items()}

if __name__ == '__main__':
    flat = math.log(1 / 3)
    search.PRIOR = {k: flat for k in search.PRIOR}
    search.EXTRA = []
    LP = latin_vocab(); T = search.trie(LP)
    for ln in [int(x) for x in sys.argv[1:]]:
        A, B = search.PAIRS[ln - 1]
        A2, B2 = A.replace('j', 'i').replace('v', 'u'), B.replace('j', 'i').replace('v', 'u')
        res = search.kbest(A2, B2, LP, T)
        print('\nline %d  %s / %s  (Latin, u=v, i=j)' % (ln, A, B))
        for sc, ws in res[:15]:
            print('   %7.1f  %s' % (sc, ' '.join(ws)))
        sys.stdout.flush()
