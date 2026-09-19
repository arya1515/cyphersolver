"""Scoreboard for index.html, computed from the result tables in ../README.md.

Run  python _build_stats.py  from docs/ (then _build_site.py as usual). Idempotent: rewrites the block between
<!-- stats:start --> and <!-- stats:end -->, inserting it after <main> the first time, and adds the jump link.

Categories are the README's own sections. Every number on the page is derived here, nothing is typed in:
  read      ### Solved                          (decipherments made or completed here)
  nothing   ### Explained                        (shown to carry no message)
  partly    ### Partly read or adjudicated
  found     ### Found already solved by others   (the lists were stale)
  closed    ### Attempted and closed             (attacked with controls; the notes say why it stops)
  offline   ### Offline only                     (nothing more can be done online)
  active    ### In progress
Overrides: rows whose target text matches OVERRIDE are moved (Forster sits in the README's Solved table but was read by others).
"""
import re, pathlib, html, datetime

HERE = pathlib.Path(__file__).parent
README = HERE.parent / 'README.md'
INDEX = HERE / 'index.html'
YEAR_NOW = datetime.date.today().year

SECTIONS = [
    ('read',    '### Solved'),
    ('nothing', '### Explained'),
    ('partly',  '### Partly read'),
    ('found',   '### Found already solved'),
    ('closed',  '### Attempted and closed'),
    ('offline', '### Offline only'),
    ('active',  '### In progress'),
]
OVERRIDE = {'Forster': 'found'}
LABEL = {
    'read': 'read', 'nothing': 'no message', 'partly': 'partly read', 'found': 'already solved elsewhere',
    'closed': 'closed, with the reason', 'offline': 'waiting on an archive', 'active': 'in progress',
}
COLOR = {  # CSS variables from style.css
    'read': 'var(--green)', 'nothing': 'var(--blue)', 'partly': 'var(--violet)', 'found': 'var(--amber)',
    'closed': 'var(--red)', 'offline': 'var(--muted)', 'active': 'var(--gold)',
}

def parse_year(s):
    s = s.strip()
    m = re.search(r'(\d{4})', s)
    if m:
        y = int(m.group(1))
        return y + 5 if re.search(r'\d{4}s', s) else y     # "c.1950s" -> 1955
    m = re.search(r'(\d{2})th c', s)
    if m:
        return (int(m.group(1)) - 1) * 100 + 50           # "17th c." -> 1650
    return None

def strip_md(s):
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'[`*]', '', s)
    return html.unescape(s).strip()

def load():
    text = README.read_text(encoding='utf-8')
    items = []
    for cat, head in SECTIONS:
        i = text.find(head)
        if i < 0:
            continue
        j = text.find('\n### ', i + 1); j = len(text) if j < 0 else j
        k = text.find('\n## ', i + 1)
        if 0 <= k < j: j = k
        for line in text[i:j].splitlines():
            if not line.startswith('| ') or line.startswith('| Target') or line.startswith('|---'):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) < 2:
                continue
            name, date = strip_md(cells[0]), cells[1]
            c = cat
            for key, dest in OVERRIDE.items():
                if key in name:
                    c = dest
            items.append(dict(name=name, date=date.strip(), year=parse_year(date), cat=c))
    return items

def timeline_svg(items):
    dated = [it for it in items if it['year']]
    x0 = min(1480, int(min(it['year'] for it in dated) // 100 * 100))  # start at the oldest item's century
    x1 = 2000
    W, H, top, lane_h, r = 1000, 150, 26, 12, 4.5
    def X(y): return 30 + (y - x0) / (x1 - x0) * (W - 60)
    # lane assignment: greedy, avoid overlap within 12 px
    lanes = []
    placed = []
    for it in sorted(dated, key=lambda d: d['year']):
        x = X(it['year'])
        for li, last in enumerate(lanes):
            if x - last >= 11:
                lanes[li] = x; placed.append((it, x, li)); break
        else:
            lanes.append(x); placed.append((it, x, len(lanes) - 1))
    nl = len(lanes)
    H = top + nl * lane_h + 30
    out = [f'<svg class="tl" viewBox="0 0 {W} {H}" role="img" aria-label="Every target placed by date and coloured by outcome" preserveAspectRatio="xMidYMid meet">']
    base = top + nl * lane_h + 4
    out.append(f'<line x1="30" y1="{base}" x2="{W-30}" y2="{base}" class="axis"/>')
    for c in range((x0 + 99) // 100 * 100, 2001, 100):
        x = X(c)
        out.append(f'<line x1="{x:.1f}" y1="{base-4}" x2="{x:.1f}" y2="{base+4}" class="axis"/>')
        out.append(f'<text x="{x:.1f}" y="{base+18}" class="tick" text-anchor="middle">{c}</text>')
    for it, x, li in placed:
        y = base - 8 - li * lane_h
        title = html.escape(f"{it['name']} ({it['date']}): {LABEL[it['cat']]}")
        out.append(f'<g class="pt {it["cat"]}"><title>{title}</title><circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{COLOR[it["cat"]]}"/></g>')
    out.append('</svg>')
    return '\n'.join(out)

def build(items):
    n = {c: sum(1 for it in items if it['cat'] == c) for c, _ in SECTIONS}
    total = len(items)
    attacked = total - n['offline']                     # everything that got a real attempt online
    decided = n['read'] + n['nothing'] + n['found']     # outcomes with a definite answer
    read = [it for it in items if it['cat'] == 'read' and it['year']]
    silence = sum(YEAR_NOW - it['year'] for it in read)
    oldest = min(read, key=lambda d: d['year'])
    span = [it['year'] for it in items if it['year']]
    pct = round(100 * n['read'] / attacked)
    order = ['read', 'nothing', 'found', 'partly', 'active', 'closed', 'offline']
    bar = ''.join(
        f'<span class="seg {c}" style="flex:{n[c]};background:{COLOR[c]}" title="{n[c]} {LABEL[c]}"></span>'
        for c in order if n[c])
    legend = ''.join(
        f'<span class="lg"><i style="background:{COLOR[c]}"></i>{n[c]} {LABEL[c]}</span>' for c in order if n[c])
    lines = []
    lines.append('<!-- stats:start -->')
    lines.append('<section class="scoreboard" id="scoreboard" aria-labelledby="sb-h">')
    lines.append('<h2 id="sb-h"><span class="num">&sum;</span> The ledger so far</h2>')
    lines.append(f'<p class="sb-lede">{total} targets taken from the three lists. {attacked} were attacked online; {n["offline"]} stop at an archive door before any cryptanalysis is possible. Every outcome is one of seven kinds, and the honest denominator for a &ldquo;success rate&rdquo; is the {attacked} attacked, not the {total}.</p>')
    lines.append(f'<div class="sb-bar" role="img" aria-label="Outcomes of {total} targets">{bar}</div>')
    lines.append(f'<div class="sb-legend">{legend}</div>')
    lines.append('<div class="sb-grid">')
    lines.append(f'<div class="sb-big"><b>{n["read"]} <small>of {attacked}</small></b><span>attacked targets read in full or in substance, {pct}&nbsp;%. One completes an alphabet another solver published (Boswell 1643); one applies a table already in print to letters never before decoded (Catinat 1691).</span></div>')
    lines.append(f'<div class="sb-big"><b>{decided}</b><span>questions settled one way or another: read, shown to carry no message, or found already solved in print, in a comment thread, or on GitHub.</span></div>')
    lines.append(f'<div class="sb-big"><b>{n["closed"]}</b><span>attacks that stop with a stated reason and a control that passed where the target failed. A negative here says something; it is not a shrug.</span></div>')
    lines.append(f'<div class="sb-big"><b>{silence:,}</b><span>years of silence ended, summed over the {len(read)} texts read: each had waited from its date until {YEAR_NOW}. The oldest is {oldest["name"].split(",")[0].split(" (")[0]} ({oldest["date"]}).</span></div>')
    lines.append('</div>')
    lines.append(f'<p class="sb-note">Every target by date, {min(span)}&ndash;{max(span)}. Hover a dot for the name and outcome.</p>')
    lines.append(timeline_svg(items))
    lines.append(f'<p class="sb-foot">Counted from the results tables in the <a href="https://github.com/dbourdeau/cyphersolver#results">repository README</a> by <code>_build_stats.py</code>; regenerated {datetime.date.today():%d %B %Y}. &ldquo;Already solved elsewhere&rdquo; and &ldquo;no message&rdquo; are not decipherments and are not counted as such. Forster (1644) is counted among those read by others. Rows are documents, not correspondents: S&eacute;gur f.&nbsp;143 and Urquhart&rsquo;s distich stand as separate open items beside the letters and the octastich that were read.</p>')
    lines.append('</section>')
    lines.append('<!-- stats:end -->')
    return '\n'.join(lines), n

def main():
    items = load()
    block, n = build(items)
    s = INDEX.read_text(encoding='utf-8')
    if '<!-- stats:start -->' in s:
        s = re.sub(r'<!-- stats:start -->.*?<!-- stats:end -->', lambda m: block, s, flags=re.S)
    else:
        s = s.replace('<main>\n', '<main>\n\n' + block + '\n\n', 1)
    if 'href="#scoreboard"' not in s:
        s = s.replace('<div class="jump"><a href="#recent">', '<div class="jump"><a href="#scoreboard">The ledger</a><a href="#recent">', 1)
    INDEX.write_text(s, encoding='utf-8')
    for c, _ in SECTIONS:
        print(f'{c:8s} {n[c]:3d}  ' + '; '.join(it['name'][:28] for it in items if it['cat'] == c))
    print('total', len(items), 'undated:', [it['name'] for it in items if not it['year']])

if __name__ == '__main__':
    main()
