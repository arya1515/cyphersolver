"""Render ../CATALOGUE.md as docs/catalogue.html. Run from docs/, then run _build_site.py for nav, toc and footer.
Only the Markdown the catalogue uses is handled: paragraphs, one H1, H2 sections, pipe tables, bullet lists,
**bold**, *italic*, `code` and bare URLs/arks."""
import re, html, pathlib

HERE = pathlib.Path(__file__).parent
src = (HERE.parent / 'CATALOGUE.md').read_text(encoding='utf-8')


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)([^*]+?)\*(?!\w)', r'<i>\1</i>', t)
    t = re.sub(r'\bark (btv1b[0-9a-z]+)', lambda m: f'ark <a href="https://gallica.bnf.fr/ark:/12148/{m.group(1)}" rel="noopener">{m.group(1)}</a>', t)
    t = t.replace(' -> ', ' &rarr; ')
    return t


out, i, lines = [], 0, src.split('\n')
title = ''
while i < len(lines):
    ln = lines[i]
    if ln.startswith('# '):
        title = ln[2:].strip(); i += 1; continue
    if ln.startswith('## '):
        out.append(f'<h2>{inline(ln[3:].strip())}</h2>'); i += 1; continue
    if ln.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
        head, body = rows[0], [r for r in rows[2:]]
        out.append('<div class="tablewrap"><table class="cat">\n<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead>\n<tbody>')
        for r in body:
            cells = ''.join(f'<td>{inline(c)}</td>' for c in r)
            out.append(f'<tr>{cells}</tr>')
        out.append('</tbody></table></div>'); continue
    if ln.startswith('- '):
        items = []
        while i < len(lines) and (lines[i].startswith('- ') or (lines[i].startswith('  ') and items)):
            if lines[i].startswith('- '): items.append(lines[i][2:])
            else: items[-1] += ' ' + lines[i].strip()
            i += 1
        out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'); continue
    if ln.strip() == '':
        i += 1; continue
    para = []
    while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||- )', lines[i]):
        para.append(lines[i].strip()); i += 1
    out.append(f'<p>{inline(" ".join(para))}</p>')

body = '\n'.join(out)
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catalogue of unsolved historical ciphers — 25 new targets</title>
<meta name="description" content="Twenty-five undeciphered historical cipher letters, 1497–1610, not on the standard unsolved lists: found by harvesting the BnF catalogue on Gallica and by reading the fine print of the cryptiana articles. With shelfmarks, arks, prior art, difficulty class and what would confirm each is open.">
<link rel="stylesheet" href="style.css">
<style>
.tablewrap{{overflow-x:auto;margin:1.2rem 0}}
table.cat{{border-collapse:collapse;font-size:.86rem;min-width:900px}}
table.cat th,table.cat td{{border-bottom:1px solid var(--line,#ccc);padding:.45rem .5rem;vertical-align:top;text-align:left}}
table.cat th{{position:sticky;top:0;background:var(--bg,#fff)}}
table.cat td:nth-child(2){{white-space:nowrap}}
</style>
</head>
<body id="top">
<!-- site:nav -->

<section class="hero">
  <p class="kicker">Gallica · BnF catalogue harvest · cryptiana fine print · 1497–1610 · 25 new targets, unvalidated</p>
  <h1>{html.escape(title)}</h1>
  <p class="sub">What is still in cipher in the digitised French diplomatic volumes, and nobody has put on a list. Each row gives the shelfmark and ark, the status as the catalogue and the literature record it, why the letter matters, and a difficulty class: <b>A</b> siblings with decipherment in the same volume, <b>B</b> a partial key in print, <b>C</b> statistics only.</p>
  <p class="sub">Compiled from 331 catalogue records and six cryptiana pages, not from the leaves: rows marked ◇ have not been viewed on the image and each carries the check that would confirm it is open. Source file: <a href="https://github.com/dbourdeau/cyphersolver/blob/main/CATALOGUE.md" rel="noopener">CATALOGUE.md</a>.</p>
  <p class="meta">Daniel Bourdeau · September 2026</p>
</section>

<main>
{body}
</main>
<!-- site:footer -->
</body>
</html>
'''
(HERE / 'catalogue.html').write_text(page, encoding='utf-8')
print('wrote catalogue.html', len(page))
