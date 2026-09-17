# Compare our decode of the 8 July 1691 and 19 Aug 1691 letters against the clear texts Bazeries printed in 1893
# (Le Masque de fer, pp. 42-46 and pp. 292-300). Letter-level agreement after normalisation measures the OCR error
# rate of the MDZ hOCR of the cipher pages plus any residual table errors.
import re, os, unicodedata, difflib, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FEU = os.path.join(HERE, '..', 'feuquieres')
mf = open(os.path.join(FEU, 'masque_de_fer_1893.txt'), encoding='utf-8', errors='replace').read().split('=====PDFPAGE=====')


def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.replace('j', 'i').replace('v', 'u').replace('y', 'i')
    return re.sub(r'[^a-z]', '', s)


def bazeries_clear(pages, start_marker, end_marker):
    txt = ' '.join(mf[p] for p in pages)
    txt = re.sub(r'\s+', ' ', txt)
    a = txt.find(start_marker); b = txt.find(end_marker, a)
    txt = txt[a:b]
    txt = re.sub(r'\(\d\)', '', txt)            # footnote marks
    txt = re.sub(r'\d+ LE MASQUE DE FE[RD]\.?', '', txt)
    txt = re.sub(r'LEV[ÉE]E DU SI[ÈE]GE DE CONI\. \d+', '', txt)
    txt = re.sub(r'PREUVE DE L.EXACTITUDE DU CHIFFRE\. \d+', '', txt)
    txt = txt.replace('«', ' ').replace('- ', '')
    return txt


def our_reading(fn):
    t = open(os.path.join(HERE, 'letters', fn), encoding='utf-8').read()
    r = t.split('## Reading')[1].split('## Groups')[0]
    r = r.split('\n', 1)[1]
    r = re.sub(r'\[[^\]]*\]', '', r)   # drop flags
    return r


def compare(name, ours, theirs):
    a = norm(ours); b = norm(theirs)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    same = sum(bl.size for bl in sm.get_matching_blocks())
    print('%s: ours %d chars, Bazeries %d chars, matching %d (%.1f%% of Bazeries)' % (name, len(a), len(b), same, 100.0 * same / len(b)))
    # list the differing stretches (first 40)
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal' and (i2 - i1 > 1 or j2 - j1 > 1):
            print('   %-8s ours[%s] vs baz[%s]   ...%s|%s|%s' % (tag, a[i1:i2], b[j1:j2], b[max(0, j1 - 15):j1], b[j1:j2], b[j2:j2 + 15]))
            n += 1
            if n >= 60:
                break


if __name__ == '__main__':
    # 8 July: pdf pages 57-60, from "Monsieur, l'ordinaire" to "M. LOUVOIS"
    b8 = bazeries_clear(range(57, 61), 'Monsieur, l', 'M. LOUVOIS')
    o8 = our_reading('L1.txt')
    o8 = o8[o8.find('Monsieur'):]
    compare('8 July 1691', o8, b8)
    # 19 Aug: pdf pages 323-326 (clear text after the cipher), from "M. Catinat, j" to "Écrit à Versailles" / "LOUIS"
    b19 = bazeries_clear(range(323, 327), 'Catinat, j', 'LOUIS')
    o19 = our_reading('L3.txt')
    o19 = o19[o19.find('Catinat'):]
    compare('19 Aug 1691', o19, b19)
