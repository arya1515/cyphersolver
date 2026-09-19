"""Write-up completeness: is a finished cipher on every surface it should be on?

A finished result touches eleven places (see .claude/skills/writeup/SKILL.md). Sessions in this repository
kept skipping some of them, and concurrent sessions committed each other's folders without a write-up, so
this script checks the surfaces mechanically. It reads the working tree; it never edits anything.

Run from anywhere:

  python docs/_check_writeup.py <slug>          every surface for one write-up (slug = docs/<slug>.html)
  python docs/_check_writeup.py --audit         finished targets with no write-up, and other drift
  python docs/_check_writeup.py --hook start    SessionStart hook: short audit as context for the session
  python docs/_check_writeup.py --hook stop     Stop hook: block the stop once when a target this session
                                                worked on looks finished in its NOTES but has no write-up

Exit code 1 from <slug> or --audit when something is missing; the hook modes always exit 0.
"""
import sys, re, json, pathlib, subprocess, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = pathlib.Path(__file__).resolve().parent          # docs/
ROOT = HERE.parent
SITE = 'https://dbourdeau.github.io/cyphersolver/'
SURVEYS = {'famous', 'solved'}
NOT_TARGETS = {'docs', 'papers', 'gallica_siblings', 'gallica_sweep', 'top50', 'oldest', 'source_headings.txt'}

def read(p):
    try: return pathlib.Path(p).read_text(encoding='utf-8')
    except (FileNotFoundError, UnicodeDecodeError): return ''

# ---------------------------------------------------------------------------
# the surfaces

def manifest():
    """slug -> st for every PAGES entry, and the IMAGES keys, from _build_site.py (no import: it has side effects)."""
    s = read(HERE / '_build_site.py')
    pages = {m.group(1): m.group(2) for m in re.finditer(r"dict\(slug='([a-z0-9]+)'.*?st='([a-z]+)'", s)}
    im = re.search(r'^IMAGES = \{(.*)\}\s*$', s, re.M)
    images = {}
    if im:
        for m in re.finditer(r"'([a-z0-9]+)': (\(|None)", im.group(1)): images[m.group(1)] = m.group(2) == '('
    version = re.search(r"^VERSION = '([^']+)'", s, re.M)
    return pages, images, version.group(1) if version else ''

def dates():
    try: return json.loads(read(HERE / '_dates.json')).get('pages', {})
    except json.JSONDecodeError: return {}

def readme_rows():
    """Rows of README's Results tables: section, target cell, where cell, linked slugs, linked repo dirs."""
    rows, sect = [], None
    for line in read(ROOT / 'README.md').splitlines():
        if line.startswith('## '): sect = None
        if line.startswith('### '): sect = line[4:].strip(); continue
        if not sect or not line.startswith('| ') or line.startswith('| Target') or line.startswith('|---'): continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 4: continue
        where = cells[-1]
        rows.append(dict(section=sect, target=cells[0], where=where, line=line,
                         slugs=set(re.findall(r'cyphersolver/([a-z0-9]+)\.html', where)),
                         dirs=set(re.findall(r'\]\(([a-z0-9_]+)/\)', where))))
    return rows

def catalogue():
    try:
        d = json.loads(read(ROOT / 'catalogue.json'))
        return d if isinstance(d, list) else d.get('entries', [])
    except json.JSONDecodeError: return []

FINISHED = re.compile(r'status:\s*\**\s*(solved|read|broken|resolved|done)\b|\bread in (full|part|substance)\b|'
                      r'\bletter is read\b|\bcipher is broken\b|\bkey (is )?recovered\b|\bdeciphered in full\b|'
                      r'\bsolved \(\d|\bsolved \d{1,2} [A-Z][a-z]+ \d{4}', re.I)
NOT_FINISHED = re.compile(r'status:\s*\**\s*(in progress|open|unsolved|attempted|stuck|blocked|no write-?up)', re.I)

def target_dirs():
    """Root folders with a NOTES.md, and whether the head of the notes reads as finished."""
    out = {}
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name in NOT_TARGETS or d.name.startswith('.'): continue
        notes = d / 'NOTES.md'
        if not notes.exists(): continue
        head = '\n'.join(read(notes).splitlines()[:40])
        m = FINISHED.search(head)
        out[d.name] = dict(finished=bool(m) and not NOT_FINISHED.search(head),
                           why=(m.group(0).strip() if m else ''), mtime=notes.stat().st_mtime)
    return out

def git(*args):
    try: return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20).stdout
    except (OSError, subprocess.TimeoutExpired): return ''

def page_on_main(slug):
    """Does docs/<slug>.html exist on origin/main or main? (Cheap: git cat-file -e, no checkout.)"""
    for ref in ('origin/main', 'main'):
        try:
            r = subprocess.run(['git', 'cat-file', '-e', f'{ref}:docs/{slug}.html'], cwd=ROOT, capture_output=True, timeout=20)
            if r.returncode == 0: return True
        except (OSError, subprocess.TimeoutExpired): pass
    return False

def key_words(target_cell):
    """The name to look for in the ranking and catalogue tables: the README target cell up to the first comma."""
    t = re.sub(r'[*`\[\]]', '', target_cell).split(',')[0].split(' → ')[0].strip()
    return t[:40]

# ---------------------------------------------------------------------------
# one write-up

def check_slug(slug):
    pages, images, version = manifest()
    rows = readme_rows()
    ok = True
    def item(good, text, warn=False):
        nonlocal ok
        mark = 'ok  ' if good else ('warn' if warn else 'MISS')
        if not good and not warn: ok = False
        print(f'  [{mark}] {text}')

    page_path = HERE / f'{slug}.html'
    page = read(page_path)
    print(f'{slug}: write-up surfaces')
    item(bool(page), f'docs/{slug}.html exists')
    if page:
        item('<section class="hero">' in page, 'page has a <section class="hero"> (kicker, h1, sub, meta)')
        item('<p class="meta">' in page, 'hero has the <p class="meta"> byline the builder stamps')
        item(bool(re.search(r'<title>.+</title>', page)) and 'name="description"' in page, 'title and meta description')
        item(bool(re.search(r'<h2[^>]*>.*?Sources', page, re.S)), 'a Sources section', warn=True)
        item(bool(re.search(r'\bclass="callout"', page)), 'a summary callout at the top of <main>', warn=True)
        for img in set(re.findall(r'<img[^>]+src="([^"]+)"', page)):
            item((HERE / img).exists(), f'figure file docs/{img} exists')
        item(f'?v={version}' in page if version else True, 'page carries the current stylesheet version (else rebuild)', warn=True)
        item(bool(git('ls-files', f'docs/{slug}.html').strip()), 'page is tracked by git', warn=True)
    st = pages.get(slug)
    item(st is not None, f'PAGES entry in docs/_build_site.py (st={st})')
    item(slug in images, 'IMAGES entry in docs/_build_site.py (None is allowed, a lead figure is better)')
    item(slug in dates(), 'docs/_dates.json has the page (created by the first build)')
    mine = [r for r in rows if slug in r['slugs']]
    item(bool(mine), f'README.md results row links {SITE}{slug}.html')
    index = read(HERE / 'index.html')
    reg = re.search(r'<h2 id="recent">.*?(?=\n<h2|\n<!-- |\Z)', index, re.S)
    item(bool(reg) and f'href="{slug}.html"' in reg.group(0), 'index.html Recent findings has a <li> linking the page')
    # solved.html is unpublished (kept in unpublished/); a row there is optional until it goes back into docs/
    live = (HERE / 'solved.html').exists()
    solved = read(HERE / 'solved.html') if live else read(ROOT / 'unpublished' / 'solved.html')
    need_solved = live and st in ('solved', 'partial')
    item(f'href="{slug}.html"' in solved, ('' if live else 'unpublished/') + 'solved.html row (solved/partly read; then recount its short version)',
         warn=not need_solved)
    wu = read(HERE / 'writeups.html')
    if wu: item(f'href="{slug}.html"' in wu, 'writeups.html lists the page (regenerated by the build)', warn=True)
    cat = [e for e in catalogue() if (e.get('writeup') or '') == f'{slug}.html']
    item(bool(cat), 'catalogue.json entry has "writeup" (only if the target is a catalogue item)', warn=True)
    if cat:
        cmd = read(ROOT / 'CATALOGUE.md')
        item(f'{slug}.html' in cmd or str(cat[0].get('id')) in cmd, 'CATALOGUE.md regenerated after the json edit (_catalogue_page.py)', warn=True)
    if mine:
        name = key_words(mine[0]['target'])
        for f in ('SOLVED_CATALOGUE.md', 'SOLVED_RANKING.md', 'TARGETS.md'):
            item(name.lower() in read(ROOT / f).lower(), f'{f} mentions "{name}" (checked by name, confirm the row by eye)',
                 warn=(f == 'TARGETS.md'))
    print('  result:', 'complete' if ok else 'INCOMPLETE - see MISS lines')
    return ok

# ---------------------------------------------------------------------------
# the audit

def audit(brief=False):
    pages, images, _ = manifest()
    rows = readme_rows()
    dirs = target_dirs()
    listed_dirs = set().union(*(r['dirs'] for r in rows)) if rows else set()
    listed_slugs = set().union(*(r['slugs'] for r in rows)) if rows else set()
    html_slugs = {p.stem for p in HERE.glob('*.html')} - {'index', 'catalogue', 'writeups'}
    problems = 0

    # 1. finished in the notes, nowhere else. The shared checkout is often on a stale branch, so a page that
    #    exists on main counts as written up and is only mentioned.
    gaps, on_main = [], []
    for d, info in dirs.items():
        if not info['finished']: continue
        if d in listed_dirs or d in pages or d in html_slugs: continue
        if page_on_main(d): on_main.append(d)
        else: gaps.append((d, info['why']))
    print(f'A. Finished in NOTES.md, no README row and no site page: {len(gaps)}')
    for d, why in gaps: print(f'   {d}/   (notes say: "{why}")')
    if on_main: print(f'   (written up on main, not in this checkout: {", ".join(on_main)})')
    problems += len(gaps)

    # 2. README rows with a repo link but no write-up page
    notes_only = [r for r in rows if not r['slugs'] and r['dirs']
                  and r['section'].split(' ')[0] in ('Solved', 'Explained:', 'Partly', 'Found')]
    print(f'B. README results rows with no write-up page (notes only): {len(notes_only)}')
    if not brief:
        for r in notes_only: print(f'   [{r["section"][:22]}] {key_words(r["target"])}  ->  {", ".join(sorted(r["dirs"]))}/')

    # 3. catalogue.json outcomes with no write-up link
    cat = [e for e in catalogue() if e.get('outcome') and not e.get('writeup')]
    print(f'C. catalogue.json entries with an outcome but no "writeup": {len(cat)}')
    for e in cat: print(f'   #{e.get("id")} {str(e.get("title", ""))[:60]}  (outcome: {e.get("outcome")})')
    problems += len(cat)

    # 4. site pages / README / manifest drift
    drift = []
    for s in sorted(set(pages) - SURVEYS - listed_slugs): drift.append(f'docs/{s}.html is in the manifest but README has no row linking it')
    for s in sorted(html_slugs - set(pages) - SURVEYS): drift.append(f'docs/{s}.html exists but has no PAGES entry in _build_site.py')
    for s in sorted(listed_slugs - html_slugs): drift.append(f'README links {s}.html, which does not exist in docs/')
    for s in sorted(set(pages) - set(images) - SURVEYS): drift.append(f'{s} has no IMAGES entry (add one, or None)')
    print(f'D. Manifest / README / docs drift: {len(drift)}')
    for x in drift: print('   ' + x)
    problems += len(drift)
    return problems, gaps

# ---------------------------------------------------------------------------
# hooks

def hook_start():
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): problems, gaps = audit(brief=True)
    if not problems:
        print(json.dumps({'suppressOutput': True})); return
    text = ('Write-up audit (docs/_check_writeup.py --audit). A finished cipher is not done until it is written up: '
            'run the /writeup skill for it.\n' + buf.getvalue())
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': text}}))

def hook_stop():
    try: inp = json.loads(sys.stdin.read() or '{}')
    except json.JSONDecodeError: inp = {}
    if inp.get('stop_hook_active'):                     # we already blocked once this stop; never loop
        print(json.dumps({'suppressOutput': True})); return
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()): _, gaps = audit(brief=True)
    if not gaps:
        print(json.dumps({'suppressOutput': True})); return
    # only targets this session worked in: a tool call whose input names a path in the folder (a folder merely
    # mentioned in prose, or in this script's own audit output, does not count); without a transcript, fall
    # back to uncommitted changes in the folder or notes edited in the last 6 h
    tpath = inp.get('transcript_path') or ''
    tpath = re.sub(r'^/([a-zA-Z])/', lambda m: m.group(1).upper() + ':/', tpath)     # Git Bash spelling on Windows
    transcript = read(tpath) if tpath else ''
    tool_lines = [l for l in transcript.splitlines() if '"type":"tool_use"' in l or '"type": "tool_use"' in l]
    status = git('status', '--porcelain')
    dirs = target_dirs()
    mine = []
    for d, why in gaps:
        if transcript: touched = any(re.search(rf'"input":.*\b{re.escape(d)}[/\\]', l) for l in tool_lines)
        else: touched = f' {d}/' in status or time.time() - dirs[d]['mtime'] < 6 * 3600
        if touched: mine.append((d, why))
    if not mine:
        print(json.dumps({'suppressOutput': True})); return
    names = ', '.join(d for d, _ in mine)
    reason = (f'Write-up check: {names} reads as finished in NOTES.md ("{mine[0][1]}") but has no README results row '
              f'and no site page. Before stopping, either run the /writeup skill for it now (every surface, then '
              f'`python docs/_check_writeup.py {mine[0][0]}` must print "complete"), or, if it is not finished, put '
              f'"Status: in progress" at the top of {mine[0][0]}/NOTES.md so the check stops asking.')
    print(json.dumps({'decision': 'block', 'reason': reason}))

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        if args[:1] == ['--hook']:
            (hook_stop if args[1:2] == ['stop'] else hook_start)()
        elif args[:1] == ['--audit']:
            problems, _ = audit()
            sys.exit(1 if problems else 0)
        elif len(args) == 1 and re.fullmatch(r'[a-z0-9]+', args[0]):
            sys.exit(0 if check_slug(args[0]) else 1)
        else:
            print(__doc__); sys.exit(2)
    except SystemExit: raise
    except Exception as e:                              # a hook must never break the session
        if args[:1] == ['--hook']: print(json.dumps({'suppressOutput': True, 'systemMessage': f'_check_writeup.py: {e!r}'}))
        else: raise
