"""Build an Italian character n-gram LM from the Nuntiaturberichte OCR (papal diplomatic Italian, 1533-1559),
filtering out German editorial text. Output: it_ngrams.json {n: {gram: count}} for n=1..5, alphabet a-z + space.
"""
import re, json, pathlib, collections, unicodedata, glob
HERE = pathlib.Path(__file__).parent
IT = set('che di la il non per con si se et le della delle del dello alla alle quello questo questa sua suo che ma sono essere '
         'da dal dalla come anche ancora tutto tutti molto piu più cosa cose nostro vostra signore stato haver havere fatto '
         'quale quali questi quelli loro noi voi lui lei gli una uno mi ti ci vi ne lo li ha hanno era erano sia siano '
         'perche perché poi qui qua ogni altro altra altri senza sopra sotto dopo prima tanto quanto bene male dio papa'.split())
DE = set('der die das und ist nicht von zu den dem des mit auf für ein eine einer eines im am an bei nach über unter vor '
         'aus auch sich wird wurde werden hat hatte haben sein seine seiner ihm ihn ihr ihre als wie noch nur schon oder '
         'aber dass daß wenn weil brief nuntius kardinal papst kaiser könig reichstag anm vgl siehe ebenda abschr konz'.split())

def normalize(s):
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = s.replace('v', 'u').replace('j', 'i').replace('k', 'c').replace('w', 'u').replace('y', 'i')
    s = re.sub(r"[’'`]", '', s)                    # l'una -> luna (16th c. cipher practice: no apostrophes)
    s = re.sub(r'[^a-z]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def italian_paragraphs(text):
    out = []
    for para in re.split(r'\n\s*\n', text):
        words = re.findall(r'[A-Za-zÀ-ÿ]+', para.lower())
        if len(words) < 12: continue
        it = sum(w in IT for w in words); de = sum(w in DE for w in words)
        if it >= 0.08 * len(words) and it > 3 * de:
            out.append(para)
    return out

def main():
    corpus = []
    for p in sorted(HERE.glob('nb_*.txt')):
        t = p.read_text(encoding='utf-8', errors='ignore')
        paras = italian_paragraphs(t)
        n = sum(len(x) for x in paras)
        print(f'{p.name}: {len(paras)} Italian paragraphs, {n//1000}k chars')
        corpus += paras
    text = ' '.join(normalize(x) for x in corpus)
    (HERE / 'corpus_it.txt').write_text(text, encoding='utf-8')
    print('total normalized chars:', len(text))
    grams = {}
    for n in range(1, 6):
        c = collections.Counter(text[i:i+n] for i in range(len(text) - n + 1))
        grams[n] = {k: v for k, v in c.items() if v >= (1 if n < 4 else 2)}
        print(f'{n}-grams: {len(grams[n])}')
    json.dump(grams, open(HERE / 'it_ngrams.json', 'w'))
    words = collections.Counter(text.split())
    json.dump(words.most_common(30000), open(HERE / 'it_words.json', 'w'))
    print('top words:', words.most_common(40))

if __name__ == '__main__':
    main()
