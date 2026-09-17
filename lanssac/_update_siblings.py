"""One-off: fold the sibling readings (ff. 160, 164, 174) into NOTES.md, README.md, TARGETS.md, docs/_build_site.py,
docs/index.html and docs/lanssac.html. Run from the repo root. Idempotent (checks for markers)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

def rw(rel, fn):
    p = ROOT / rel; s = p.read_text(encoding='utf-8'); t = fn(s)
    if t != s: p.write_text(t, encoding='utf-8'); print('updated', rel)
    else: print('unchanged', rel)

# ---------------- NOTES.md ----------------
NOTES_ADD = '''
## 8. The other Lanssac letters, read with the same key (second session, 17 Sept 2026)

The "déchiffrement" the catalogue credits to nos. 60, 61, 63, 65 and 70 is the gutter-cut marginal gloss, so their
cipher passages had never been readable from the scan. With the key the three letters that matter for the election
read in substance (reading_siblings.txt; tokens in f160_tokens.txt, f164_tokens.txt, f174_tokens.txt):

- **f. 160, to the King, 1 May** (canvas 307): *Car je veoy que ceste nation est autant vénale et sujette à se laisser
  gaigner par argent comme sont les Allemans leurs voisins.* Every word but "et" and "par" is sign-by-sign; the gloss
  has "autant", "gaigner", "comme son[t]", "[voi]sins".
- **f. 164, to Anjou, 1 May** (canvas 313): the opposing party *a despendu … ensemble … en ceste négotiation;
  l'Empereur en y a despendu plus de trois cens mil …, si faict … riens qu'il vaille …; seulement il le trouble …,
  faisant le pis qu'il peult contre vous.* Firm words: despendu (twice), ensemble, ceste négotiation, plus de trois
  cens mil, faict, riens qu'il vaille, seulement, trouble, desseing, faisant, le pis qu'il peult, contre vous. Four
  runs of 3–7 signs unread; the sign o- is the letter f in *faict* and *faisant* and the word-sign *l'Empereur* before
  *en y a despendu* (two signs conflated, or a variant).
- **f. 174, to the King, Płock, 9 May** (canvas 329), the letter announcing the election: *… qui est reüssy tant
  heureusement [contre la volunté et menées du Grand Seigneur, de l'Empereur, des princes de l'Empire, du Roy
  d'Espaigne, du Moscovite et du Roy de Suède, qui tous estoient bandez contre vostre Majesté].* Firm: contre la
  volunté et, seigneur, des princes, du Roy d'Espaigne, Moscovite, et du Roy de Suède, bandez, contre. From the gloss
  and sign count: Grand, de l'Empire, estoient, vostre. The gloss beside it has "la volunté et", "du Grand", "de
  l'Empereur", "de l'Empire", "de Spaigne", "et du", "Suède, qui tout", "bandez contr[e]", "Majesté", and it puts
  "l'Empereur" beside the o- sign, which is what fixes that word-sign.

New sign values from these leaves: 4 = b (*bandez*, *trouble*, Tomokiyo's value); three strokes = z (*bandez*) as well
as t (*oultre*) and s; the tailed 4 (Tomokiyo's Ꝝ) = p (*Empire*); Λ = ns (*riens*, *cens*); the C with hook = qu
(*qu'il*, twice); the 6-like sign = o (*trouble*, *volunté*); Δ = g (*seigneur*, *gaigner*, *négotiation*, *desseing*);
the plain cross with curl = t in *négotiation* and h in *empesché* (two forms not separated); the o with cross below =
et (*volunté et*, *et du Roy*), which makes f. 124's *retenu ou empesché* rather *retenu et empesché*.

Controls for this session: none beyond the glosses. The joint annealer over all six leaves (1,140 tokens, pins as
before) keeps every pinned value and agrees across three seeds on the frequent free signs (Γ = e, ✱ = e, ꟿ = i,
2 = l) but not on the rare ones (4, the 6-like sign, ⊓, o-, ff-with-bar differ or come out as vowels), so those rest
on the words above. Not done: ff. 156v–157 (rest of the letter to Catherine), f. 154 in full, the 9 May letters to
Anjou, Catherine, Brulart and Lanssac père (ff. 182 ff.), and Monluc's cipher, which is another system. Tomokiyo's
"f. 331" is not a Lanssac item in the BnF notice (f. 330 is Crosne, 1587; f. 334 Brulart, 1586).
'''
def notes(s):
    if '## 8. The other Lanssac letters' in s: return s
    s = s.replace('\n## 7. Files', NOTES_ADD + '\n## 7. Files')
    s = s.replace('**Verdict: read.** Both cipher passages of the letter are recovered',
                  '**Verdict: read; key carried to three sibling letters (section 8).** Both cipher passages of the letter are recovered')
    s = s.replace('tomokiyo_lansac_key.png (his table, for comparison)',
                  'reading_siblings.txt, f160_tokens.txt, f164_tokens.txt, f174_tokens.txt, cands.py (second session)')
    return s
rw('lanssac/NOTES.md', notes)

# ---------------- README ----------------
README_ROW = ("| Lanssac → Charles IX, Warsaw, 26 Apr 1573, BnF fr. 4735 no. 51 f. 124, and the siblings ff. 160, 164, 174 (catalogue item 3, class A) | 1573 | "
 "**Read** (17 Sept 2026): both cipher passages of f. 124 (96/100 signs) from the Gallica images; homophonic letter cipher with word signs, key fixed from the glossed sibling f. 154v "
 "(\"car je n'ay pas cinquante escuz\"), the gutter-cut marginal fragments, and a pinned annealer with shuffled and blind controls. The key then reads the three election letters whose "
 "\"déchiffrement\" is only that cut gloss: 1 May to the King, *ceste nation est autant vénale et sujette à se laisser gaigner par argent comme sont les Allemans*; 1 May to Anjou, "
 "*l'Empereur en y a despendu plus de trois cens mil … faisant le pis qu'il peult contre vous*; 9 May from Płock, the election carried *contre la volunté et menées du Grand Seigneur, de l'Empereur, "
 "des princes de l'Empire, du Roy d'Espaigne, du Moscovite et du Roy de Suède, qui tous estoient bandez contre vostre Majesté*. Tomokiyo's table for the cipher corrected. Short runs unread, flagged | [`lanssac/`](lanssac/) · [write-up](https://dbourdeau.github.io/cyphersolver/lanssac.html) |")
def readme(s):
    i = s.index('| Lanssac → Charles IX, Warsaw, 26 Apr 1573'); j = s.index('\n', i)
    return s[:i] + README_ROW + s[j:]
rw('README.md', readme)

# ---------------- TARGETS ----------------
def targets(s):
    old = 'f. 331 (same cipher) not looked at |'
    new = ('Second session: key carried to ff. 160, 164, 174 (1 and 9 May; their "déchiffrement" is the cut gloss): venality of the Polish nation, '
           'the Emperor\'s 300,000 spent, and the 9 May list of the powers "bandez contre vostre Majesté" (Grand Seigneur, Emperor, princes of the Empire, Spain, Muscovy, Sweden). '
           '`reading_siblings.txt`. Tomokiyo\'s "f. 331" is not a Lanssac item in the notice; ff. 156v–157, 182 ff. not read |')
    return s.replace(old, new)
rw('TARGETS.md', targets)

# ---------------- _build_site ----------------
def site(s):
    s = s.replace("Both passages read: the dangers French travellers meet in Germany, and how, without his Saxon escort, Lanssac would have been detained or stopped on his way to Warsaw. Tomokiyo&rsquo;s published table for the cipher is corrected.",
      "Both passages read, and the key then opens the three election letters whose only &ldquo;decipherment&rdquo; was that cut gloss: the Polish nation &ldquo;autant v&eacute;nale &hellip; comme sont les Allemans&rdquo;, the Emperor&rsquo;s three hundred thousand spent for nothing, and on 9 May the election carried against the Sultan, the Emperor, the princes of the Empire, Spain, Muscovy and Sweden, &ldquo;qui tous estoient bandez contre vostre Majest&eacute;&rdquo;. Tomokiyo&rsquo;s published table for the cipher is corrected.")
    s = s.replace("quote='&ldquo;j&rsquo;eusse sans doubte pour le moins est&eacute; retenu ou empesch&eacute; de passer oultre&rdquo;',",
                  "quote='&ldquo;qui tous estoient bandez contre vostre Majest&eacute;&rdquo; &middot; P&#322;ock, 9 May 1573',")
    return s
rw('docs/_build_site.py', site)

# ---------------- index finding ----------------
INDEX_LI = ('<li><b>Lanssac&rsquo;s Polish election letters, April&ndash;May 1573</b> &mdash; <span class="fnd">read; the first class-A item of the new catalogue, and with it the three election letters whose &ldquo;d&eacute;chiffrement&rdquo; was only a gutter-cut gloss.</span> '
 'BnF fr. 4735 f. 124 (26 April) is catalogued &ldquo;avec chiffre&rdquo; with no decipherment. One surviving gloss line on the sibling f. 154v, &ldquo;car je n&rsquo;ay pas cinquante escuz&rdquo;, fixes eleven signs; the fragments on f. 124 fix the rest; a pinned annealer fills in the remainder against shuffled and blind controls. '
 'The same key then reads 1 May to the King (<em>ceste nation est autant v&eacute;nale et sujette &agrave; se laisser gaigner par argent comme sont les Allemans</em>), 1 May to Anjou (<em>l&rsquo;Empereur en y a despendu plus de trois cens mil &hellip; faisant le pis qu&rsquo;il peult contre vous</em>) and 9 May from P&#322;ock, the election carried <em>contre la volunt&eacute; et men&eacute;es du Grand Seigneur, de l&rsquo;Empereur, des princes de l&rsquo;Empire, du Roy d&rsquo;Espaigne, du Moscovite et du Roy de Su&egrave;de, qui tous estoient bandez contre vostre Majest&eacute;</em>. '
 'Tomokiyo&rsquo;s table for this cipher is off by one letter from <em>m</em>. <a href="lanssac.html">Write-up</a>.</li>')
def index(s):
    i = s.index('<li><b>Lanssac'); j = s.index('</li>', i) + 5
    return s[:i] + INDEX_LI + s[j:]
rw('docs/index.html', index)

# ---------------- lanssac.html ----------------
SEC = '''
<h2 id="siblings"><span class="num">05</span> The election letters, read with the same key</h2>
<p>The catalogue credits Lanssac&rsquo;s letters of 24 April, 1 May and 9 May with a &ldquo;d&eacute;chiffrement&rdquo;. It is the Court decipherer&rsquo;s note in the outer margin, and the microfilm keeps
only the last word or two of each of its lines; the cipher passages themselves had never been readable from the scan. With the key they read in substance. Transcriptions and sign-by-sign
choices are in <code>lanssac/reading_siblings.txt</code>; unread runs are in braces, and words read from the gloss and the sign count rather than sign by sign carry a query.</p>
<figure><img src="lanssac_f174.jpg" alt="BnF fr. 4735 f. 174, Lanssac to Charles IX from Plock, 9 May 1573: the ciphered list of the powers opposed to the election, with the decipherer's gloss in the margin" loading="lazy">
<figcaption>Fr. 4735 f. 174 (canvas 329): the six ciphered lines of the 9 May letter and the gloss beside them &mdash; &ldquo;&hellip;la volunt&eacute; et / &hellip;du Grand / &hellip;de l&rsquo;Empereur / &hellip;de l&rsquo;Empire / &hellip;de Spaigne / &hellip;et du / &hellip;Su&egrave;de, qui tou[s] / &hellip;bandez contr[e] / &hellip;Majest&eacute;&rdquo;.</figcaption></figure>
<blockquote>
<strong>To Charles IX, Warsaw, 1 May 1573 (f. 160).</strong> &hellip; que pour en envoyer devant selon que les occasions des affaires premi&egrave;rement surviennent. [Car je veoy que ceste nation
est autant v&eacute;nale et? sujette &agrave; se laisser gaigner par argent comme sont les Allemans leurs voisins.] Ce jourd&rsquo;huy ilz mettent en d&eacute;lib&eacute;ration s&rsquo;ilz doibvent prendre pour Roy ung Piaste
ou ung prince estrangier, mais on s&ccedil;ait bien quelle en doibt estre la r&eacute;solution.
</blockquote>
<blockquote>
<strong>To the duc d&rsquo;Anjou, Warsaw, 1 May 1573 (f. 164).</strong> &hellip; c&rsquo;est de latin et d&rsquo;argent, et &agrave; bonne quantit&eacute;, car il y aura de quoy l&rsquo;employer [&agrave; vostre d&eacute;sir]. &hellip;
les traverses de nos contraires qui n&rsquo;y espargnent rien pour nous empescher, [{5 signs} a despendu {4 signs} ensemble {7 signs}. C&rsquo;est en ceste n&eacute;gotiation; l&rsquo;Empereur en y a despendu
plus de trois cens mil {3 signs}, si faict {5} {5}, riens qu&rsquo;il vaille pour ser{&hellip;}. Seulement il le trouble {7 signs}, desseing faisant le pis qu&rsquo;il peult contre vous.] Encores ne veulx-je
faillir, Monseigneur, de vous ramentevoir &hellip; que vous fassiez donner ordre que les navires soient prestz pour l&rsquo;embarquement.
</blockquote>
<blockquote>
<strong>To Charles IX, P&#322;ock, 9 May 1573 (f. 174).</strong> &hellip; ayant est&eacute; employ&eacute; en un affaire de telle importance et qui est re&uuml;ssy tant heureusement [contre la volunt&eacute; et
men&eacute;es? du Grand? Seigneur, de l&rsquo;Empereur, des princes de l&rsquo;Empire?, du Roy d&rsquo;Espaigne, du Moscovite, {3 signs} et du Roy de Su&egrave;de, qui tous estoient? bandez contre vo[st]re Majest&eacute;].
Si est-ce que j&rsquo;auray encores plus d&rsquo;occasion de louer Dieu si je suis tant heureux que vostre Majest&eacute; me juge digne d&rsquo;estre employ&eacute; en ce second &hellip;
</blockquote>
<h3>English</h3>
<blockquote>
<strong>1 May, to the King.</strong> For I see that this nation is as venal and as ready to let itself be won by money as are the Germans, their neighbours. &mdash;
<strong>1 May, to Anjou.</strong> &hellip; has spent &hellip; together &hellip;. It is in this negotiation; the Emperor has spent more than three hundred thousand in it &hellip; and done nothing worth the name &hellip;;
he can only trouble the design, doing the worst he can against you. &mdash;
<strong>9 May, to the King.</strong> &hellip; an affair of such weight, which has succeeded so happily against the will and the intrigues of the Grand Seigneur, of the Emperor, of the princes of the
Empire, of the King of Spain, of the Muscovite and of the King of Sweden, who were all leagued against your Majesty.
</blockquote>
<p>The 9 May list is the field of the 1573 election as the French embassy saw it: Archduke Ernest for the Emperor and Spain, Ivan IV, John III of Sweden, and a Habsburg-leaning party among
the German princes. The &ldquo;Grand Seigneur&rdquo; (the Sultan) is the surprise, since the Porte was generally reckoned to favour the French candidate, and that group is read from the gloss
(&ldquo;du Grand&rdquo;) and the sign count rather than sign by sign. The 300,000 of f. 164 is the Habsburg outlay as Lanssac reckoned it; the unit sits in an unread group. New sign values from
these leaves &mdash; 4&nbsp;=&nbsp;b, three strokes&nbsp;=&nbsp;z as well as t, the tailed 4&nbsp;=&nbsp;p, &Lambda;&nbsp;=&nbsp;ns, the hooked C&nbsp;=&nbsp;qu, the 6-like sign&nbsp;=&nbsp;o, &Delta;&nbsp;=&nbsp;g, the o with cross below&nbsp;=&nbsp;et &mdash;
are listed in the notes; the last makes f. 124&rsquo;s &ldquo;retenu ou empesch&eacute;&rdquo; rather &ldquo;retenu et empesch&eacute;&rdquo;.</p>
'''
def page(s):
    if 'id="siblings"' in s: return s
    s = s.replace('<p class="sub">Key recovered from the glossed sibling letters of 24 April (ff. 154, 156) and the decipherer&rsquo;s marginal fragments on f. 124 itself; 96 of 100 signs read</p>',
      '<p class="sub">Key recovered from the glossed sibling letters of 24 April (ff. 154, 156) and the decipherer&rsquo;s marginal fragments on f. 124 itself; 96 of 100 signs read &middot; the same key then reads the election letters of 1 and 9 May (ff. 160, 164, 174)</p>')
    s = s.replace('Tomokiyo&rsquo;s published table for this cipher is corrected (first row shifted by one letter from m).</em>',
      'Tomokiyo&rsquo;s published table for this cipher is corrected (first row shifted by one letter from m). Section 05 carries the key into the three election letters of 1 and 9 May, whose catalogued &ldquo;d&eacute;chiffrement&rdquo; is only the gutter-cut gloss.</em>')
    s = s.replace('<h2 id="residuals"><span class="num">05</span> What remains uncertain</h2>', SEC + '\n<h2 id="residuals"><span class="num">06</span> What remains uncertain</h2>')
    s = s.replace('<h2 id="method"><span class="num">06</span> Method</h2>', '<h2 id="method"><span class="num">07</span> Method</h2>')
    s = s.replace('<h2 id="sources"><span class="num">07</span> Sources</h2>', '<h2 id="sources"><span class="num">08</span> Sources</h2>')
    old = ('<li>The sibling letters ff. 154&ndash;164 are transcribed only in part and as a first pass; they carry their own decipherments in the margin and hold nothing locked. Tomokiyo also lists\n'
           'f. 331 in the same cipher, with no decipherment noted; it has not been looked at.</li>')
    new = ('<li>The sibling readings of section 05 are first readings from the microfilm: f. 160 is sign by sign, f. 164 has four unread runs and one word-sign (<em>l&rsquo;Empereur</em>) fixed only by the f. 174 gloss, and in f. 174 &ldquo;Grand&rdquo;, &ldquo;de l&rsquo;Empire&rdquo;, &ldquo;estoient&rdquo; and &ldquo;vostre&rdquo; rest on the gloss and the sign count. Ff. 156v&ndash;157, the rest of f. 154 and the 9 May letters to Anjou, Catherine and Brulart (ff. 182 ff.) are not read. Tomokiyo&rsquo;s &ldquo;f. 331&rdquo; is not a Lanssac item in the BnF notice.</li>')
    s = s.replace(old, new)
    return s
rw('docs/lanssac.html', page)
