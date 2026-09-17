"""One-off, 2026-09-17: remove list entries that were found solved by others with nothing added here
(Perwich 1670, Ferdinand III 1634-40, Milroy 1861-62, Feynman 2 and 3, Confederate dictionary code, Mazarin-Bordeaux 1654)
from README.md, TARGETS.md, SOLVED_RANKING.md, docs/index.html and docs/_build_queue.py. Directories are kept.
Run from docs/. Prints every line removed so the change can be audited.
"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent

def edit(path, fn):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    t = fn(s)
    if t != s:
        p.write_text(t, encoding='utf-8')
    print(f'-- {path}: {len(s.splitlines()) - len(t.splitlines())} lines removed')

def drop_lines(s, prefixes):
    out = []
    for line in s.split('\n'):
        if any(line.startswith(p) for p in prefixes):
            print('   -', line[:110])
            continue
        out.append(line)
    return '\n'.join(out)

NOTE = ('Six further list entries turned out to be solved by others with nothing to add here: Perwich 1670 (Brown; Lasry, '
        'Biermann and Tomokiyo, 2025), Ferdinand III and the Cardinal-Infante (Ernst, 2017), the Milroy telegrams (Bean, 2026), '
        'the Feynman ciphers 2 and 3 (2023), the Confederate Navy dictionary code (2026) and the Mazarin–Bordeaux letter of 1654 '
        '(Lasry, 2025). They are not counted in the results above; the directories `perwich/`, `ferdinand3/`, `milroy/`, `feynman/` '
        'and `barney/` hold only the pointer to the published solution.')

def readme(s):
    s = drop_lines(s, ['| Perwich → Arlington', '| Ferdinand III ↔', '| Milroy telegrams', '| Feynman ciphers', '| Confederate Navy dictionary code'])
    # add the note after the found table (before the next ### heading)
    i = s.find('### Found already solved')
    j = s.find('\n### ', i + 1)
    block = s[i:j].rstrip('\n')
    s = s[:i] + block + '\n\n' + NOTE + '\n' + s[j:]
    return s

def targets(s):
    s = drop_lines(s, ['| 16 | Ferdinand III ↔', '| 27 | Mazarin → Bordeaux', '| ~~William Perwich~~', '| A Dictionary Code Used by Confederate Navy'])
    s = re.sub(r'\nThe source has caught up on one item since our ranking: \*\*Union Ciphers during the Civil War \(1862\)\*\* is now marked\nSolved \(Richard Bean with Claude Opus 5, 2026\), matching our `milroy/` finding\.\n', '\n', s)
    s = s.replace('Already closed from that list: Feynman ciphers 2 and 3 (Vierra 2023, verified here), Zodiac Z408/Z340,',
                  'Already closed from that list: Zodiac Z408/Z340,')
    return s

def ranking(s):
    s = drop_lines(s, ['2. **Perwich → Arlington 1670.**', '3. **Feynman ciphers 2 and 3.**', '4. **Ferdinand III ↔ Cardinal-Infante.**', '5. **Milroy telegrams; Confederate Navy dictionary code.**'])
    s = s.replace('   method reimplemented and re-deriving seven pages blind; the ten open messages shown to be garbles.\n',
                  '   method reimplemented and re-deriving seven pages blind; the ten open messages shown to be garbles.\n\n'
                  'Perwich, the Feynman ciphers, Ferdinand III, Milroy, the Confederate dictionary code and Mazarin–Bordeaux 1654 were found\n'
                  'solved by others with nothing added here and are no longer listed (removed 17 September 2026).\n', 1)
    return s

def index(s):
    s = drop_lines(s, ['<li><b>Ferdinand III, 1634&ndash;40</b>', '<li><b>Perwich to Arlington, 1670</b>',
                       '<tr class="done"><td>Ferdinand III and the Cardinal-Infante</td>',
                       '<tr class="done"><td>Union cipher telegrams to General Milroy</td>',
                       '<tr class="done"><td>Confederate Navy dictionary code</td>',
                       '<tr class="done"><td>Feynman ciphers 2 and 3</td>'])
    # rows whose first cell is a link: Perwich (TNA blog) and Mazarin (bordeaux notes)
    out = []
    for line in s.split('\n'):
        if line.startswith('<tr class="done"><td><a href="https://www.nationalarchives.gov.uk/explore-the-collection/the-collection-blog/secret-diplomatic-message') \
           or (line.startswith('<tr class="done"><td><a href="https://github.com/dbourdeau/cyphersolver/blob/main/bordeaux/NOTES.md">Mazarin')):
            print('   -', line[:110]); continue
        out.append(line)
    return '\n'.join(out)

def queue(s):
    i = s.find('    ("William Perwich to Lord Arlington"')
    j = s.find('Only the nomenclator numbers remain."),\n', i) + len('Only the nomenclator numbers remain."),\n')
    assert i > 0 and j > i
    print('   -', s[i:j].splitlines()[0])
    return s[:i] + s[j:].lstrip('\n')

edit('README.md', readme)
edit('TARGETS.md', targets)
edit('SOLVED_RANKING.md', ranking)
edit('docs/index.html', index)
edit('docs/_build_queue.py', queue)
