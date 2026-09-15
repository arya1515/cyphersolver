"""Tanaka -> Sun Yat-sen, Swatow 3 April 1916 (JACAR B03050738800, frame 680682).
Parse the ten-letter groups into consonant+vowel syllables and print statistics."""
import collections, re
CT = ("Twelve baxuxupeja qicijinati bemigasiqi jakebiqoye kufohemige tuxaboboba "
      "gedoeijiga poyevayoxa leyoleveke biromapesa vorobenife xikebiqoye qekufiyaqa "
      "tijaqixiqo xitohatula xopavajejo ropezpo ngobunibai tanaka")
groups = CT.split()[1:-1]
CONS = 'bcdfghjklmnpqrstvxyz'; VOW = 'aeiou'
def parse(groups):
    s = ''.join(groups)
    out = []; i = 0
    while i < len(s):
        if i+1 < len(s) and s[i] in CONS and s[i+1] in VOW:
            out.append(s[i:i+2]); i += 2
        else:
            out.append('?'+s[i]); i += 1
    return out
if __name__ == '__main__':
    s = ''.join(groups)
    print('letters', len(s), 'groups', len(groups), [len(g) for g in groups])
    syl = parse(groups)
    print('tokens', len(syl), 'anomalies', [t for t in syl if t.startswith('?')])
    print(' '.join(syl))
    c = collections.Counter(t for t in syl if not t.startswith('?'))
    print('distinct syllables', len(c), 'repeats:', [(k, v) for k, v in c.most_common() if v > 1])
    print('consonants', sorted(set(s) - set(VOW)), 'vowels', collections.Counter(ch for ch in s if ch in VOW))
    good = [t for t in syl if not t.startswith('?')]
    # positional stats assuming alternation page/cell
    for par in (0, 1):
        sub = good[par::2]
        print('parity', par, collections.Counter(t[0] for t in sub).most_common(), collections.Counter(t[1] for t in sub).most_common())
