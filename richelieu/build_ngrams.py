"""Build French letter n-gram statistics (normalized to a 22-letter 17th-c. alphabet).

Alphabet: a b c d e f g h i l m n o p q r s t u x y z   (j->i, v->u, k->c, w->u, accents stripped)
Output: fr_quadgrams.json  {quadgram: count}
"""
import requests, unicodedata, re, json, collections, pathlib, sys

HERE = pathlib.Path(__file__).parent
TEXTS = {
    # Gutenberg plain-text French sources (mix of 17th-19th c.)
    'sevigne_lettres': 'https://www.gutenberg.org/cache/epub/30926/pg30926.txt',   # Mme de Sévigné, Lettres
    'retz_memoires': 'https://www.gutenberg.org/cache/epub/36297/pg36297.txt',     # Cardinal de Retz
    'trois_mousq': 'https://www.gutenberg.org/cache/epub/13951/pg13951.txt',       # Dumas (17th c. setting, modern French)
    'pascal_provinciales': 'https://www.gutenberg.org/cache/epub/12977/pg12977.txt',
    'corneille_cid': 'https://www.gutenberg.org/cache/epub/14954/pg14954.txt',
}

def normalize(s: str) -> str:
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = s.replace('j', 'i').replace('v', 'u').replace('k', 'c').replace('w', 'u')
    s = s.replace('œ', 'oe').replace('æ', 'ae').replace('ß', 'ss')
    return re.sub(r'[^a-z]', '', s.replace('j','i'))

def main():
    corpus = ''
    for name, url in TEXTS.items():
        p = HERE / f'corpus_{name}.txt'
        if not p.exists():
            r = requests.get(url, timeout=60)
            if r.status_code != 200:
                print('skip', name, r.status_code); continue
            p.write_text(r.text, encoding='utf-8')
        t = p.read_text(encoding='utf-8', errors='ignore')
        # strip gutenberg header/footer
        a = t.find('*** START'); b = t.find('*** END')
        if a > 0: t = t[a:]
        if b > 0: t = t[:b]
        n = normalize(t)
        print(name, len(n))
        corpus += n + 'zzzz'  # separator noise, negligible
    counts = collections.Counter(corpus[i:i+4] for i in range(len(corpus)-3))
    uni = collections.Counter(corpus)
    tot = sum(uni.values())
    print('letters:', ' '.join(f'{k}:{100*v/tot:.1f}' for k, v in uni.most_common()))
    json.dump(counts, open(HERE / 'fr_quadgrams.json', 'w'))
    print('quadgrams:', len(counts))

if __name__ == '__main__':
    main()
