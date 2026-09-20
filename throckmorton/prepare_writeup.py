"""Prepare the result on an isolated copy of the current site; no publication."""
import html, json, pathlib, re, shutil, sys

source = pathlib.Path(__file__).resolve().parent
repo = pathlib.Path(sys.argv[1]).resolve()
assert (repo/'.git').exists() and (repo/'docs/_build_site.py').exists()
target = repo/'throckmorton'
target.mkdir(exist_ok=True)
for p in source.iterdir():
    if p.is_file() and (p.suffix in ('.md','.json','.txt','.py') or p.name=='.gitignore'):
        shutil.copy2(p, target/p.name)

rows=json.loads((source/'concordance.json').read_text(encoding='utf-8'))
table='\n'.join('<tr><td><a href="https://de-crypt.org/decrypt-web/RecordsView/'+r['record'][1:]+'">'+r['record']+'</a></td><td>'+html.escape(r['folio'])+'</td><td>'+html.escape(r['date'])+'</td><td>'+html.escape(r['recipient'])+'</td><td><a href="'+r['url']+'">CSP '+str(r['csp_volume'])+', '+str(r['csp_entry'])+'</a>; '+html.escape(r['edition'])+'</td><td>'+html.escape(r['evidence'])+'</td></tr>' for r in rows)
page='''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Throckmorton (1560–63) — Archived key and published plaintext verified</title>
<meta name="description" content="BL Add MS 4136: twenty DECODE records matched to published correspondence, with two short passages verified against Throckmorton's third cipher. Prior solution, not twenty new decryptions.">
<link rel="stylesheet" href="style.css"></head><body>
<!-- site:nav -->
<section class="hero">
<p class="kicker">France → Cecil, Elizabeth I and the Council · Homophones and nomenclator · 1560–63 · Prior solution verified</p>
<h1>Throckmorton: the key survives, and the text was printed</h1>
<p class="sub">Twenty records catalogued as non-decrypted in BL Add MS 4136 lead to surviving keys, Forbes's eighteenth-century edition and the Calendar of State Papers. Two samples verify the connection.</p>
<p class="meta">Daniel Bourdeau</p></section>
<main>
<div class="callout"><strong>Summary.</strong> The proposed target was a group of twenty DECODE records, R9220–R9234, R9242–R9245 and R9255. All 54 image references were obtained; they represent 39 distinct photographs because adjacent records share leaves. Four nearby key records add 17 photographs. R9262 supplies the archived “Third Cipher” and reads a complete numbered extract on R9220, matching Forbes I, p.355. A second, shorter check on R9230 matches Forbes II, p.12. A twenty-record concordance identifies published counterparts, most by date and addressee. These are <strong>42 verified tokens, not twenty complete decryptions</strong>. Tomokiyo had already identified the printed texts and surviving keys; this result confirms that route and corrects the target description.</div>

<h2 id="reading"><span class="num">01</span> A key test on the first leaf</h2>
<p>R9220, f.110, begins in the middle of a letter. Its first complete numbered extract, (6), reads:</p>
<blockquote>all be it i be revoked or the warr breake</blockquote>
<p>In modern English: “albeit I be recalled, or war break out.” Throckmorton is asking Cecil to obtain permission for Mr Jones to remain abroad and gain experience, even if the ambassador is recalled or war begins. Forbes prints the phrase in volume I (1740), p.355, within the 7 March 1559/60 despatch. The same leaf includes the 8 March continuation and the separate letter to the Queen of 9 March.</p>
<p>The 27 transcribed cipher tokens include two nulls. The alphabet on R9262 image P1 supplies the letters: dotted 4, 5 and 6 all represent <em>r</em>; plain 4 represents <em>o</em>; colon-marked 6 represents <em>u/v</em>. P3 gives the marked A for <em>all</em> and marked b for <em>be</em>. P4 gives the suffix <em>-ed</em>, and P9 gives the curved T for <em>the/to</em>. Thus the reading tests the alphabet, word signs, suffixes and nulls together. The final word before <em>breake</em> is <em>warr</em>, with two different r homophones, not <em>wars</em>.</p>
<p>R9230, f.133, offers a second check at the opening of extract (1):</p>
<blockquote>orleans or burges</blockquote>
<p>These fifteen alphabet tokens agree with Forbes II (1741), p.12. CSP Foreign V, no.425, paragraph 11 summarizes the surrounding warning: the apparent preparations against Orleans or Bourges may conceal an attack on Rouen, Newhaven (Le Havre), and Dieppe. No.426 describes a separate decipher of the ciphered passages. The rest of that sentence has not been transcribed token by token here.</p>
<p>Both checks have grade <strong>H</strong>: values read from the archived key. Spacing and capitalization are editorial. The printed counterparts were available during verification, so these are known-plaintext checks, not blind decipherments. The token labels and values are preserved in <code>control.json</code> and <code>control_9230.json</code>, with a replay script. The script verifies substitution of those labels; inspection of the images establishes the glyph identifications.</p>

<h2 id="keys"><span class="num">02</span> Four nearby records are not four interchangeable keys</h2>
<table><thead><tr><th>Record</th><th>Leaf and contents</th><th>Use here</th></tr></thead><tbody>
<tr><td><a href="https://de-crypt.org/decrypt-web/RecordsView/9257">R9257</a></td><td>f.172; Percy extracts above a separate alphabet and nomenclator</td><td>Not established as a Throckmorton key</td></tr>
<tr><td><a href="https://de-crypt.org/decrypt-web/RecordsView/9260">R9260</a></td><td>ff.177–178; a preceding fragment and Throckmorton's first/second keys</td><td>Earlier systems, not the key tested here</td></tr>
<tr><td><a href="https://de-crypt.org/decrypt-web/RecordsView/9261">R9261</a></td><td>f.179; heading “Sr Thomas Smith's Cipher”</td><td>A different alphabet, relevant to distinguishing Smith material</td></tr>
<tr><td><a href="https://de-crypt.org/decrypt-web/RecordsView/9262">R9262</a></td><td>ff.180–185; “Sr Nicholas Throckmorton's Third Cipher,” eleven photographs</td><td>Matches both sampled passages</td></tr>
</tbody></table>
<p>The third cipher combines homophonic letters, marked initial-letter codes for words, names and places, morphological endings and nulls. Dots distinguish values; a two-digit superscript system is not the explanation of these samples. The archive contains reconstructed keys: its catalogue date does not prove that these sheets were the original operational keys.</p>

<h2 id="concordance"><span class="num">03</span> Record-to-edition concordance</h2>
<p>These are source counterparts, with direct passage tests only where stated. CSP often abridges the full letters. Dates use January-start years: March 1559 becomes March 1560, and January 1562 becomes January 1563, without changing the day. R9234 remains 1 November 1563. Shared leaves must be separated at the letter headings before assigning their passages.</p>
<div class="tablewrap"><table><thead><tr><th>DECODE</th><th>Folios</th><th>Date</th><th>To</th><th>Published source</th><th>Evidence and limits</th></tr></thead><tbody>
'''+table+'''
</tbody></table></div>
<p>R9232 is a provisional match to CSP V no.597: the opening mentions dispatching Francisco on the ninth. Nos.599–600 are other same-day Cecil material and remain comparison candidates. R9255 is composite: the Throckmorton portion matches 22 November 1562, CSP V nos.1099–1100, but the Smith, Somer and Randolph material requires separate identification and keys.</p>

<h2 id="prior"><span class="num">04</span> Prior work and the misleading target description</h2>
<p>Satoshi Tomokiyo's Elizabethan cipher study already identifies the Add MS 4136 ciphertexts as largely extracts, cites Forbes, reconstructs three Throckmorton ciphers, and records the archive keys in a November 2024 note. This is not a newly discovered key or first publication of the plaintext. DECODE's “Non-decrypted” status describes the record and cannot by itself establish that the text is unread.</p>
<p>The remark about meaningful two-digit superscripts comes from the neighbouring Serno Gilino/Bishop of Worcester discussion on the unsolved list. It was misattributed to Throckmorton in the proposed target. Tomokiyo's two specifically unresolved cases are the marginal ciphertext on R2988 and John Wod's 1568 material on R2989. Both lie outside these twenty records and remain unresolved here.</p>

<h2 id="limits"><span class="num">05</span> What is established, and what is not</h2>
<p>All 71 referenced image files passed JPEG signature checks and have SHA-256 hashes in the research inventory. The 54 target references contain 39 distinct images, including a byte-identical R9220/R9221 pair. Two short passages, totalling 42 tokens, were checked against the third cipher. Their published counterparts agree.</p>
<p>No whole-corpus token count or percentage read is claimed. Most record-to-edition matches have not been checked glyph by glyph. A diplomatic edition would require transcribing the 39 unique leaves, separating all letter boundaries and other writers, and aligning every numbered extract with the printed text. The result resolves the proposed unknown-key premise; it does not stand for a complete edition of the twenty records.</p>

<h2 id="sources"><span class="num">06</span> Sources</h2>
<ul>
<li>British Library, Add MS 4136, via the DECODE records linked above. Manuscript photographs remain in the private research cache; they are not republished on this page.</li>
<li>Patrick Forbes, <em>A Full View of the Public Transactions in the Reign of Q. Elizabeth</em>, <a href="https://archive.org/details/bim_eighteenth-century_a-full-view-of-the-publi_1740_1">I (1740)</a>, especially p.355; <a href="https://archive.org/details/AFullViewofthePublicTransa007">II (1741)</a>, especially p.12. Cached OCR is a finding aid, not a facsimile transcription.</li>
<li><em>Calendar of State Papers, Foreign, Elizabeth</em>, II, V and VI, British History Online; individual entries linked in the concordance.</li>
<li>Satoshi Tomokiyo, <a href="https://cryptiana.web.fc2.com/code/elizabeth.htm">English Ciphers during the Reign of Elizabeth I</a>, Throckmorton sections, and <a href="https://cryptiana.web.fc2.com/code/unsolved.htm">Unsolved Historical Ciphers</a>.</li>
</ul>
<p class="muted">Research files, exact token labels, source inventory and published-text dossier: <a href="https://github.com/dbourdeau/cyphersolver/tree/main/throckmorton">throckmorton/</a>.</p>
</main>
<!-- site:footer -->
</body></html>
'''
(repo/'docs/throckmorton.html').write_text(page,encoding='utf-8')

manifest=repo/'docs/_build_site.py'
s=manifest.read_text(encoding='utf-8')
entry='''    dict(slug='throckmorton', label='Throckmorton', year='1560&ndash;63', y=1561.5, place='France', st='found', stt='key and printed text verified',
         title='Throckmorton &mdash; archived key and published plaintext',
         blurb='Twenty DECODE records in BL Add MS 4136 lead to Forbes and CSP. The archived third cipher reads two short samples, 42 tokens in all. A record-to-edition concordance separates the published counterparts from full token verification; composite material remains to be checked.',
         quote='&ldquo;all be it i be revoked or the warr breake&rdquo;',
         rights='British Library, Add MS 4136, via DECODE; photographs not republished'),
'''
if "slug='throckmorton'" not in s:
    # Builder sorts navigation by y; preserve existing manifest entries verbatim.
    s=s.replace('PAGES = [\n','PAGES = [\n'+entry,1)
if "'throckmorton': None" not in s:
    s=s.replace('IMAGES = {',"IMAGES = {'throckmorton': None, ",1)
manifest.write_text(s,encoding='utf-8')

readme=repo/'README.md';s=readme.read_text(encoding='utf-8')
row='| Nicholas Throckmorton → Cecil, Elizabeth I and the Council, BL Add MS 4136 (20 DECODE records; catalogue 88) | 1560–63 | 20 Sept 2026 | **Archived key and prior printed plaintext verified.** All 54 target image references retrieved (39 unique photographs), plus 17 images in four nearby key records. R9262 reads R9220 extract (6), “all be it i be revoked or the warr breake” (Forbes I p.355), and R9230 “orleans or burges” (Forbes II p.12): 42 tokens. Twenty-record CSP concordance; most matches are by date/addressee, not complete glyph alignment. R9255 combines other writers. Tomokiyo already identified the keys and editions; the superscript note belongs to another cipher. R2988/R2989 remain outside scope. | [`throckmorton/`](throckmorton/) · [write-up](https://dbourdeau.github.io/cyphersolver/throckmorton.html) |\n'
if 'cyphersolver/throckmorton.html' not in s:
    start=s.index('### Found already solved')
    at=s.index('|---|---|---|---|---|',start)+len('|---|---|---|---|---|')
    s=s[:at]+'\n'+row+s[at:]
readme.write_text(s,encoding='utf-8')

index=repo/'docs/index.html';s=index.read_text(encoding='utf-8')
if 'href="throckmorton.html"' not in s:
    at=s.index('<ul class="findings">')+len('<ul class="findings">')
    s=s[:at]+'\n<li><b>Throckmorton to Cecil and the Queen, 1560–63</b> &mdash; <span class="fnd">archived key and printed plaintext verified</span>: two samples, 42 tokens; twenty-record source concordance. <a href="throckmorton.html">write-up</a></li>'+s[at:]
index.write_text(s,encoding='utf-8')

targets=repo/'TARGETS.md';s=targets.read_text(encoding='utf-8')
if 'throckmorton/RESULT.md' not in s:
    s=s.replace('## Done elsewhere in this repo\n','## Done elsewhere in this repo\n\n- **Nicholas Throckmorton, Add MS 4136, twenty records (catalogue 88)** — prior printed counterparts found; R9262 verified on 42 tokens, 20 Sept 2026. See [result](throckmorton/RESULT.md). This excludes the still-open R2988 margin and R2989 John Wod material.\n',1)
targets.write_text(s,encoding='utf-8')

for name in ['SOLVED_CATALOGUE.md','SOLVED_RANKING.md']:
    p=repo/name;s=p.read_text(encoding='utf-8')
    if 'throckmorton/RESULT.md' not in s:
        s+='\n\nNicholas Throckmorton (BL Add MS 4136, 1560–63; catalogue 88): **prior solution verified, unranked**, 20 Sept 2026. Two archive-key samples (42 tokens) and a twenty-record edition concordance; not counted as twenty new solves or a full transcription. See [evidence and limits](throckmorton/RESULT.md).\n'
    p.write_text(s,encoding='utf-8')

p=repo/'catalogue.json';data=json.loads(p.read_text(encoding='utf-8'))
matches=[e for e in data['entries'] if 9220 in e.get('decode_ids',[])]
assert len(matches)<=1
if matches:
    assert matches[0]['id']==88
    (target/'catalogue_entry_before.json').write_text(json.dumps(matches[0],indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    data['entries'].remove(matches[0])
    p.write_text(json.dumps(data,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
    catmd=repo/'CATALOGUE.md';s=catmd.read_text(encoding='utf-8')
    s+='\n\nRemoved 20 Sept 2026: **88, Nicholas Throckmorton, twenty Add MS 4136 records** — archived key and prior printed counterparts verified on two samples; see [result](throckmorton/RESULT.md). Full token alignment and composite-record non-Throckmorton material are not claimed solved.\n'
    catmd.write_text(s,encoding='utf-8')
print('Prepared isolated write-up:',repo/'docs/throckmorton.html')
