"""Parse the MysteryTwister transcript of ASV Segr. Stato Spagna 1A/2 (Vatican Challenge Part 5)."""
import re, pathlib, collections, sys
SRC = pathlib.Path(__file__).with_name('ASV_i1025_SdS_Spain_IA-2.txt')

def load(path=SRC):
    """Return list of pages: (image_name, [segments]) where segment = ('C', cleartext) or ('D', [digit tokens]).
    A digit token is a string like '7', '7^.', '0^,', '3?', '2/', etc."""
    text = path.read_text(encoding='utf-8', errors='replace')
    pages, cur, name = [], [], None
    # split on IMAGE NAME headers
    parts = re.split(r'#IMAGE NAME:\s*(\S+)', text)
    for i in range(1, len(parts), 2):
        name, body = parts[i], parts[i+1]
        if name.endswith('.jpg-073v.jpg'): continue          # header line
        segs = []
        pos = 0
        for m in re.finditer(r'<CLEARTEXT([^>]*)>', body, re.S):
            digits = body[pos:m.start()]
            toks = tokens(digits)
            if toks: segs.append(('D', toks))
            segs.append(('C', m.group(1).strip()))
            pos = m.end()
        toks = tokens(body[pos:])
        if toks: segs.append(('D', toks))
        pages.append((name, segs))
    return pages

def tokens(s):
    s = s.replace('\n', ' ')
    # a token = digit followed by optional marks
    return re.findall(r'\d(?:\^[.,]?|_[.,]?|\?|<-|/|,)*', s)

def digit_stream(pages, keep_marks=True):
    out = []
    for name, segs in pages:
        for kind, v in segs:
            if kind == 'D':
                out.append(v if keep_marks else [t[0] for t in v])
    return out

if __name__ == '__main__':
    pages = load()
    runs = digit_stream(pages)
    flat = [t for r in runs for t in r]
    print(f'{len(pages)} pages, {len(runs)} digit runs, {len(flat)} digit tokens')
    plain = [t[0] for t in flat]
    c = collections.Counter(plain)
    print('digit freq:', ' '.join(f'{d}:{c[d]}' for d in sorted(c)))
    marks = collections.Counter(t[1:] for t in flat if len(t) > 1)
    print('marks:', marks.most_common())
    marked = collections.Counter(t for t in flat if len(t) > 1)
    print('marked digits:', marked.most_common(20))
    # digit bigrams (within runs)
    bg = collections.Counter()
    for r in runs:
        d = [t[0] for t in r]
        for a, b in zip(d, d[1:]): bg[a+b] += 1
    print('\nbigram matrix (row=first, col=second):')
    print('    ' + ''.join(f'{d:>5}' for d in '0123456789'))
    for a in '0123456789':
        print(f'{a}   ' + ''.join(f'{bg[a+b]:>5}' for b in '0123456789'))
    # what follows / precedes each digit
    print('\nrun lengths:', sorted(len(r) for r in runs))
    print('\ncleartext fragments:')
    for name, segs in pages:
        for kind, v in segs:
            if kind == 'C': print(f'  [{name}] {v[:120]}')
