"""What unit does a glyph stand for? Compare the cipher poem's token statistics with 279-unit samples of
real verse cut into candidate units.

Cipher (verse_transcription.py): 279 tokens, 111 types, 52 hapax, top type 9.0%, 5 adjacent doubles,
13.7 units per line.

Units tried, in English (Moore) and French (Hugo, Chenier, Musset, Gautier):
  letter, bigram (non-overlapping letter pairs per line), syllable (orthographic: onset + vowel group, final
  consonants kept with the last syllable of the word), word.
"""
import collections, glob, os, random, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verse_transcription import lines

V = 'aeiouyàâäéèêëîïôöûùüÿœ'
HERE = os.path.dirname(os.path.abspath(__file__))


def verse_lines(files):
    out = []
    for f in files:
        run = []
        for l in open(f, encoding='utf-8', errors='ignore').read().split('\n'):
            l = l.strip()
            if 15 <= len(l) <= 80 and re.search('[a-zà-ÿ]', l) and not re.search(r'[0-9_\[\]]', l):
                run.append(l)
            else:
                if len(run) >= 8: out.extend(run)
                run = []
    return out


def units(line, kind):
    s = line.lower()
    words = re.findall('[a-zà-ÿœ]+', s)
    if kind == 'letter':
        return list(''.join(words))
    if kind == 'bigram':
        t = ''.join(words)
        return [t[i:i + 2] for i in range(0, len(t), 2)]
    if kind == 'word':
        return words
    if kind == 'syllable':
        out = []
        for w in words:
            parts = re.findall('[^%s]*[%s]+' % (V, V), w)
            tail = re.sub('^(?:[^%s]*[%s]+)*' % (V, V), '', w)
            if not parts:
                out.append(w); continue
            if tail: parts[-1] += tail
            out.extend(parts)
        return out


def stats(seq):
    c = collections.Counter(seq)
    doubles = sum(1 for a, b in zip(seq, seq[1:]) if a == b)
    return len(c), sum(1 for v in c.values() if v == 1), c.most_common(1)[0][1] / len(seq), doubles


def sample(L, kind, n=279, trials=300, rnd=random.Random(0)):
    res, per_line = [], []
    for _ in range(trials):
        i = rnd.randrange(len(L) - 60)
        seq = []
        j = i
        while len(seq) < n:
            u = units(L[j], kind); per_line.append(len(u)); seq.extend(u); j += 1
        res.append(stats(seq[:n]))
    avg = [sum(r[k] for r in res) / len(res) for k in range(4)]
    return avg, sum(per_line) / len(per_line)


def main():
    toks = [t for l in lines() for t in l]
    t, h, top, d = stats(toks)
    print('cipher:       types %5.1f  hapax %5.1f  top %.3f  doubles %4.1f  per line %.1f' % (t, h, top, d, len(toks) / 20))
    corp = {'English (Moore)': [os.path.join(HERE, 'corpus', f) for f in ('pg8187.txt', 'pg76794.txt')],
            'French verse': glob.glob(os.path.join(HERE, 'corpus', 'fr*.txt'))}
    for name, files in corp.items():
        L = verse_lines(files)
        print('\n%s: %d verse lines' % (name, len(L)))
        for kind in ('letter', 'bigram', 'syllable', 'word'):
            (t, h, top, d), pl = sample(L, kind)
            print('  %-9s types %5.1f  hapax %5.1f  top %.3f  doubles %4.1f  per line %.1f' % (kind, t, h, top, d, pl))


if __name__ == '__main__':
    main()
