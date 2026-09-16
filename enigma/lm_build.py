"""Build the trigram log-probability table for Wehrmacht Enigma plaintext.

Base: Sullivan & Weierud's trigram counts from raw 1941 Enigma decrypts (bomm/data/frequencies/
enigma1941-trigram.txt, 17,694 trigrams) plus the Huppenkothen/Michel-Levy 1945 plaintexts, smoothed with
Gutenberg German (adfgvx/corpus/de_*.txt) converted to Enigma conventions: ae oe ue sz, ch/ck -> q,
punctuation -> x, digits spelled out, no spaces."""
import glob, os, re, sys, collections, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A = 'abcdefghijklmnopqrstuvwxyz'
DIG = {'0': 'null', '1': 'eins', '2': 'zwo', '3': 'drei', '4': 'vier', '5': 'fuenf', '6': 'seqs', '7': 'sieben',
       '8': 'aqt', '9': 'neun'}


def convert(t):
    t = t.lower()
    for a, b in [('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'sz'), ('é', 'e'), ('è', 'e')]:
        t = t.replace(a, b)
    t = t.replace('ch', 'q').replace('ck', 'q')
    t = re.sub(r'\d', lambda m: DIG[m.group()] + 'x', t)
    t = re.sub(r'[.,;:!?"()]+', 'x', t)
    return re.sub('[^a-z]', '', t)


def idx(s):
    return (A.index(s[0]) * 26 + A.index(s[1])) * 26 + A.index(s[2])


def main(scratch):
    c41 = np.zeros(17576)
    for l in open(os.path.join(scratch, 'enigma', 'bomm', 'data', 'frequencies', 'enigma1941-trigram.txt')):
        p = l.split()
        if len(p) == 2 and len(p[0]) == 3: c41[idx(p[0])] += float(p[1])
    # 1945 KL plaintexts (Sullivan & Weierud), Enigma conventions already applied
    kl = ('XGEHEIMXSSXGRUFXGLUECKSXPERSOENLIQXBITTEXSSXGRUFXMUELLERXMUELLERXFERNMUENDLIQXFERNSCHRIFTLIQODERDURQBOTENSQNELLSTENSFOLGENDES'
          'MITZUTEILENXEINSXAUFTRAGBEFEHLSGEMAESSERLEDIGTBESTAETIGUNGNIQTERFORDERLIQXZWEIXGOGALLAXGOGALLAXSEITXNEUNXVIERXVIERXUHRX'
          'AUFDEMWEITERMARSQNIMMTXDREIXBUCHENWALDERXMITXDREIXFUENFFUENFXBUCHENWALDERXSIPPENXUNDXSONDERHAEFTLINGEXBEFINDENSIQMIT'
          'WEITERENXEINSZWOXZELLENHAEFTLINGENINXSCHOENBERGXKRSXGRAFENAUXMITBEGLEITKOMMANDOSTAPOXWEIMARXUNTERXSSXUSTUFXBADERXUNTERKUNFTX'
          'UNZULAENGLIQXHILFSLAZARETTXFRUEHERESCHULEWEITEREVERFUEGUNGANSTAPOLEITERXREGENSBURGXERBETENXVIERXBINMORGENVORMITTAGXPAXZWOXPAXZWOX'
          'FALLSDORTKEINEBEFEHLEUNVERZUEGLIQEWEITERREISEXBERLINXBEABSIQTIGTXFUENFXFUNKODERANDEREBEFEHLEFUERMIQBISHERHIER'
          'NIQTEINGEGANGENXGEZHUPPENKOTHENXHUPPENKOTHENXSSXSTAFX').lower()
    for i in range(len(kl) - 2): c41[idx(kl[i:i + 3])] += 1
    print('military trigrams:', c41.sum())
    cg = np.zeros(17576)
    for f in sorted(glob.glob(os.path.join(HERE, '..', 'adfgvx', 'corpus', 'de_*.txt'))):
        t = open(f, encoding='utf-8', errors='ignore').read()
        s = t.find('*** START'); e = t.find('*** END')
        s = convert(t[s if s > 0 else 0: e if e > 0 else len(t)])
        ii = np.array([A.index(c) for c in s])
        k = (ii[:-2] * 26 + ii[1:-1]) * 26 + ii[2:]
        cg += np.bincount(k, minlength=17576)
    print('gutenberg trigrams:', cg.sum())
    # blend: military counts weighted as if 200k, Gutenberg as 100k
    mix = c41 / c41.sum() * 200000 + cg / cg.sum() * 100000
    mix[mix == 0] = mix[mix > 0].min() / 2
    logp = np.log(mix / mix.sum()).astype(np.float32)
    np.save(os.path.join(HERE, 'tri_logp.npy'), logp)
    # also a monogram table for reference
    mono = np.zeros(26)
    for i in range(17576): mono[i // 676] += mix[i]
    print('top letters:', ''.join(A[i] for i in np.argsort(-mono)[:12]))
    print('saved tri_logp.npy; mean logp of KL text per trigram:',
          np.mean([logp[idx(kl[i:i + 3])] for i in range(len(kl) - 2)]))



def build_lower(scratch):
    """Bigram and monogram log-prob tables from the same blend."""
    c41 = np.zeros(676)
    for l in open(os.path.join(scratch, 'enigma', 'bomm', 'data', 'frequencies', 'enigma1941-bigram.txt')):
        p = l.split()
        if len(p) == 2 and len(p[0]) == 2: c41[A.index(p[0][0]) * 26 + A.index(p[0][1])] += float(p[1])
    cg = np.zeros(676)
    for f in sorted(glob.glob(os.path.join(HERE, '..', 'adfgvx', 'corpus', 'de_*.txt'))):
        t = open(f, encoding='utf-8', errors='ignore').read()
        s = convert(t)
        ii = np.array([A.index(c) for c in s])
        cg += np.bincount(ii[:-1] * 26 + ii[1:], minlength=676)
    mix = c41 / c41.sum() * 200000 + cg / cg.sum() * 100000
    mix[mix == 0] = mix[mix > 0].min() / 2
    np.save(os.path.join(HERE, 'bi_logp.npy'), np.log(mix / mix.sum()).astype(np.float32))
    mono = mix.reshape(26, 26).sum(1)
    np.save(os.path.join(HERE, 'mono_logp.npy'), np.log(mono / mono.sum()).astype(np.float32))
    print('bigram/monogram tables saved')


if __name__ == '__main__':
    main(sys.argv[1]); build_lower(sys.argv[1])
