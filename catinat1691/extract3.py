# Grand Chiffre 1691 letters, Memoires de Catinat (1819) t. II pp. 295-342 (MDZ bsb10720287 scans 329-376).
# Tokenise from the MDZ hOCR (word boxes kept, specks dropped), segment into letters, decode with Bazeries' table,
# word-segment the decode, write letters/*.txt and groups.json (every group with scan, bbox, decode).
import re, json, os, sys, unicodedata, collections, math, pickle, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segment
HERE = os.path.dirname(os.path.abspath(__file__)); FEU = os.path.join(HERE, '..', 'feuquieres')
tab = {}
for l in open(os.path.join(FEU, 'grand_chiffre_1691.tsv'), encoding='utf-8'):
    if l.startswith('#') or not l.strip():
        continue
    n, v = l.rstrip('\n').split('\t'); tab[int(n)] = v
CORR = {}   # (scan, x0, y0) -> corrected text, from corrections.tsv (image checks)
cf = os.path.join(HERE, 'corrections.tsv')
if os.path.exists(cf):
    for l in open(cf, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        p = l.rstrip('\n').split('\t')
        CORR[(int(p[0]), int(p[1]), int(p[2]))] = p[3]

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


def restore(word, disp):
    """word: normalised (u,i). disp: same length, with known letters or '?' at ambiguous positions."""
    pos = [p for p, c in enumerate(disp) if c == '?']
    base = list(word)
    for p, c in enumerate(disp):
        if c != '?':
            base[p] = c
    best = ''.join(base); bc = LEX2.get(best, 0)
    for mask in range(1, 1 << len(pos)):
        w = list(base)
        for k, p in enumerate(pos):
            if mask >> k & 1:
                w[p] = {'u': 'v', 'i': 'j'}.get(w[p], w[p])
        w = ''.join(w); c = LEX2.get(w, 0)
        if c > bc:
            best, bc = w, c
    if bc == 0 and pos:
        w = list(base)
        for p in pos:
            if w[p] == 'u' and (p == 0 or w[p - 1] in 'aeiou') and p + 1 < len(w) and w[p + 1] in 'aeiou':
                w[p] = 'v'
            if w[p] == 'i' and p == 0 and p + 1 < len(w) and w[p + 1] in 'aeiou':
                w[p] = 'j'
        best = ''.join(w)
    return best


def unit_text(v):
    """table value -> (norm chars for segmentation, display chars with '?' where u/v i/j is ambiguous)"""
    if v == 'NULL':
        return ('|', '|')
    if v == 'CANCEL':
        return ('<CANCEL>', '<CANCEL>')
    k = unicodedata.normalize('NFD', v.lower()); k = ''.join(c for c in k if unicodedata.category(c) != 'Mn')
    k = k.replace('persuad (ou) asseur', 'persuad').replace('persuad ou asseur', 'persuad').replace('rait ou roit', 'roit').replace('hi ou hy', 'hi')
    if re.fullmatch(r'[a-z]{1,2}-[a-z]{1,2}', k):
        a, b = k.split('-')
        nrm = ''; dsp = ''
        for x, y in zip(a, b):
            if x != y:
                nrm += x if x in 'iu' else y; dsp += '?'
            else:
                nrm += x; dsp += x
        return (nrm, dsp)
    k = re.sub(r"[^a-z]", '', k)
    nrm = k.replace('j', 'i').replace('v', 'u').replace('y', 'i')
    return (nrm, k)


def render(items):
    """items: list of dicts {kind: clear|num|bad, text, ...}. Returns reading string."""
    out = []; run = ''; disp = ''

    def flush():
        nonlocal run, disp
        if run:
            words = segment.seg(run); pos = 0; ws = []
            for w in words:
                ws.append(restore(w, disp[pos:pos + len(w)])); pos += len(w)
            out.append(' '.join(ws))
        run = ''; disp = ''
    for it in items:
        if it['kind'] == 'clear':
            flush(); out.append(it['text']); continue
        if it['kind'] == 'bad':
            flush(); out.append('[' + it['text'] + '!]'); continue
        n = int(it['text']); v = tab.get(n)
        if v is None:
            flush(); out.append('[%d!]' % n); continue
        if v == '?':
            flush(); out.append('[%d?]' % n); continue
        nrm, dsp = unit_text(v)
        if nrm == '|':
            flush(); out.append('|'); continue
        if nrm == '<CANCEL>':
            flush(); out.append('<CANCEL>'); continue
        run += nrm; disp += dsp
    flush()
    return ' '.join(out)


# ---- tokenise from hOCR
FIRST, LAST = 329, 376
toks = []
for s in range(FIRST, LAST + 1):
    t = open(os.path.join(HERE, 'hocr', '%d.html' % s), encoding='utf-8', errors='replace').read()
    words = []
    for m in re.finditer(r"<span class=['\"]ocrx_word['\"][^>]*title=['\"]bbox (\d+) (\d+) (\d+) (\d+)['\"][^>]*>(.*?)</span>", t, re.S):
        x0, y0, x1, y1 = map(int, m.groups()[:4])
        w = html.unescape(re.sub(r'<[^>]+>', '', m.group(5))).strip()
        if not w:
            continue
        w = CORR.get((s, x0, y0), w)
        w = re.sub(r'[Ͱ-ϿЀ-ӿ؀-ۿ]', '', w).strip()   # show-through junk (Greek, Cyrillic, Arabic glyphs)
        if not w or w in ('.', ',', ':', ';'):
            continue
        if w == '-':
            continue
        h = y1 - y0
        if h < 30 and re.fullmatch(r'[\d\.\-,;:\'•·`~_|!]*', w):
            continue   # speck
        words.append((w, (x0, y0, x1, y1)))
    # drop running head (first line: page number + PIECES / JUSTIFICATIVES) and signature marks
    body = []
    for w, bb in words:
        if bb[1] < 250 and re.fullmatch(r'\d{3}|PI[EÈ]CES|JUSTIFICATIVES\.?|\.', w):
            continue
        body.append((w, bb))
    for w, bb in body:
        for m in re.finditer(r'\d+[a-z]+\d*|\d+|[^\s\d\.,;:]+', w):
            tok = m.group(0)
            kind = 'num' if tok.isdigit() else ('flag' if re.fullmatch(r'\d+[a-z]+\d*', tok) else 'word')
            toks.append({'scan': s, 'kind': kind, 'text': tok, 'bbox': bb, 'ocr': w})
# strip "T. II. 20" signature marks: tokens 'T' 'II' followed by a number at page bottom
clean = []
i = 0
while i < len(toks):
    tk = toks[i]
    if tk['kind'] == 'word' and tk['text'] in ('T', 'Τ') and i + 2 < len(toks) and toks[i + 1]['text'] in ('II', 'ΙΙ', 'Il', 'IL') and toks[i + 2]['kind'] == 'num':
        i += 3; continue
    if tk['kind'] == 'word' and tk['text'] in ('г', '*', '•', '••', ':', 'I', '—', '-', '«', '»', '(', ')') and False:
        i += 1; continue
    clean.append(tk); i += 1
toks = clean

# ---- letters
letters = []; cur = None; i = 0


def words_at(i, n):
    return ' '.join(tk['text'] for tk in toks[i:i + n])


MONTHS = ('juillet', 'aout', 'août', 'septembre')


def is_header(i):
    tk = toks[i]
    if tk['kind'] != 'word' or tk['text'].lower() not in MONTHS:
        return None
    if not any(x['text'] == '1691' for x in toks[i + 1:i + 3]):
        return None
    before = [x['text'] for x in toks[max(0, i - 3):i]]
    after = [x['text'] for x in toks[i + 2:i + 7]]
    if 'LOUIS' in before:
        return i - 1 - before[::-1].index('LOUIS')
    if 'M' in after or 'Monsieur' in after:
        if i >= 4 and toks[i - 4]['text'] == 'A' and toks[i - 3]['text'] == 'Versailles':
            return i - 4
        return i - 1
    return None


while i < len(toks):
    tk = toks[i]
    if tk['kind'] == 'word' and tk['text'] == '(' and i + 4 < len(toks) and toks[i + 2]['text'] == ')' and toks[i + 3]['text'].lower().startswith('page'):
        i += 5; continue      # footnote marker "( n ) Page NN" of the 1819 edition
    if tk['kind'] == 'word' and tk['text'] == 'Pour' and words_at(i + 1, 3) == 'rendre la traduction':
        break
    h = None
    for j in range(i, min(i + 5, len(toks))):
        hj = is_header(j)
        if hj == i:
            h = j; break
    if h is not None:
        cur = {'id': 'L%d' % (len(letters) + 1), 'ref': toks[h]['text'], 'scan': tk['scan'], 'items': []}; letters.append(cur)
    if cur is not None:
        it = dict(tk)
        if it['kind'] == 'word':
            it['kind'] = 'clear'
        elif it['kind'] == 'flag':
            it['kind'] = 'bad'
        elif it['kind'] == 'num' and (it['text'] == '1691' or any(x['text'].lower() in MONTHS for x in toks[i + 1:i + 3])
                                       or (i >= 1 and toks[i - 1]['text'].lower() in ('du', 'le', 'ce') and any(x['text'].lower() in MONTHS + ('de',) for x in toks[i + 1:i + 3]) and len(it['text']) <= 2 and i >= 2 and toks[i - 2]['kind'] == 'word')):
            it['kind'] = 'clear'     # a date written in clear
        cur['items'].append(it)
    i += 1

meta = {'L1': 'Louvois to Catinat, Versailles, 8 July 1691', 'L2': 'Louvois to Catinat, Versailles, 9 July 1691',
        'L3': 'Louis XIV to Catinat, Versailles, 19 August 1691', 'L4': 'Louis XIV to Catinat, 24 August 1691',
        'L5': 'Louis XIV to Catinat, 29 August 1691', 'L6': 'Louis XIV to Catinat, Versailles, 6 September 1691',
        'L7': 'Louis XIV to Catinat, Fontainebleau, 14 September 1691'}
os.makedirs(os.path.join(HERE, 'letters'), exist_ok=True)
rows = []; allgroups = []
for L in letters:
    nums = [it for it in L['items'] if it['kind'] == 'num']
    bad = [it for it in L['items'] if it['kind'] == 'bad' or (it['kind'] == 'num' and int(it['text']) > 587)]
    unk = [it for it in L['items'] if it['kind'] == 'num' and tab.get(int(it['text'])) == '?']
    text = render(L['items'])
    groups = []
    last = None
    for it in L['items']:
        if it['scan'] != last:
            groups.append('\n[p.%d]' % (it['scan'] - 34)); last = it['scan']
        groups.append(it['text'] if it['kind'] != 'clear' else '<' + it['text'] + '>')
    fn = os.path.join(HERE, 'letters', L['id'] + '.txt')
    with open(fn, 'w', encoding='utf-8') as f:
        f.write('# %s %s\n# t. II from p. %d (MDZ scan %d); %d groups; %d OCR-bad; %d groups blank in Bazeries\n\n'
                % (L['id'], meta.get(L['id'], ''), L['scan'] - 34, L['scan'], len(nums), len(bad), len(unk)))
        f.write('## Reading (word-segmented; | = null/point; clear text as printed; [n?] = group blank in Bazeries; [n!] = OCR error)\n')
        f.write(text + '\n\n## Groups as printed\n' + ' '.join(groups) + '\n')
    for it in L['items']:
        allgroups.append({'letter': L['id'], 'scan': it['scan'], 'kind': it['kind'], 'text': it['text'], 'bbox': it['bbox'], 'ocr': it['ocr'],
                          'dec': tab.get(int(it['text'])) if it['kind'] == 'num' else None})
    rows.append((L['id'], meta.get(L['id'], ''), L['scan'] - 34, len(nums), len(bad), len(unk)))
    print(rows[-1])
json.dump(rows, open(os.path.join(HERE, 'letters_summary.json'), 'w'))
json.dump(allgroups, open(os.path.join(HERE, 'groups.json'), 'w'))
print('total groups', sum(r[3] for r in rows))
