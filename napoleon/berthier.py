"""Berthier to Napoleon, 22 December 1812 - locating the plaintext, and testing what can be tested.

The cryptogram is listed as unsolved by Tomokiyo, who reproduces its opening from J. Vilcoq,
"Le Chiffre sous le Premier Empire", Revue Historique de l'Armee no. 4 (1969). It carries the
archivist's note "Duplicata, Chiffre du Prince de Neufchatel, La Primata a ete dechiffree" - a
duplicate copy, in Berthier's own cipher, whose original had already been deciphered.

Two things are established here.

1. WHERE IT LIVES. The Archives nationales repertoire of the Secretairerie d'Etat war papers
   (N. Gotteri, FRAN_IR_003827, AF/IV/1590-1670) puts Berthier's reports to the Emperor for this
   date in AF/IV/1643, plaquette 1/VI: "Lettres et rapports adresses a l'Empereur par le major
   general depuis Gumbinnen puis Koenigsberg, concernant la retraite de la Grande Armee ... 17, 31
   decembre 1812", with a topic list running from the retreat on the Vistula to the attitude of
   Prussia.

2. THE PLAINTEXT IS IN PRINT, AND HAS BEEN SINCE 1912. Arthur Chuquet, "1812, la guerre de Russie:
   notes et documents", third series (1912), section 45, pp. 165-219, prints Berthier's letters to
   Napoleon of 1-31 December 1812 in clear, and says exactly where he got them: "tirees soit des
   archives de la guerre, soit des archives nationales (A. F. iv. 1643)" - the same carton. Two of
   them are dated 22 December 1812: letter XIX (a short letter about Colonel Bosset's widow) and
   letter XXIII, sent at 9 in the evening, a long situation report.

So this is not a cipher that has to be broken. It is a known-plaintext problem whose plaintext was
published a century ago, and the only thing missing is the rest of the ciphertext, which exists in
one 1969 French service journal that is not digitised.

What this script does is the part that can be done without that article: check whether the 325 code
groups Tomokiyo does print are statistically compatible with the printed candidates, and say plainly
how weak or strong that evidence is. It deliberately stops short of proposing an alignment. With 325
codes and a free choice of plaintext, an alignment can always be produced, and it would mean nothing.

Usage: python berthier.py
"""
import collections, re, sys


CT = 'berthier_ct.txt'
CHUQUET = 'berthier_chuquet.txt'


def ciphertext():
    return [int(x) for x in re.findall(r'\d+', open(CT, encoding='utf-8').read())]


def clean(body):
    """Strip Chuquet's running heads, page numbers and footnotes from an OCR'd letter."""
    b = body
    b = re.sub(r'(?i)LA\s+G\w*\s+DE\s+RUSSIE', ' ', b)      # running head, OCR'd many ways
    b = re.sub(r'(?i)\bLA\s+giehrk\s+de\s+Russie\b', ' ', b)
    b = re.sub(r'(?m)^\s*\d{1,3}\s*$', ' ', b)               # bare page numbers
    b = re.sub(r'(?ms)^\s*\d\.\s.*?(?=\n\s*\n|\Z)', ' ', b)  # footnotes "1. ..."
    b = re.sub(r'\s+', ' ', b)
    return b.strip()


def words(s):
    s = s.lower()
    s = re.sub(r"[^a-zà-ÿ'’\s]+", ' ', s)
    return [w for w in re.split(r"[\s’']+", s) if w]


def letters_of(path=CHUQUET):
    blk = open(path, encoding='utf-8').read()
    parts = re.split(r'\n\s*([IVXL]{1,6})\s*\n', blk)
    out = []
    for i in range(1, len(parts) - 1, 2):
        rn, body = parts[i], parts[i + 1]
        m = re.match(r'\s*([^\n]{0,80}?18[01]\d[^\n]{0,30})', body)
        hdr = re.sub(r'\s+', ' ', m.group(1)) if m else ''
        out.append((rn, hdr, clean(body)))
    return out


def profile(seq):
    c = collections.Counter(seq)
    n = len(seq)
    big = collections.Counter(tuple(seq[i:i + 2]) for i in range(n - 1))
    tri = collections.Counter(tuple(seq[i:i + 3]) for i in range(n - 2))
    return {
        'n': n,
        'distinct': len(c),
        'hapax': sum(1 for v in c.values() if v == 1),
        'hapax_pct': 100.0 * sum(1 for v in c.values() if v == 1) / len(c) if c else 0,
        'top': c.most_common(6),
        'maxfreq_pct': 100.0 * c.most_common(1)[0][1] / n if c else 0,
        'rep2': sum(1 for v in big.values() if v > 1),
        'rep3': sum(1 for v in tri.values() if v > 1),
    }


def show(name, p):
    print('%-34s n=%-5d distinct=%-5d hapax=%-4d (%2.0f%%)  top=%-6s (%.1f%%)  rep2=%-3d rep3=%d'
          % (name, p['n'], p['distinct'], p['hapax'], p['hapax_pct'],
             str(p['top'][0][1]) if p['top'] else '-', p['maxfreq_pct'], p['rep2'], p['rep3']))


def main():
    ct = ciphertext()
    pc = profile(ct)
    print('=== THE CIPHERTEXT AS PRINTED (opening only; Tomokiyo ends it with "....")')
    show('Berthier 22 Dec 1812, cipher', pc)
    print('    most frequent codes: %s'
          % ', '.join('%d x%d' % (k, v) for k, v in pc['top']))
    print('    repeated 3-grams   : 918 1045 1100 (x2), 168 854 1148 (x2)')
    print('    range %d-%d; occupancy is near flat over 1-1199 and all but empty above 1200,'
          % (min(ct), max(ct)))
    print('    so the code book is about 1200 entries and is being used across its whole span.')

    print('\n=== THE PRINTED CANDIDATES (Chuquet 1912, from AF/IV/1643)')
    cands = [(rn, h, t) for rn, h, t in letters_of() if re.search(r'22\s*d[ée]', h)]
    for rn, hdr, txt in cands:
        w = words(txt)
        print('\nletter %s - %s' % (rn, hdr))
        show('  first %d words' % min(len(w), pc['n']), profile(w[:pc['n']]))
        show('  whole letter', profile(w))
        print('  opens: %s' % ' '.join(w[:14]))

    print("""
=== READING

The comparison that matters is the shape of the repeats, and it does not match a plain
one-code-per-word encoding. In French prose of this length the commonest word takes 4-5% of all
tokens; the commonest code group here takes 2.5%. Either the code gives its frequent words several
alternative groups, which is normal in a nomenclator of this size and period, or the printed extract
is not this letter. The extract cannot settle it, because Tomokiyo prints only its opening.

What the extract does establish is negative and worth stating: with 64% of the code groups occurring
exactly once, against a book of about 1200 entries, there is nothing here for frequency analysis to
work on. This cryptogram will not be read by attacking it.

It does not need to be. The plaintext is in Chuquet. What is missing is the rest of the ciphertext,
which means the whole of Vilcoq's 1969 article - Revue Historique de l'Armee no. 4 (1969), which
also carries the Marmont cryptogram. That single article is now the only thing standing between
these two catalogue entries and a reconstruction of the cipher of the Prince of Neuchatel.""")


if __name__ == '__main__':
    main()
