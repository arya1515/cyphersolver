"""Build the word table implied by hand-aligned group=output pairs, and decode groups with it.

Usage: python wordtable.py r2237_assign.txt            -> print the table and any conflicts
       python wordtable.py r2237_assign.txt cipher.txt -> also decode a group-transcribed ciphertext
"""
import re, sys

GROUP = re.compile(r'(?:(\d+)\))?(\d+)(_)?(?:\^(\d+))?((?:,\d+)*)$')

def parse(g):
    m = GROUP.match(g)
    if not m:
        return None
    k, n, whole, j, pos = m.groups()
    return int(n), int(k or 0), int(j or 0), bool(whole), [int(p) for p in pos.split(',')[1:]] if pos else []

def build(path):
    letters, length, conflicts = {}, {}, []
    def put(n, p, c, src):
        d = letters.setdefault(n, {})
        if d.get(p, c) != c:
            conflicts.append(f'{n}[{p}] {d[p]}/{c} ({src})')
        d.setdefault(p, c)
    for ln in open(path, encoding='utf8'):
        if ln.startswith('#'):
            continue
        for item in ln.split():
            g, _, out = item.partition('=')
            if out.endswith('?') or not out:
                continue
            n, k, j, whole, pos = parse(g)
            if pos:
                for p, c in zip(pos, out):
                    put(n, p, c, item)
            else:
                for t, c in enumerate(out):
                    put(n, k + 1 + t, c, item)
                L = k + len(out) + j
                if length.setdefault(n, L) != L:
                    conflicts.append(f'{n} len {length[n]}/{L} ({item})')
    return letters, length, conflicts

def show(n, letters, length):
    d = letters.get(n, {})
    top = length.get(n) or (max(d) if d else 0)
    return ''.join(d.get(p, '.') for p in range(1, top + 1)) + ('' if n in length else '+')

def decode_group(g, letters, length):
    r = parse(g)
    if r is None:
        return g           # clear word
    n, k, j, whole, pos = r
    d = letters.get(n, {})
    if pos:
        return ''.join(d.get(p, '.') for p in pos)
    L = length.get(n)
    if L is None:
        top = max(d) if d else 0
        s = ''.join(d.get(p, '.') for p in range(k + 1, top + 1))
        return (s or '') + '~' if j == 0 else s[:max(0, len(s))] + '~'
    return ''.join(d.get(p, '.') for p in range(k + 1, L - j + 1))

if __name__ == '__main__':
    letters, length, conflicts = build(sys.argv[1])
    if len(sys.argv) == 2:
        for n in sorted(letters):
            print(n, show(n, letters, length))
        print('conflicts:', conflicts or 'none')
    else:
        for ln in open(sys.argv[2], encoding='utf8'):
            if ln.startswith('#') or not ln.strip():
                continue
            out = [decode_group(g, letters, length) for g in ln.split()]
            print(' '.join(out))
