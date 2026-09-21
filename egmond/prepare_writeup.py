"""Prepare the Egmond edition and its site/ledger entries (run once per checkout)."""
import copy
import html
import json
import re
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'egmond'
DOCS = ROOT / 'docs'
IMAGES = Path(sys.argv[1])

def read(p):
    return p.read_text(encoding='utf-8')

def write(p, s):
    p.write_text(s, encoding='utf-8')

def crop(name, source, box=None):
    im = Image.open(IMAGES / source)
    if box:
        im = im.crop(box)
    im.thumbnail((1100, 1600))
    out = DOCS / f'egmond_{name}.jpg'
    im.convert('RGB').save(out, quality=88, optimize=True)
    assert out.stat().st_size < 400_000, out

crop('lead', 'address_full.png')
crop('body', 'f27_hi.jpg', (670, 475, 2780, 1920))
crop('insertion', 'insertion_native.png')
crop('date', 'date_native.png')
crop('cross', 'cross_line4.png')

address = json.loads(read(R / 'address_audited.json'))
write(R / 'address_complete_tokens.txt', ' '.join(t for l in address['lines'] for t in l) + '\n')
body_count = len(read(R / 'body_complete_tokens.txt').split())
address_count = sum(map(len, address['lines']))
assert body_count == 726 and address_count == 48

p = R / 'profile.json'
d = json.loads(read(p))
body = d['documents'][0]
body['id'] = 'letter-body'
body['length'] = dict(tokens=body_count, unit='symbols', measured=True, file='body_complete_tokens.txt')
body['transcription']['notes'] = 'Sixteen lines and two insertions; 726 labelled signs. Variants retained; blotted date u and left-bar x are marked M. No independent key or clear copy.'
addr = copy.deepcopy(body)
addr['id'] = 'ciphered-address'
addr['length'] = dict(tokens=address_count, unit='symbols', measured=True, file='address_complete_tokens.txt')
addr['transcription']['notes'] = 'Three lines, 48 compound signs/nulls; address_audited.json records shapes and values. No personal name in the address.'
addr['cleartext_in_document'] = 'none'
d['documents'] = [body, addr]
d['system']['types'] = ['monoalphabetic']
d['system']['summary'] = 'Graphic letter substitution with nulls, paired-stroke compound letters and u/v shared; inferred from the letter and its address.'
d['conditions']['attack'] = 'ciphertext-only'
d['conditions']['inputs'] = ['images', 'cleartext context']
d['conditions']['models'] = ['GPT-6 (Codex; exact runtime identifier unavailable)']
d['conditions']['last_date'] = '2026-09-20'
d['outcome']['class'] = 'read'
d['outcome']['fraction_read'] = 1.0
d['outcome']['notes'] = 'Every transcribed sign has a proposed letter or null value; this is coverage, not 100% confidence. Left-bar x and blotted date u remain M; anomalous literal spellings retained. Internal body/address consistency only, no independent key or clear copy.'
d['solution'].append(dict(date='2026-09-20', kind='verification', result='worked', what='Native-image review distinguishes the left-extending bar in lextreme from plain plus/g. It still has only one occurrence, so x remains M. Native crops confirm the anomalous literal forms; no silent emendation. All main lines, both insertions, address and clear closing accounted for.'))
write(p, json.dumps(d, ensure_ascii=False, indent=2) + '\n')

p = R / 'READING.md'
s = read(p).replace('Status: in progress — full candidate reading; final consistency review and site write-up pending.', 'Status: read, with minor glyph uncertainties and literal anomalies retained.')
s = s.replace('context; its visual distinction from plain plus/g needs a final inventory check.', 'context. Native-image review shows its bar extending left from the upright, unlike the plain plus/g; the value still rests on one occurrence and remains M.')
s = s.replace('Re-inspection is\n  required before choosing between those explanations.', 'Native-resolution re-inspection retains these shapes; it does not establish which of those explanations is responsible.')
write(p, s)
p = R / 'NOTES.md'
s = read(p).replace('Status: in progress', 'Status: read, with minor uncertainties retained', 1)
s += '''

## Final reading and publication review

The body (16 main lines plus two insertions), address (three lines), clear closing
and signature are all accounted for. Native-resolution crops were inspected for
the anomalous forms. The cross in lextreme has a bar extending left from the stem,
distinct from the plain cross used for g; x still has only one occurrence and is
graded M. The blotted date u remains M. These are disclosed local uncertainties,
not unresolved passages. No independent clear copy or key has been found; no
claim of 100% letter accuracy or proven priority is made.

The corrected body has 726 labelled signs and the address 48, measured from the
replay files. The 27 body label names include u variants and a special label for
the blotted u; they are not a claim of 27 distinct historical glyphs. The original
catalogue's 1520s attribution is not substantiated by the recovered date. The
reading gives Arnhem, apparently 18 July, without a year. Recipient and ambassador
are identified only by the titles actually in the cipher.
'''
write(p, s)

lines = json.loads(read(R / 'diplomatic_lines.json'))
rows = '\n'.join(f'<tr><th scope="row">{n:02}</th><td>{html.escape(line)}</td></tr>' for n, line in enumerate(lines, 1))
english = read(R / 'READING.md').split('## Meaning in modern English\n\n')[1].split('\n\nThis translates')[0]
key = json.loads(read(R / 'audited_key.json'))['tokens']
key_rows = ''.join(f'<tr><td><code>{html.escape(t)}</code></td><td>{html.escape(v) if v else "null"}</td></tr>' for t, v in key.items())
page = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Charles of Egmond to the grand master of France — Read</title>
<meta name="description" content="BnF français 3015 no. 8: Charles of Egmond’s ciphered letter and address read as French. Arnhem, apparently 18 July, year unknown. Inferred key, full transcription and residual uncertainties.">
<link rel="stylesheet" href="style.css"></head><body>
<!-- site:nav -->
<section class="hero">
<p class="kicker">Arnhem → grand master of France · graphic substitution with nulls · year unknown · read</p>
<h1>Charles of Egmond: a request for support in war</h1>
<p class="sub">BnF français 3015 no. 8, folio 16: sixteen lines of cipher, two raised insertions and a ciphered address. The text is French. It asks the grand master of France to continue supporting Charles’s affairs and to assist his ambassador, the commander of Saint John.</p>
<p class="sub">The date reads “dih[u]itieme de iuillet”: apparently 18 July, with one ink-heavy sign. The year and the recipient’s personal name are not supplied.</p>
<p class="meta">Daniel Bourdeau</p></section>
<main><div class="callout"><strong>Summary.</strong> The catalogue described an entirely ciphered letter by Charles, duke of Guelders, with its address also in cipher. An inferred substitution key now reads the body and address throughout, with minor glyph uncertainties retained. The address is “A mon bon cousin / Monsieur le grant maistre / de France”. Charles says that obeying the king’s commands caused him to enter the war, and asks for continuing support in his present necessity. His ambassador is described as the commander of Saint John. Both raised insertions are read. The place is Arnhem and the apparent date 18 July; no year has been recovered. This is an internal decipherment from the images, not a reading confirmed by an archived key or a matching clear copy.</div>
<h2 id="source"><span class="num">01</span> The manuscript</h2>
<p>The BnF catalogue places item 8 at folio 16. Gallica view 27 contains the body; view 28 contains the address. The clear closing and signature identify Charles. The separate letter at folio 24, views 39–40, is dated 3 April 1537 and also addresses the grand master, but is not a clear copy of this cipher. Its year cannot be transferred to this letter.</p>
<figure><img src="egmond_body.jpg" alt="Sixteen lines of Egmond’s cipher with insertions above lines seven and fifteen" loading="lazy"><figcaption>The complete cipher block, Gallica view 27. The full page also has a clear closing and CHARLES signature. BnF / Gallica.</figcaption></figure>
<h2 id="reading"><span class="num">02</span> The French reading</h2>
<p>Spaces and capitals are editorial; u/v are left as u in the cipher transcription. Braces mark raised insertions. Square brackets mark the blotted sign interpreted as u. All values are inferred (<strong>I</strong>), with the doubts below graded <strong>M</strong>. Unusual spellings and the repeated “en ce / ce faisant” are preserved.</p>
<table><thead><tr><th>Line</th><th>Literal working reading</th></tr></thead><tbody>ROWS</tbody></table>
<p>Clear closing, abbreviation expanded: <em>Le tout v[ost]re bon cousin</em>. Signature: <strong>CHARLES</strong>.</p>
<p><strong>Address:</strong> <em>A mon bon cousin / Monsieur le grant maistre / de France.</em></p>
<figure><img src="egmond_lead.jpg" alt="Three-line ciphered address to the grand master of France" loading="lazy"><figcaption>The address, Gallica view 28: A mon bon cousin / Monsieur le grant maistre / de France. Initial and final nulls carry no words.</figcaption></figure>
<h2 id="meaning"><span class="num">03</span> Meaning in English</h2>
<blockquote><p>ENGLISH</p></blockquote>
<p>This translates the apparent sense, not every literal anomaly. “Certain” interprets the unexpanded <em>aulc</em>; “eighteenth” interprets <em>dih[u]itieme</em>. The cipher gives titles, not the personal names of the recipient or ambassador.</p>
<h2 id="method"><span class="num">04</span> How it was read</h2>
<p>Short French, German and Italian substitution probes on rough transcriptions did not yield a reliable reading. Extending the transcript to all sixteen lines gave French fragments under a five-gram model. Image comparison then corrected compound signs and nulls: the paired looped stems labelled DD give s, and the paired arches CE give r. Tall looped f forms, small circles and several other shapes are nulls. Early drafts had confused m/n zigzags, seven/b with corner/f, and angular u with a plain cross/g.</p>
<p>The address and body share letter values and null behaviour. Their coherent readings cross-check the interpretation, but are not independent known plaintext. A synthetic 180-letter French substitution control was recovered exactly by the probe; it checks the solver implementation, not this historical reading. No matching prior decipherment or archived key was found in the searches recorded in the notes. That is not proof that no earlier reading exists.</p>
<p>The final body transcript contains <strong>726 labelled signs</strong>, including both insertions; the address has <strong>48</strong>. The body uses 27 label names, including variants of u and a special label for the blotted occurrence. This is a transcription inventory, not 27 proven distinct historical characters.</p>
<details><summary>Replay labels and inferred values</summary><p>These labels are research identifiers, not facsimile glyphs. Shape descriptions and occurrence corrections are in the repository.</p><table><thead><tr><th>Label</th><th>Value</th></tr></thead><tbody>KEYROWS</tbody></table></details>
<p><code>python egmond/decode_audited.py</code> replays every main-line token and both insertions, checks their anchors and checks that the word-divided edition contains exactly the replayed letters. This guards transcription-to-edition fidelity; it is not independent proof of the inferred key.</p>
<figure><img src="egmond_insertion.jpg" alt="Raised cipher insertion read as entenderes" loading="lazy"><figcaption>“Entenderes”, inserted after “amplement” in line 7. The small e after t overlaps a descender from the preceding line.</figcaption></figure>
<h2 id="limits"><span class="num">05</span> Uncertainties and limits</h2>
<ul><li><strong>M, line 4:</strong> x in <em>lextreme</em> is assigned to a small sign with its bar extending left from the upright. Native-image inspection distinguishes it from the plain cross/g, but its value is supported by one occurrence and context.</li>
<li><strong>M, line 15:</strong> the u in <em>dih[u]itieme</em> is ink-heavy. The reading points to 18 July; no year is present. The catalogue’s tentative 1520s label is not established by this decipherment.</li>
<li><strong>M, insertion 7:</strong> the small e after t overlaps another line’s descender.</li>
<li><strong>I/M:</strong> several m/n zigzags are distinguished partly by context. All main lines were inspected, but this remains an inferred key without an independent historical control.</li>
<li>The literal forms <em>sueis, uouellu, cosidere, auir, aulc</em> and the repetition <em>en ce / ce faisant</em> survive native-resolution re-inspection. They may reflect spelling, abbreviation, enciphering slips or residual transcription error. The edition does not choose silently between those possibilities.</li>
<li>No personal names are substituted for “grand master of France” or “commander of Saint John”. A complete year, the precise campaign and priority over any unpublished decipherment remain unestablished.</li></ul>
<figure><img src="egmond_cross.jpg" alt="Small left-bar sign before t in lextreme" loading="lazy"><figcaption>The left-bar sign read x, followed by the taller two-bar t sign, a null circle and paired arches r.</figcaption></figure>
<figure><img src="egmond_date.jpg" alt="Ink-heavy sign in dihuitieme and the following date letters" loading="lazy"><figcaption>The date detail: h, the ink-heavy [u], i, t, i, e, m, e, followed by de. The preceding letters di are partly outside this crop.</figcaption></figure>
<h2 id="sources"><span class="num">06</span> Sources</h2>
<ul><li><a href="https://archivesetmanuscrits.bnf.fr/ark:/12148/cc49473n">BnF, Français 3015 catalogue</a>, item 8, folio 16; component FRBNFEAD000049473_d0e176.</li>
<li><a href="https://gallica.bnf.fr/ark:/12148/btv1b9060086g/f27.item">Gallica view 27: letter</a>; <a href="https://gallica.bnf.fr/ark:/12148/btv1b9060086g/f28.item">view 28: ciphered address</a>. Native body image: 4351 × 6122 pixels.</li>
<li><a href="https://gallica.bnf.fr/ark:/12148/btv1b9060086g/f39.item">Views 39–40: separate clear letter, 3 April 1537</a>, used for context only.</li></ul>
<p class="muted">Transcriptions, inferred key, failed probes, audit trail and replay script: <a href="https://github.com/dbourdeau/cyphersolver/tree/main/egmond">egmond/ in the repository</a>. Manuscript crops: Bibliothèque nationale de France / Gallica.</p>
</main>
<!-- site:footer -->
</body></html>
'''.replace('KEYROWS', key_rows).replace('ROWS', rows).replace('ENGLISH', html.escape(english))
write(DOCS / 'egmond.html', page)

p = DOCS / '_build_site.py'
s = read(p)
entry = '''dict(slug='egmond', label='Charles of Egmond', year='18 July (?) · year unknown', y=1525, place='Arnhem &rarr; grand master of France', st='solved', stt='read; minor uncertainties',
         title='Charles of Egmond &mdash; a ciphered request for support in war',
         blurb='The French body and ciphered address read with an inferred graphic substitution key and nulls. Charles asks the grand master to support his affairs and assist the commander of Saint John. Arnhem, apparently 18 July; year unknown. Minor glyph uncertainties and literal anomalies remain explicit.',
         quote='lequel est cause que suis entre en ceste guerre', rights='Biblioth&egrave;que nationale de France / Gallica'),
    '''
assert "slug='egmond'" not in s
s = s.replace("dict(slug='gramont1529'", entry + "dict(slug='gramont1529'", 1)
s = s.replace('IMAGES = {', "IMAGES = {'egmond': ('egmond_lead.jpg', 'The ciphered address: A mon bon cousin / Monsieur le grant maistre / de France', 'Biblioth&egrave;que nationale de France / Gallica'), ", 1)
write(p, s)

p = ROOT / 'README.md'; s = read(p)
row = '| Charles of Egmond → grand master of France, Arnhem, BnF fr. 3015 no. 8, fol. 16 (catalogue 28, class C) | 18 July (?), year unknown | 20 Sept 2026 | **Read, with minor uncertainties.** Sixteen cipher lines, two insertions and the address recovered as French with an inferred substitution key and nulls. Requests support after entering war on the king’s commands and assistance for the commander of Saint John. Date sign and a few literal anomalies retained; no independent key or clear-copy control, no personal recipient name or year established | [`egmond/`](egmond/) · [write-up](https://dbourdeau.github.io/cyphersolver/egmond.html) |\n'
anchor = '|---|---|---|---|---|\n'; idx = s.index(anchor, s.index('### Solved')) + len(anchor)
write(p, s[:idx] + row + s[idx:])

p = ROOT / 'SOLVED_CATALOGUE.md';s = read(p)
num = max(map(int, re.findall(r'^\| (\d+) \|', s, re.M))) + 1
row = f'| {num} | **Charles of Egmond → grand master of France**, BnF fr. 3015 no. 8, fol. 16 | 18 July (?), year unknown | 20 Sept 2026 | Graphic substitution and nulls inferred from full-body language-model probes, corrected against images; body, two insertions and address read with minor doubts | Transcribed the images, tested failed segmentations and languages, identified nulls and compound signs, replayed the full reading; internal consistency only, no independent clear copy. [Write-up](https://dbourdeau.github.io/cyphersolver/egmond.html)* |\n'
anchor = '|---|---|---|---|---|---|\n';idx=s.index(anchor)+len(anchor);write(p,s[:idx]+row+s[idx:])

p = ROOT / 'SOLVED_RANKING.md';s=read(p)
n=max(map(int,re.findall(r'^\| p(\d+) \|',s,re.M)))+1
addition=f'''### Provisional addition, 20 September 2026: Egmond

Charles of Egmond (p{n}, 3.10) sits beside Armstrong in this provisional scoring; no claim of an independently confirmed first reading is made.

| # | Target | Date | D | H | N | R | F | V | Score | Why it sits here (provisional) |
|---|---|---|---|---|---|---|---|---|---|---|
| p{n} | **Charles of Egmond → grand master of France**, BnF fr. 3015 no. 8 | 18 July (?), year unknown | 4 | 3 | 3 | 3 | 2 | 3 | **3.10** | Ciphertext-only graphic substitution with nulls, recovered from images after failed short probes. Full letter and address read with minor doubts. A request for support in war, without campaign year or personal names. Novelty unproven; verification is internal. |

'''
s=s.replace('## By single axis',addition+'## By single axis',1)
s+='\nEgmond provisional score: 0.25×4 + 0.25×3 + 0.20×3 + 0.10×3 + 0.10×2 + 0.10×3 = **3.15**.\n'
# Keep the displayed score equal to the documented weighted sum.
s=s.replace(f'(p{n}, 3.10)',f'(p{n}, 3.15)').replace(f'| p{n} | **Charles of Egmond',f'| p{n} | **Charles of Egmond')
s=s.replace('| 4 | 3 | 3 | 3 | 2 | 3 | **3.10** | Ciphertext-only', '| 4 | 3 | 3 | 3 | 2 | 3 | **3.15** | Ciphertext-only')
s=s.replace('sits beside Armstrong in this provisional scoring', 'sits just above Armstrong in this provisional scoring')
write(p,s)

p=ROOT/'TARGETS.md';s=read(p);anchor='## Done elsewhere in this repo\n';write(p,s.replace(anchor,anchor+'\n- **Charles of Egmond → grand master of France**, catalogue 28, BnF fr. 3015 no. 8 — body, both insertions and address read, 20 Sept 2026; Arnhem, apparently 18 July, no year. Minor glyph uncertainties retained; no independent key or clear copy. [Write-up](https://dbourdeau.github.io/cyphersolver/egmond.html).\n',1))

p=ROOT/'catalogue.json';d=json.loads(read(p));removed=[e for e in d['entries'] if e['id']==28];assert len(removed)==1
write(R/'catalogue_entry_before.json',json.dumps(removed[0],ensure_ascii=False,indent=2)+'\n')
d['entries']=[e for e in d['entries'] if e['id']!=28];write(p,json.dumps(d,ensure_ascii=False,indent=1)+'\n')
p=ROOT/'CATALOGUE.md';s=read(p);anchor='## Read or resolved here, and removed\n';assert anchor in s
write(p,s.replace(anchor,anchor+'\n- **28 — Charles of Egmond → grand master of France, BnF fr. 3015 no. 8**: French body and address read with an inferred substitution key and nulls. Arnhem, apparently 18 July; no year established. Minor glyph doubts and literal anomalies retained. [Write-up](https://dbourdeau.github.io/cyphersolver/egmond.html).\n',1))
p=DOCS/'index.html';s=read(p);idx=s.index('<ul class="findings">',s.index('<h2 id="recent">'))+len('<ul class="findings">')
li='\n<li><b>Charles of Egmond to the grand master of France, year unknown</b> &mdash; <span class="fnd">ciphered body and address read</span>. A request for support after entering war on the king’s commands; Arnhem, apparently 18 July. Minor glyph doubts retained. <a href="egmond.html">write-up</a></li>'
write(p,s[:idx]+li+s[idx:])
print('Prepared Egmond page, figures, profile and ledgers.')
