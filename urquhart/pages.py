# The Jewel (Ekskybalauron, 1652) from EEBO-TCP A95749: printed pages 1-284 as word lists.
# Pages whose <pb> lacks n= are numbered by position between their neighbours.
import re, html, os
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path=os.path.join(HERE, 'src', 'tcp_A95749.xml'), keep_notes=False, numbering='physical'):
    """numbering='physical': pages counted in order from printed p. 1 (the 1652 printer repeated 34-35, 38-39,
    42-43, 46-47 and skipped 60 and 110, so printed numbers and physical order diverge between 36 and 112).
    numbering='printed': the n= of the TCP <pb>, i.e. the number printed on the page."""
    x = open(path, encoding='utf-8').read()
    body = x[x.find('<text'):]
    parts = re.split(r'(<pb [^>]*/>)', body)
    pages = {}
    phys = 0; started = False
    for i in range(1, len(parts), 2):
        tag = parts[i]; seg = parts[i + 1]
        if 'rendition="simple:additions"' in tag:
            continue
        m = re.search(r'n="(\d+)"', tag)
        if m and int(m.group(1)) == 1:
            started = True
        if not started:
            continue
        words_probe = re.findall(r"[A-Za-zÀ-ſ][A-Za-zÀ-ſ'’\-]*", html.unescape(re.sub(r'<[^>]+>', ' ', seg)))
        if len(words_probe) < 10 and m and pages and numbering == 'physical' and int(m.group(1)) < phys:
            continue      # TCP artefact: a duplicated <pb> for a re-shot image (physical 158-159, 184-185), two words each
        phys += 1
        if numbering == 'physical':
            cur = phys
        else:
            cur = int(m.group(1)) if m else None
        if cur is None:
            continue
        if not keep_notes:
            seg = re.sub(r'<note[^>]*>.*?</note>', '', seg, flags=re.S)
        seg = re.sub(r'<fw[^>]*>.*?</fw>', '', seg, flags=re.S)
        seg = re.sub(r'<g ref="char:EOLhyphen"/>', '', seg)
        seg = re.sub(r'<[^>]+>', ' ', seg)
        seg = html.unescape(seg).replace('ſ', 's')
        words = re.findall(r"[A-Za-zÀ-ſ][A-Za-zÀ-ſ'’\-]*", seg)
        pages[cur] = pages.get(cur, []) + words
    return pages


def first_index(words, letter):
    """1-based index of the first word starting with letter (case-insensitive), or None."""
    L = letter.upper()
    for i, w in enumerate(words):
        if w[0].upper() == L:
            return i + 1
    return None


if __name__ == '__main__':
    P = load()
    print('physical', min(P), max(P), len(P))
    Q = load(numbering='printed')
    print('printed', min(Q), max(Q), len(Q), [n for n in range(1, 285) if n not in Q])
    print('phys page 36 starts:', ' '.join(P[36][:8]), '| printed 34 (2nd) len', len(Q[34]))
