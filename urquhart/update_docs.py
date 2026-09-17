# One-off: update site page, manifest, index, README and tracker for the completed octastich reading (16 Sept 2026).
import re, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def rw(path, fn):
    p = os.path.join(ROOT, path); s = open(p, encoding='utf-8').read(); s2 = fn(s)
    assert s2 != s, path
    open(p, 'w', encoding='utf-8').write(s2)


def site(s):
    s = s.replace("<title>Urquhart's encrypted poems (1652–53) — Adjudicated</title>", "<title>Urquhart's Cyphral Octastich (1652) — Read</title>")
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Thomas Urquhart\'s Cyphral Octastich of 1652 read in full: a book cipher on his own Jewel, the k-th number indexing the first word of the needed initial on page k; 238 of 284 first-occurrence hits against 0.43 for controls; the companion distich claim not reproduced.">', s)
    s = s.replace('· 1652–53 · adjudicated</p>', '· 1652–53 · octastich read</p>')
    s = s.replace('The octastich rule published as a Claude Fable 5.1 result on 31 August 2026 is reproduced here from the EEBO-TCP text and the public transcription, without the claimed plaintext, and passes shuffled controls; the distich rule does not reproduce.',
                  'The octastich is read in full from the EEBO-TCP text of <em>The Jewel</em> and a fresh transcription of its 285 numbers from the 1983 edition, without using the plaintext published by Vals AI on 31 August 2026; 238 of 284 numbers are first-occurrence hits against 0.43 for both controls. The distich rule does not reproduce.')
    a = s.index('<div class="callout">'); b = s.index('</div>', a) + 6
    callout = '''<div class="callout">
<strong>Summary.</strong> Urquhart printed a verse under the octastich saying the key was “gather’d out of my Exskybalorum” and that he loved “an aphaeresified treason”:
the cipher takes word-initials from the book it is printed in. The <em>k</em>-th number, counting straight through the poem, is a word index into physical page <em>k</em>
of the 1652 <em>Jewel</em>, and Urquhart took the <em>first</em> word on the page that began with the letter he wanted. That habit makes the rule testable without any
plaintext: whether number <em>n</em> on page <em>k</em> is the first word of its own initial is a fact about the page. The public transcription (Schmeh, 2015) turned out
to be short by thirteen numbers; the 1983 Jack and Lyall edition, photographed on the HCPortal record, gives 285. Decoded one number per page against the TCP text,
238 of 284 are first-occurrence hits, against 0.43 for the same numbers shuffled and 0.44 for random pages, and the poem reads: <em>Great Lord, mantaine that regal
familie, / Whereof King Charls the second is the head, / And grant that he may beare the supreme sweigh / Where English, Scots and Irsh are borne and bred; / And
[…] this usurp’d authoritie / Reigne in his royal predecessors stead: / Let him be our sole Cesar, Artur, Hector, / Our Emperour, King, Monarch and Protector. / Amen,
so be it.</em> Vals AI published this rule and plaintext on 31 August 2026 as a Claude Fable 5.1 result; here it is reached from the text and the numbers alone, and
their two caveats are traced to defects of the digitised copy. The distich claim, <em>i</em>-th number into the <em>i</em>-th Proquiritation, gives 34 of 64
first-occurrence hits, chance for texts that short, and no English.
<em>Status: octastich read, ten letters of line 5 excepted; distich open.</em>
</div>'''
    s = s[:a] + callout + s[b:]
    a = s.index('<p>The EEBO-TCP transcription of <em>The Jewel</em> was parsed'); b = s.index('</p>', a) + 4
    s = s[:a] + '''<p>The EEBO-TCP transcription of <em>The Jewel</em> was parsed into word lists per page. The 1652 printer numbered pages 34–35, 38–39, 42–43 and 46–47 twice and skipped
60 and 110, so pages are counted physically from p. 1, and three duplicated page breaks that the TCP carries for re-shot images are removed. Schmeh’s 272-number
transcription, the only one in circulation since 2015, omits the run-over lines of stanzas 2 and 6, one figure, and misreads one; a dynamic-programme alignment that may
skip pages still placed it at 231 first-occurrence hits in 267 and read five lines. The photographs of the 1983 edition on the HCPortal record give the full 285, which
then decode straight, one number per page.</p>''' + s[b:]
    a = s.index('<table>'); b = s.index('</table>', a) + 8
    s = s[:a] + '''<table>
<thead><tr><th>Run</th><th>First-occurrence rate</th></tr></thead>
<tbody>
<tr><td>The 285 numbers, one per physical page</td><td>0.838 (238/284)</td></tr>
<tr><td>Same numbers shuffled, 200 trials</td><td>mean 0.434, max 0.491</td></tr>
<tr><td>Numbers in order, pages randomly permuted, 200 trials</td><td>mean 0.436, max 0.509</td></tr>
<tr><td>Schmeh’s 272 numbers, aligned with page skips</td><td>0.865 (231/267), vs 0.686 shuffled and re-aligned</td></tr>
<tr><td>Distich, <em>i</em>-th number into <em>i</em>-th Proquiritation</td><td>0.53 (34/64), no English</td></tr>
<tr><td>Distich, shuffled, against pages of <em>The Jewel</em>, 100 trials</td><td>mean 0.50, max 0.62</td></tr>
</tbody></table>''' + s[b:]
    a = s.index('<pre>'); b = s.index('</pre>', a) + 6
    s = s[:a] + '''<pre>
wREATLORDMApTAInETHATREGtaFAMILIE          Great Lord, mantaine that regal familie
WtEREOFKINGCHARLStHaStCONtISTaEHiAD        Whereof King Charls the second is the head
ANDGRAnTTHatHEDAYBEARETHEFUPaEMESgEIGS     And grant that he may beare the supreme sweigh
WHERDENGLIsHSCoTSANDIOSoAREBORNEANDBRED    Where English, Scots and Irsh are borne and bred
AaDCOnERTHTO_aIttSUaPDApTHORIEIE           And [conerthto?] this usurp’d authoritie
REIGtEINMISnOtALPREDECESSORSSifAt          Reigne in his royal predecessors stead
SETHpLBEOURSOLtCESAtAmtaRHECBOR            Let him be our sole Cesar, Artur, Hector
OeREMPoRPUwJINGMONARCHANDPROTECTOR         Our Emperour, King, Monarch and Protector
AMsNSOwLtt                                 Amen, so be it
</pre>''' + s[b:]
    a = s.index('<p>Capitals are first-occurrence hits'); b = s.index('</p>', a) + 4
    s = s[:a] + '''<p>Capitals are first-occurrence hits, lower case a word a few places off in the TCP tokenisation, <code>_</code> the one page (physical 158) whose text the TCP
does not carry. The right-hand column is the reading.</p>''' + s[b:]
    a = s.index('<p>Where the public transcription is intact'); b = s.index('</p>', a) + 4
    s = s[:a] + '''<p>The reading agrees with Vals’ published plaintext throughout, including the nine letters of line 5 that neither decoder can read (<em>conerthto</em>, pages 149–157,
eight of them exact first-occurrence hits) followed by the one letter on the TCP’s near-empty page 158. Their “one page used twice from position 159” is that page.
<em>Sweigh</em> is Scots <em>swey</em>, “sway”; <em>mantaine</em>, <em>Charls</em>, <em>Cesar</em> and <em>Artur</em> are period spellings. A royalist prayer for Charles II,
written in London in March 1652 by a prisoner of Worcester, hidden in a book dedicated to the vindication of Scotland: entirely in character.</p>''' + s[b:]
    a = s.index('<h2 id="remaining">'); b = s.index('</ul>', a) + 5
    s = s[:a] + '''<h2 id="remaining"><span class="num">05</span> What remains</h2>
<ul>
<li>Ten letters of line 5 (positions 151–160): nine decode as <em>conerthto</em> from the TCP text and one falls on a page the TCP does not carry. A misprint of the 1652
numbers, a miscount by Urquhart, or a divergence between the filmed copy and the print at pages 149–158; the 1652 leaves would settle it.</li>
<li>The 46 positions where the TCP word is not the first of its initial are one to a few words off, tokenisation differences; they do not change the reading.</li>
<li>The distich.</li>
</ul>''' + s[b:]
    a = s.index('<p>In <code>urquhart/</code>:'); b = s.index('</p>', a) + 4
    s = s[:a] + '''<p>In <code>urquhart/</code>: <code>ct.py</code> holds both transcriptions of the octastich; <code>pages.py</code> parses the TCP XML of A95749 into pages under both
numberings; <code>decode_1983_full.tsv</code> gives every position with page, word, letter and first-occurrence flag; <code>align.py</code> is the alignment used on the
defective transcription; the controls are in the notes. The TCP text comes from the Text Creation Partnership’s GitHub mirror; the 1983 page photographs from the
HCPortal record, whose API answers at api.hcportal.eu.</p>''' + s[b:]
    s = s.replace('<li>HCPortal, cryptogram record 8 (Urquhart octastich), Eugen Antal.</li>',
                  '<li>HCPortal, cryptogram record 7 (Urquhart), Eugen Antal, with photographs of Jack and Lyall (eds), <em>The Jewel</em> (Scottish Academic Press, 1983), p. 212 and facing.</li>')
    return s


def manifest(s):
    s = s.replace("dict(slug='urquhart', label='Urquhart', year='1652&ndash;53', y=1652, place='London', st='partial', stt='octastich rule verified',",
                  "dict(slug='urquhart', label='Urquhart', year='1652', y=1652, place='London', st='solved', stt='octastich read',")
    s = s.replace("title='Urquhart&rsquo;s Cyphral Octastich &mdash; a book cipher on his own Jewel, verified without the plaintext',",
                  "title='Urquhart&rsquo;s Cyphral Octastich &mdash; a book cipher on his own Jewel, read without the plaintext',")
    s = re.sub(r"blurb='Eight lines and a &ldquo;Decagram&rdquo; of numbers on the last leaf of The Jewel \(1652\).*?',\n(\s+)quote=",
               lambda m: "blurb='Eight lines and a &ldquo;Decagram&rdquo; of numbers on the last leaf of The Jewel (1652), Schmeh&rsquo;s Top 50 no. 28. Number k indexes a word on physical page k of the book, and Urquhart took the first word of the initial he needed: a habit checkable without any plaintext. The public transcription was thirteen numbers short; the 1983 edition&rsquo;s photographs on the HCPortal give 285, which decode straight with 238 of 284 first-occurrence hits against 0.43 for shuffled and random-page controls, into a royalist prayer for Charles II. Vals AI published the rule in August 2026 as a Claude Fable 5.1 result; the companion distich claim does not reproduce.',\n" + m.group(1) + "quote=", s, flags=re.S)
    return s


def index(s):
    a = s.index('<li><b>Urquhart&rsquo;s Cyphral Octastich, 1652</b>'); b = s.index('</li>', a) + 5
    return s[:a] + '<li><b>Urquhart&rsquo;s Cyphral Octastich, 1652</b> &mdash; <span class="fnd">read in full, without the plaintext the August 2026 AI claim published; the distich claim not reproduced.</span> The k-th number indexes physical page k of Urquhart&rsquo;s own <em>Jewel</em>, and he took the first word of the initial he needed, a property of number and page alone. The public transcription was thirteen numbers short; the 1983 edition&rsquo;s photographs on the HCPortal record give 285, which decode straight against the TCP text with 238 of 284 first-occurrence hits against 0.43 for shuffled and random-page controls: a prayer for Charles II, <em>Great Lord, mantaine that regal familie &hellip; Our Emperour, King, Monarch and Protector. Amen, so be it.</em> Ten letters of line 5 stay unread. The distich rule gives 34 of 64, chance, and no English. <a href="urquhart.html">Full write-up &rarr;</a></li>' + s[b:]


def readme(s):
    a = s.index("| Urquhart's Cyphral Octastich and Distich"); b = s.index('\n', a) + 1
    s = s[:a] + s[b:]
    row = "| Urquhart's Cyphral Octastich, The Jewel (1652), last leaf | 1652 | Book cipher on the book itself: number k → first word of the needed initial on physical page k; verified from EEBO-TCP A95749 and a new 285-number transcription from the 1983 edition's photographs (HCPortal), without the plaintext Vals AI published in Aug 2026: 238/284 first-occurrence hits vs 0.43 shuffled and random-page controls. A royalist prayer for Charles II in ottava rima, *Great Lord, mantaine that regal familie … Our Emperour, King, Monarch and Protector. Amen, so be it.* Ten letters of line 5 unread (TCP text defect at pp. 149–158). Distich (Works 1834 p. 417): Proquiritation rule 34/64, chance, no English; open | [`urquhart/`](urquhart/) · [write-up](https://dbourdeau.github.io/cyphersolver/urquhart.html) |\n"
    return s.replace("\n### Explained: not a cipher, or nothing to read", row + "\n### Explained: not a cipher, or nothing to read", 1)


def targets(s):
    a = s.index("| 28 | Thomas Urquhart's poems | **octastich rule verified"); b = s.index('Distich: Proquiritation rule', a)
    return s[:a] + "| 28 | Thomas Urquhart's poems | **octastich read 2026-09-16; distich open** | 2026-09-16: book cipher on The Jewel (1652) itself, number k → first word of the needed initial on physical page k. Schmeh's 272-number transcription is 13 short; re-transcribed (285) from the 1983 edition's photographs on the HCPortal API; straight decode against TCP A95749: 238/284 first-occurrence hits vs 0.43 controls; all eight lines and the Decagram read (royalist prayer for Charles II), ten letters of line 5 excepted. Vals AI's Aug 2026 rule confirmed without their plaintext. " + s[b:]


rw('docs/urquhart.html', site)
rw('docs/_build_site.py', manifest)
rw('docs/index.html', index)
rw('README.md', readme)
rw('TARGETS.md', targets)
print('ok')
