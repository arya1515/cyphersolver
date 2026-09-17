import re, json, os, sys, unicodedata, collections, math, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segment
HERE = os.path.dirname(os.path.abspath(__file__)); FEU = os.path.join(HERE, '..', 'feuquieres')
t = open(os.path.join(FEU, 'catinat1819_bsb10720287.txt'), encoding='utf-8').read()
pages = re.split(r'\n=====SCAN (\d+)=====\n', t)
d = {int(pages[i]): pages[i + 1] for i in range(1, len(pages), 2)}
tab = {}
for l in open(os.path.join(FEU, 'grand_chiffre_1691.tsv'), encoding='utf-8'):
    if l.startswith('#') or not l.strip():
        continue
    n, v = l.rstrip('\n').split('\t'); tab[int(n)] = v

# unmerged lexicon for v/j restoration
P2 = os.path.join(HERE, 'lex2.pkl')
if os.path.exists(P2):
    LEX2 = pickle.load(open(P2, 'rb'))
else:
    LEX2 = collections.Counter()
    for f in ['catinat1819_bsb10720286.txt', 'catinat1819_bsb10720287.txt', 'catinat1819_bsb10720288.txt',
              'rousset4.txt', 'feuq5.txt', 'masque_de_fer_1893.txt']:
        tt = open(os.path.join(FEU, f), encoding='utf-8', errors='replace').read()
        for w in re.findall(r"[A-Za-zÀ-ÿ]+", tt):
            w2 = unicodedata.normalize('NFD', w.lower()); w2 = ''.join(c for c in w2 if unicodedata.category(c) != 'Mn')
            LEX2[w2] += 1
    pickle.dump(LEX2, open(P2, 'wb'))

SMALL = {'le', 'la', 'de', 'du', 'en', 'et', 'ce', 'ne', 'se', 'si', 'il', 'je', 'me', 'au', 'on', 'ou', 'vous', 'les',
         'des', 'que', 'qui', 'sur', 'par', 'pas', 'son', 'mon', 'est', 'roy', 'peu', 'ces', 'vos', 'lui', 'luy', 'non',
         'cet', 'car', 'fin', 'mal', 'bon'}


def restore(word, amb):
    pos = [p for p in amb if p < len(word) and word[p] in 'ui']
    best = word; bc = LEX2.get(word, 0)
    for mask in range(1, 1 << len(pos)):
        w = list(word)
        for k, p in enumerate(pos):
            if mask >> k & 1:
                w[p] = {'u': 'v', 'i': 'j'}[w[p]]
        w = ''.join(w); c = LEX2.get(w, 0)
        if c > bc:
            best, bc = w, c
    if bc == 0 and pos:
        w = list(word)
        for p in pos:
            if w[p] == 'u' and (p == 0 or word[p - 1] in 'aeiou') and p + 1 < len(word) and word[p + 1] in 'aeiou':
                w[p] = 'v'
            if w[p] == 'i' and p == 0 and p + 1 < len(word) and word[p + 1] in 'aeiou':
                w[p] = 'j'
        best = ''.join(w)
    return best


def unit_text(v):
    if v == 'NULL':
        return ('|', [], True)
    if v == 'CANCEL':
        return ('<CANCEL>', [], True)
    k = unicodedata.normalize('NFD', v.lower()); k = ''.join(c for c in k if unicodedata.category(c) != 'Mn')
    k = k.replace('persuad (ou) asseur', 'persuad').replace('persuad ou asseur', 'persuad').replace('rait ou roit', 'roit').replace('hi ou hy', 'hi')
    amb = []
    if re.fullmatch(r'[a-z]{1,2}-[a-z]{1,2}', k):
        a, b = k.split('-')
        out = ''
        for x, y in zip(a, b):
            if x != y:
                amb.append(len(out))
            out += x if x in 'iu' else (y if y in 'iu' else x)
        k = out
    k = re.sub(r"[^a-z]", '', k)
    isword = len(k) > 3 or k in SMALL
    return (k, amb, isword)


def render(items):
    units = []
    for s, k, tx in items:
        if k == 'word':
            units.append(('clear', tx, None, None))
        elif k == 'flag':
            units.append(('bad', '[' + tx + '!]', None, None))
        else:
            n = int(tx); v = tab.get(n)
            if v is None:
                units.append(('bad', '[%d!]' % n, None, None))
            elif v == '?':
                units.append(('unk', '[%d?]' % n, None, None))
            else:
                ch, amb, isw = unit_text(v); units.append(('code', v, ch, amb))
    out = []; state = {'run': '', 'amb': set()}

    def flush():
        run = state['run']
        if run:
            words = segment.seg(run); pos = 0; ws = []
            for w in words:
                a = {p - pos for p in state['amb'] if pos <= p < pos + len(w)}
                ws.append(restore(w, a)); pos += len(w)
            out.append(' '.join(ws))
        state['run'] = ''; state['amb'] = set()
    for kind, disp, ch, amb in units:
        if kind == 'code' and ch not in ('|', '<CANCEL>'):
            for p in amb:
                state['amb'].add(len(state['run']) + p)
            state['run'] += ch
        else:
            flush()
            if kind == 'code' and ch == '|':
                out.append('|')
            else:
                out.append(disp)
    flush()
    return ' '.join(out)


FIRST, LAST = 329, 376
toks = []
for s in range(FIRST, LAST + 1):
    x = re.sub(r'bsb\d+_\d+', '', d[s]).strip()
    x = re.sub(r'^\s*(\d{3}\s+PI[EÈ]CES|JUSTIFICATIVES\s*\.\s*\d{3})', '', x)
    x = re.sub(r'T\.\s*II\s*\.\s*\d+\s*$', '', x.strip())
    for m in re.finditer(r'\d+[a-z]+\d*|\d+|[^\s\d\.,;:]+', x):
        tok = m.group(0)
        kind = 'num' if tok.isdigit() else ('flag' if re.fullmatch(r'\d+[a-z]+\d*', tok) else 'word')
        toks.append((s, kind, tok))

letters = []; cur = None; i = 0


def words_at(i, n):
    return ' '.join(tk[2] for tk in toks[i:i + n])


while i < len(toks):
    s, k, tx = toks[i]
    if k == 'word' and tx == '(' and i + 4 < len(toks) and toks[i + 1][1] == 'num' and toks[i + 2][2] == ')' and toks[i + 3][2].lower().startswith('page'):
        cur = {'id': '(' + toks[i + 1][2] + ')', 'ref': toks[i + 4][2], 'scan': s, 'items': []}; letters.append(cur); i += 5; continue
    if k == 'word' and tx == 'A' and words_at(i + 1, 2) == 'Versailles le' and i + 4 < len(toks) and toks[i + 4][2] == 'juillet' and cur and cur['id'] == '(7)' and sum(1 for it in cur['items'] if it[1] == 'num') > 100:
        cur = {'id': '(7b)', 'ref': '42', 'scan': s, 'items': []}; letters.append(cur)
    if k == 'word' and tx == 'Pour' and words_at(i + 1, 3) == 'rendre la traduction':
        break
    if cur is not None:
        cur['items'].append((s, k, tx))
    i += 1

meta = {'(7)': 'Louvois to Catinat, Versailles, 8 July 1691', '(7b)': 'Louvois to Catinat, Versailles, 9 July 1691',
        '(8)': 'Louis XIV to Catinat, Versailles, 19 August 1691', '(9)': 'Louis XIV to Catinat, 24 August 1691',
        '(11)': 'Louis XIV to Catinat, [29] August 1691', '(12)': 'Louis XIV to Catinat, 6 September 1691 (first extract)',
        '(13)': 'Louis XIV to Catinat, 6 September 1691 (second extract)', '(14)': 'Louis XIV to Catinat, Fontainebleau, 14 September 1691'}
os.makedirs(os.path.join(HERE, 'letters'), exist_ok=True)
rows = []
for L in letters:
    nums = [it for it in L['items'] if it[1] == 'num']
    bad = [it for it in L['items'] if it[1] == 'flag' or (it[1] == 'num' and int(it[2]) > 587)]
    unk = [it for it in L['items'] if it[1] == 'num' and tab.get(int(it[2])) == '?']
    text = render(L['items'])
    groups = ' '.join(it[2] if it[1] != 'word' else '<' + it[2] + '>' for it in L['items'])
    fn = os.path.join(HERE, 'letters', L['id'].strip('()') + '.txt')
    with open(fn, 'w', encoding='utf-8') as f:
        f.write('# %s %s\n# t. II from p. %d (MDZ scan %d); %d groups; %d OCR-bad; %d groups blank in Bazeries\n\n'
                % (L['id'], meta.get(L['id'], ''), L['scan'] - 34, L['scan'], len(nums), len(bad), len(unk)))
        f.write('## Reading (word-segmented; | = null/point; <...> = printed in clear; [n?] = group blank in Bazeries; [n!] = OCR error)\n')
        f.write(text + '\n\n## Groups as printed\n' + groups + '\n')
    rows.append((L['id'], meta.get(L['id'], ''), L['scan'] - 34, len(nums), len(bad), len(unk)))
    print(rows[-1])
json.dump(rows, open(os.path.join(HERE, 'letters_summary.json'), 'w'))
