# -*- coding: utf-8 -*-
"""Merged key + decoder for the Lope Hurtado 1523-24 letters (retry step, 2026-09-21).

  python decode_merged.py --build          # rebuild key_merged.tsv from the source keys
  python decode_merged.py                  # decode every letter, print coverage
  python decode_merged.py --kwic xun xor   # contexts of given tokens across all letters
  python decode_merged.py --open           # all unvalued tokens with counts and contexts

Priority when building: key_1524 additions > key_1524 > key_1523 additions/r9667 > key_retry
(this session's values) > 1522 values re-read in 1524 notation > 1522 key_codes (code groups only;
the 1522 letter-sign notation differs, so 1522 single signs are not imported). Later sources never
overwrite; a differing value is recorded in the conflict column.
"""
import re, sys, io, os, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
L1522 = os.path.join(HERE, '..', 'lopehurtado')
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SOURCES = [  # (file, source label, is_1522_notation)
    ('key_1524_additions.tsv', '1524-add', False),
    ('key_1524.tsv', '1524', False),
    ('key_1523_additions.tsv', '1523-add', False),
    ('key_1523_r9667.tsv', '1523-r9667', False),
    ('key_retry.tsv', 'retry-2026-09-21', False),
    (os.path.join(L1522, 'key_1522_from1524.tsv'), '1522-in-1524-notation', False),
    (os.path.join(L1522, 'key_1522_from1524_B.tsv'), '1522-B', 'codes'),
    (os.path.join(L1522, 'key_codes.tsv'), '1522', 'codes'),
]
CODE_RE = re.compile(r'^[a-zɣʃ3][a-zɡɣᵹεƀ]{1,3}$')


def norm(code):
    return code.replace('ɣ', 'y').replace('ɡ', 'g').replace('ᵹ', 'ε')


def build():
    rows, seen = [], {}
    for fn, label, only_codes in SOURCES:
        p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
        if not os.path.exists(p):
            continue
        for line in open(p, encoding='utf-8'):
            if line.startswith(('code\t', '#')) or not line.strip():
                continue
            f = line.rstrip('\n').split('\t') + ['', '', '']
            code, plain, conf, src = f[0].strip(), f[1].strip(), f[2].strip(), f[3].strip()
            if only_codes and not CODE_RE.match(code):
                continue
            k = norm(code) if only_codes else code
            if k in seen:
                r = seen[k]
                if plain.split(' (')[0] != r['plain'].split(' (')[0]:
                    r['conflict'].append(f'{label}: {plain} [{conf}]')
                continue
            r = dict(code=k, plain=plain, conf=conf or 'probable', source=f'{label}: {src}', conflict=[])
            seen[k] = r
            rows.append(r)
    with open(os.path.join(HERE, 'key_merged.tsv'), 'w', encoding='utf-8') as o:
        o.write('code\tplain\tconfidence\tsource\tconflicts\n')
        for r in rows:
            o.write('\t'.join([r['code'], r['plain'], r['conf'], r['source'], ' | '.join(r['conflict'])]) + '\n')
    print(f'key_merged.tsv: {len(rows)} entries, {sum(1 for r in rows if r["conflict"])} with conflicts')


def load_key():
    K = {}
    for line in open(os.path.join(HERE, 'key_merged.tsv'), encoding='utf-8'):
        if line.startswith('code\t'):
            continue
        f = line.rstrip('\n').split('\t')
        if f[2] in ('possible', 'rejected'):
            continue
        plain = f[1]
        plain = re.sub(r'\s*\((letter|spelled|whole run|clear abbreviation)[^)]*\)', '', plain)
        plain = re.sub(r'\s*\(.*\)$', '', plain).strip()
        plain = {'vuestra magestad': 'V.Md', 'Rey de Francia': 'ReyFr', 'Rey de Inglaterra': 'ReyIng'}.get(plain, plain)
        plain = plain.replace(' ', '_')
        K[f[0]] = (plain, f[2])
        if re.fullmatch(r'ɣ[a-z]{1,2}', f[0]):
            K.setdefault('y' + f[0][1:], (plain, f[2]))
    return K


# ---------------------------------------------------------------- letters
def strip_clear(s):
    s = re.sub(r'\((heading|hyphen[^)]*)\)', ' ', s)
    s = re.sub(r'<([^ >]+) underlined>', r'', s)
    return re.sub(r'\[[^\]]*\]', ' | ', s)


def letters():
    L = collections.OrderedDict()

    def simple(fn, rec, pat=r'^([A-Za-z]?\d+)\s+(.*)$'):
        out = []
        for line in open(os.path.join(HERE, fn), encoding='utf-8'):
            if line.startswith('#') or line.startswith('=='):
                continue
            m = re.match(pat, line.strip())
            if m:
                out.append((m.group(1), strip_clear(m.group(2))))
        L[rec] = out

    simple('r9683_cipher.txt', 'R9683')
    simple('r9695_cipher.txt', 'R9695')
    simple('r9867_cipher.txt', 'R9867')
    simple('r9846_cipher.txt', 'R9846')
    # R9667 runs
    out, cur = [], None
    for line in open(os.path.join(HERE, 'r9667_cipher.txt'), encoding='utf-8'):
        m = re.match(r'^\s*RUN ([A-F])[^:]*:\s*(.*)$', line)
        if m:
            cur = m.group(1); s = m.group(2)
        elif cur and line.startswith('  ') and not line.strip().startswith('['):
            s = line
        else:
            if line.startswith('#') or line.startswith('(') or line.startswith('##'):
                cur = None if line.startswith('(') else cur
            continue
        s = s.replace('Bens.', '').replace('t8-', 't8')
        s = strip_clear(s)
        if s.replace('|', '').strip():
            out.append((cur, s))
    L['R9667'] = out
    # R9866/68/69 from the read_*.md transcription blocks
    for rec in ('R9866', 'R9868', 'R9869'):
        t = open(os.path.join(HERE, f'read_{rec.lower()}.md'), encoding='utf-8').read()
        t = t.split('## Transcription', 1)[1].split('## Decoding', 1)[0].split('## Readings', 1)[0]
        out = []
        for line in t.splitlines():
            m = re.match(r'^(R\d+ l\d+|h)\s+(.*)$', line.strip())
            if m and m.group(1) != 'h':
                s = strip_clear(m.group(2))
                if s.replace('|', '').strip():
                    out.append((m.group(1), s))
        L[rec] = out
    return L


def clean_tok(t):
    t = t.strip()
    t = t.strip('~')
    t = re.sub(r'\(\?\)$', '', t).rstrip('?')
    t = ALIAS.get(t, t)
    if re.fullmatch(r'ɣ[a-z]{1,2}', t):
        t = 'y' + t[1:]
    return t


NOSPLIT = {'⁝φ', 'ʒσ', 'ʃʇ', 'ʃ̄'}
ALIAS = {'T̄': '⊤', '⁝φ': 'ʑφ', 'ɣʇʇ': 'ɣ̶', 'xyg': 'xig', 'm̲': 'm̶', 'ɣ': 'y'}


def tokens(line):
    toks = []
    for t in line.split():
        if t in ('|', '/', './', '⁞', '.', '-', '--'):
            toks.append('|') if t == '|' else None
            continue
        t = clean_tok(t)
        if t:
            toks.append(t)
    return toks


def segment(tok, K):
    """greedy longest-match of an unknown compound token into keyed signs; None if impossible"""
    if re.fullmatch(r'[a-zʃɣ3][a-z]+', tok) or tok in NOSPLIT:
        return None  # a latin-letter group is a code, never split it into letter signs
    out, i = [], 0
    while i < len(tok):
        for j in range(len(tok), i, -1):
            if tok[i:j] in K:
                out.append(K[tok[i:j]][0]); i = j; break
        else:
            return None
    return out if len(out) > 1 else None


def decode_line(toks, K):
    out, n, v = [], 0, 0
    for t in toks:
        if t == '|':
            out.append('|'); continue
        n += 1
        if t in K:
            v += 1
            p, c = K[t]
            out.append(p if c == 'confirmed' else f'<{p}>')
        else:
            s = segment(t, K)
            if s:
                v += 1; out.append('{' + '+'.join(s) + '}')
            else:
                out.append('?' + t)
    return ' '.join(out), n, v


def run(show=True):
    K = load_key()
    L = letters()
    res = {}
    for rec, lines in L.items():
        N = V = 0
        if show:
            print(f'\n=== {rec}')
        for lab, s in lines:
            d, n, v = decode_line(tokens(s), K)
            N += n; V += v
            if show:
                print(f'{lab:8} {d}')
        res[rec] = (V, N)
        if show:
            print(f'coverage {V}/{N} = {100*V/max(N,1):.1f}%')
    return res


def kwic(targets, width=6):
    K = load_key(); L = letters()
    for tgt in targets:
        print(f'\n##### {tgt}')
        for rec, lines in L.items():
            flat = []
            for lab, s in lines:
                for t in tokens(s):
                    flat.append((lab, t))
            for i, (lab, t) in enumerate(flat):
                if t == tgt:
                    L_ = [decode_line([x[1]], K)[0] for x in flat[max(0, i-width):i]]
                    R_ = [decode_line([x[1]], K)[0] for x in flat[i+1:i+1+width]]
                    print(f'{rec} {lab:7} ... {" ".join(L_)}  [[{tgt}]]  {" ".join(R_)}')


def open_list(minlen=2):
    K = load_key(); L = letters(); c = collections.Counter()
    for rec, lines in L.items():
        for lab, s in lines:
            for t in tokens(s):
                if t != '|' and t not in K and not segment(t, K):
                    c[t] += 1
    for t, n in c.most_common():
        print(n, t)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--build' in a:
        build()
    elif '--kwic' in a:
        kwic(a[a.index('--kwic')+1:])
    elif '--open' in a:
        open_list()
    else:
        r = run(show='--quiet' not in a)
        print('\nSUMMARY')
        for k, (v, n) in r.items():
            print(f'{k}\t{v}/{n}\t{100*v/max(n,1):.1f}%')
