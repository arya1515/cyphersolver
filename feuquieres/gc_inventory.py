# Unit inventory of Bazeries' Grand Chiffre de 1691 (grand_chiffre_1691.tsv), normalised, as the design template
# for the 367-group petit chiffre ("il ne differait du grand que par son nombre de groupes moins eleve", p. 272).
import re, unicodedata, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    t = t.replace("'", '')
    return re.sub(r'[^a-z ]', '', t).strip()

LETTER_MAP = {'i-j': 'i', 'u-v': 'u', 'ia-ja': 'ia', 'ie-je': 'ie', 'iu-ju': 'iu', 'io-jo': 'io', 'ua-va': 'va',
              'ue-ve': 've', 'eu-ev': 'eu', 'hi ou hy': 'hi', 'rait ou roit': 'roit', 'persuad ou asseur': 'persuad',
              'geneve': 'geneve', 'sa majeste': 'samajeste', 'le roy': 'leroy', 'vallee de luzerne': 'luzerne',
              'vallee de saint-martin': 'saintmartin', 'vallee de pragelas': 'pragelas',
              'monsieur de savoye': 'savoye', 'monsieur de rebenac': 'rebenac', "d'angrogne": 'angrogne',
              "j'ay": 'jay', "qu'il": 'quil'}

def load():
    table = {}
    for l in open(os.path.join(HERE, 'grand_chiffre_1691.tsv'), encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        n, v = l.rstrip('\n').split('\t')
        table[int(n)] = v
    letters = collections.defaultdict(list); sylls = collections.defaultdict(list); words = collections.defaultdict(list)
    nulls = []; unknown = []
    for n, v in table.items():
        if v == '?':
            unknown.append(n); continue
        if v in ('NULL', 'CANCEL'):
            nulls.append(n); continue
        k0 = unicodedata.normalize('NFD', v.lower())
        k0 = ''.join(c for c in k0 if unicodedata.category(c) != 'Mn').replace('(ou)', 'ou').replace('?', '').strip()
        k = LETTER_MAP.get(k0)
        if k is None:
            k = norm(v)
        if len(k) == 1:
            letters[k].append(n)
        elif len(k) <= 3 and not k in ('les', 'ces', 'des', 'pas', 'peu', 'fin', 'car', 'sur', 'mon', 'son', 'qui',
                                        'que', 'lui', 'luy', 'non', 'cet', 'vos', 'est', 'par', 'ni', 'et', 'en',
                                        'le', 'la', 'de', 'ne', 'ce', 'du', 'on', 'au', 'ou', 'si', 'il', 'y', 'nu',
                                        'vu', 'mal', 'bon', 'ces', 'ast', 'ent', 'nt', 'st', 'es', 'is', 'it', 'us',
                                        'oit', 'in', 'arm'):
            sylls[k].append(n)
        else:
            words[k].append(n)
    return table, letters, sylls, words, nulls, unknown

if __name__ == '__main__':
    table, letters, sylls, words, nulls, unknown = load()
    print('letters', {k: len(v) for k, v in sorted(letters.items())})
    print('syllables', len(sylls), sorted(sylls))
    print('words', len(words), sorted(words))
    print('nulls', len(nulls), 'unknown', len(unknown))
