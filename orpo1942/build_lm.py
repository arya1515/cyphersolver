"""25-letter German quadgram table for the Doppelkasten solver (J folded to II, umlauts to AE/OE/UE, ß to SS).
Writes q4.bin: 25^4 float32 log10 probabilities, index a*25^3+b*25^2+c*25+d over ABCDEFGHIKLMNOPQRSTUVWXYZ."""
import collections, glob, math, os, re, struct, sys
A = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
HERE = os.path.dirname(os.path.abspath(__file__))

def clean(t, chq=False):
    t = t.lower()
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss'), ('é', 'e'), ('j', 'ii')):
        t = t.replace(a, b)
    t = re.sub('[^a-z]', '', t).upper()
    return t.replace('CH', 'Q') if chq else t

def texts():
    for f in glob.glob(os.path.join(HERE, '..', 'abwehr', 'corpus', 'de*.txt')) + glob.glob(os.path.join(HERE, '..', 'adfgvx', 'corpus', 'de_*.txt')):
        t = open(f, encoding='utf-8', errors='ignore').read()
        s = t.find('*** START'); e = t.find('*** END')
        yield t[s + 500 if s >= 0 else 0: e if e > 0 else len(t)]

if __name__ == '__main__':
    chq = 'chq' in sys.argv
    cnt = collections.Counter()
    for t in texts():
        x = clean(t, chq)
        cnt.update(x[i:i + 4] for i in range(len(x) - 3))
    tot = sum(cnt.values())
    floor = math.log10(0.5 / tot)
    out = [floor] * 25 ** 4
    ix = {c: i for i, c in enumerate(A)}
    for k, v in cnt.items():
        out[((ix[k[0]] * 25 + ix[k[1]]) * 25 + ix[k[2]]) * 25 + ix[k[3]]] = math.log10(v / tot)
    fn = 'q4_chq.bin' if chq else 'q4.bin'
    open(os.path.join(HERE, fn), 'wb').write(struct.pack('%df' % len(out), *out))
    print(fn, tot, len(cnt), floor)

def build_low(chq=False):
    """unigram (25) and bigram (625) log10 tables -> q1.bin, q2.bin (float32)"""
    c1 = collections.Counter(); c2 = collections.Counter()
    for t in texts():
        x = clean(t, chq); c1.update(x); c2.update(x[i:i + 2] for i in range(len(x) - 1))
    ix = {c: i for i, c in enumerate(A)}
    t1 = sum(c1.values()); t2 = sum(c2.values())
    u = [math.log10(max(c1[a], 0.5) / t1) for a in A]
    b = [math.log10(max(c2[a + b], 0.5) / t2) for a in A for b in A]
    suf = '_chq' if chq else ''
    open(os.path.join(HERE, 'q1%s.bin' % suf), 'wb').write(struct.pack('25f', *u))
    open(os.path.join(HERE, 'q2%s.bin' % suf), 'wb').write(struct.pack('625f', *b))
