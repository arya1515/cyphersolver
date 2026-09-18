"""Assemble the reading: hand-read lines from gold/labels.txt where they exist, the machine
decode (draft9.txt) elsewhere, marked. Writes trans/reading.txt."""
import json, re, math, glob, unicodedata, collections
d = json.load(open('raince_tokens.json'))
gold = {}
for ln in open('gold/labels.txt'):
    if ln.startswith('#') or not ln.strip(): continue
    p, l, s = ln.split(); gold[(p, int(l))] = s
mach = {}
page = None
for ln in open('draft9.txt'):
    ln = ln.rstrip('\n')
    if ln.startswith('## '): page = ln[3:]; continue
    if not ln.strip(): continue
    n, body = ln.split(' ', 1); mach[(page, int(n))] = body

# word segmentation for readability
def norm(t):
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    t = t.lower().replace('j','i').replace('v','u').replace('w','u')
    return re.sub(r"[^a-z]+", ' ', t)
cnt = collections.Counter()
for f in glob.glob('../dubellay/ref/legrand3_*.txt')+glob.glob('../nevers1593/*.txt')+glob.glob('../debosnys/corpus/fr*.txt'):
    try: cnt.update(norm(open(f, encoding='utf-8', errors='ignore').read()).split())
    except Exception: pass
N = sum(cnt.values()); LOGP = {w: math.log(c/N) for w, c in cnt.items() if c >= 3}
def seg(s):
    # segment each ?-free run separately; ? stays as its own token
    parts = []
    for chunk in re.split(r'(\?+)', s):
        if not chunk: continue
        if chunk[0] == '?': parts.append(chunk); continue
        parts.append(_seg(chunk))
    return ' '.join(parts)

def _seg(s):
    n = len(s); best = [-1e18]*(n+1); bk = [0]*(n+1); best[0] = 0.0
    for i in range(1, n+1):
        for L in range(1, min(14, i)+1):
            w = s[i-L:i]
            sc = LOGP.get(w, -5.0-2.6*L)
            if best[i-L]+sc > best[i]: best[i] = best[i-L]+sc; bk[i] = L
    out = []; i = n
    while i > 0:
        L = bk[i]; out.append(s[i-L:i]); i -= L
    return ' '.join(reversed(out))

TITLE = {'f29r': 'p. 29  (13 May 1526, to Montmorency - first ciphered page, lines 11-35)',
         'f30v': 'p. 30  (13 May 1526 - second page, whole)',
         'f31r': 'p. 31  (13 May 1526 - third page, the 25 ciphered lines; the clear close follows in trans/p31_clear_close.txt)',
         'f105r':'p. 105 (20 Nov 1526, to Montmorency - the unglossed lower part)'}
out = []
out.append("# Raince, BnF fr. 2984: the reading of the ciphered residue")
out.append("")
out.append("Each line is given twice: `H` = read glyph by glyph off the microfilm against the")
out.append("measured key, one character per segmented token (gold/labels.txt); `M` = the machine")
out.append("decode (classifier + period-French 6-gram beam, draft9.txt) for lines not yet read by")
out.append("hand, which is right on about 85-90 % of letters and is NOT a reading. `?` = a token")
out.append("that did not resolve; word spacing is supplied by a lexicon segmenter and is a reading")
out.append("aid, not evidence. Lines run on: a word broken at a line end continues on the next.")
out.append("")
nh = nm = 0
for pg in ['f29r','f30v','f31r','f105r']:
    out.append(''); out.append('## ' + TITLE[pg]); out.append('')
    for k in range(1, len(d['regions'][pg]['lines'])+1):
        if (pg, k) in gold:
            s = gold[(pg, k)].replace('_','').replace('C','(con)')
            out.append(f"{k:02d} H | " + seg(s)); nh += 1
        else:
            out.append(f"{k:02d} M | " + seg(mach.get((pg,k),''))); nm += 1
open('trans/reading.txt','w').write('\n'.join(out)+'\n')
print('hand', nh, 'machine', nm)
