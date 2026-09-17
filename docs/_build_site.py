"""Site builder: one manifest drives the navigation, footers, tables of contents and index cards of every page.

Run  python _build_site.py  from docs/ after editing any page. It is idempotent.

Per page it: replaces the first <nav class="nav">...</nav> (or the <!-- site:nav --> marker) with the generated
header; replaces the last <footer>...</footer> (or <!-- site:footer -->) with the generated footer, including
previous / next links in chronological order; inserts an "On this page" contents strip after <main> when the page
has three or more h2 sections with ids; stamps the stylesheet and script versions; and removes inline <style>
blocks whose rules now live in style.css. On index.html it also regenerates the write-up cards between
<!-- cards:start --> and <!-- cards:end -->, and refolds "Recent findings" so that only the newest RECENT_VISIBLE
entries show and the rest sit behind the "Show N earlier findings" button (add new entries at the top of the first
list and rebuild). The priority queue is still built by _build_queue.py.
"""
import re, pathlib, html
HERE = pathlib.Path(__file__).parent
VERSION = '20260917a'
SITE = 'Unsolved Historical Ciphers'
REPO = 'https://github.com/dbourdeau/cyphersolver'

# slug, nav label, year label, sort year, place, status class, status text, title, blurb, quote, rights
PAGES = [
    dict(slug='richelieu', label='Richelieu', year='1629', y=1629, place='France', st='solved', stt='solved',
         title='Richelieu to M. de Ranc&eacute; &mdash; BnF Fran&ccedil;ais 3829',
         blurb='Ciphertext-only recovery of a homophonic alphabet with a doubling mark and nomenclature; then found to agree word for word with the decipherment Avenel printed in 1858, which the catalogues had missed.',
         quote='&ldquo;Castor voudroit bien que la [duchesse de Chevreuse] peust estre attrap&eacute;e pr&egrave;s de la fronti&egrave;re&hellip;&rdquo;',
         rights='Manuscript rights: Biblioth&egrave;que nationale de France'),
    dict(slug='ormonde', label='Ormonde', year='1634&ndash;35', y=1634, place='Ireland / England', st='solved', stt='solved',
         title='Maltravers to Ormonde &mdash; a regular block cipher',
         blurb='Doubled letters written with consecutive figures betray a regular key (consonants three figures each from 7, vowels from 64, nulls 91&ndash;111). Every spelled word reads, and the nomenclator is then confirmed clause for clause against Wentworth&rsquo;s own dispatches in Knowler&rsquo;s <em>Strafforde&rsquo;s Letters</em> (1739): the King refusing Kildare, and Ormonde moved for the Council &ldquo;in exchange&rdquo; for Sir Piers Crosby.',
         quote='&ldquo;he was angry [with the Lord Deputy] &hellip; upon his motion [Ormonde] is to be a councellor&rdquo;'),
    dict(slug='vatican', label='Vatican', year='1542', y=1542, place='Rome &rarr; Spain', st='stuck', stt='family identified',
         title='The Vatican cipher of April 1542 &mdash; an Antonio Elio cipher',
         blurb='Farnese to the nuncio Poggio, four folios, 6,549 digits, open since Lasry set it in 2019. Not read, but named: a polyphonic-syllabic cipher of the design Antonio Elio built for Paul III&rsquo;s chancery. Six sessions, five model classes excluded against matched controls, the Meister keys verified from the scans.',
         quote='27 and 80 end a third of the words &middot; 441 repeated 7-grams against 5 in a shuffle'),
    dict(slug='warsaw', label='Warsaw', year='1627', y=1627, place='Warsaw', st='solved', stt='solved',
         title='From Warsaw, 24 December 1627 &mdash; an alphabet in plain order',
         blurb='DECODE R1408, one page of figures and stray letters with only a dateline in clear, listed as non-decrypted. The letters <em>a</em> and <em>m</em> are nulls, the letter pairs are alternates for consonants, the rare groups are syllables, and the alphabet, recovered blind by a 5-gram-plus-dictionary annealer against shuffled controls, turns out to run in order: odd figures <em>a</em> to <em>m</em>, even figures <em>n</em> to <em>z</em>. A reminder that a promised canonry of Olm&uuml;tz for one of the Queen of Poland&rsquo;s sons has not been conferred.',
         quote='&ldquo;un canonicato d&rsquo;Olmiz ad uno de li suoi figli &hellip; si degni darne subito a me benigna risposta&rdquo;'),
    dict(slug='segur', label='S&eacute;gur', year='1585&ndash;86', y=1585, place='B&eacute;arn &rarr; Germany', st='solved', stt='solved',
         title='Henry of Navarre to S&eacute;gur &mdash; an alphabetical syllabary cipher',
         blurb='Three letters in figures to the envoy raising a German army, BnF 500 de Colbert 401 ff. 233, 239 and 288v, catalogued as undeciphered letters of Henry III. The upper figures pile into one slot in five (mod 5), the signature of a syllable table in alphabetical order; an annealer built on that structure, with the letters&rsquo; own clear French as context, returns a key whose letter part is alphabetical by itself and reads a matched control at 97&nbsp;%. Conclude with Duke Casimir, raise the largest levy, march it at once; Clervant&rsquo;s two thousand reiters; the Vivarais or Dauphin&eacute; road.',
         quote='&ldquo;faictes s&rsquo;il vous est possible la plus grande lev&eacute;e qui ayt est&eacute; faite&rdquo;'),
    dict(slug='boswell', label='Boswell', year='1643', y=1643, place='Oxford &rarr; The Hague', st='solved', stt='read in substance',
         title='Charles I and Nicholas to Boswell &mdash; a regular key, four signs and the wrong addressee',
         blurb='Two ciphered letters of 2 November 1643 (TNA SP 84/157). The alphabet is Robert Pitt&rsquo;s: a 24-letter row four times over 20&ndash;115, verified here at z&nbsp;=&nbsp;9.6 against 20,000 permuted rows. Added here: the four graphic signs are word-signs introduced inside the spelled word (good, Cousin, Master, us), and the King&rsquo;s letter is his re-credentials to the Duke of Courland&rsquo;s envoy, sent through Boswell in Boswell&rsquo;s cipher. Both letters read in substance.',
         quote='&ldquo;back to our good Cousin your Master, to whom we herewith send your re-credentials&rdquo;'),
    dict(slug='forster', label='Forster', year='1644', y=1644.2, place='France', st='found', stt='read by others, verified',
         title='Sir Richard Forster, 13 May 1644 &mdash; verified blind, and why the first attack fails',
         blurb='Already read by Lasry, Biermann and Pitt; Tomokiyo&rsquo;s page still says unsolved. Not a regular Stuart key but a mixed homophonic alphabet of 34 symbols over 207 tokens. Pitt&rsquo;s key stands at z&nbsp;=&nbsp;8.8 against 20,000 permutations, and an annealer recovers 31 of 34 symbols blind &mdash; but only after the French model writes <em>u</em> for <em>v</em> and <em>i</em> for <em>j</em>; before that it reads five of six matched controls and still fails the target.',
         quote='&ldquo;prenez seulement les uoyes de prudence pour conseruer uotre uie&rdquo; &middot; 202 of 207 tokens blind'),
    dict(slug='lucca', label='Lucca', year='1644', y=1644, place='Vienna', st='solved', stt='solved',
         title='Fra Giovanni di Lucca to the Emperor &mdash; a polyphonic figure cipher',
         blurb='DECODE R2159, 231 dot-delimited figures of Italian, listed as non-decrypted and left half-read on Tomokiyo&rsquo;s page because its crib is self-contradictory under any substitution. It is a 24-figure alphabet in which 17 stands for both <em>i</em> and <em>n</em> and 19 for both <em>t</em> and <em>s</em>. Eight crib letters fixed, the rest annealed, every seed agrees, shuffled controls do not; a Viterbi pass over the two alternatives reads it end to end: an offer to keep the Turk off R&aacute;k&oacute;czi, raise Moldavia against him and give two thousand Cossacks.',
         quote='&ldquo;il principe di Bogdania, et li dar&ograve; dumilia Cosachi &hellip; che non faccia pace fin che l&rsquo;habbi humiliato o vinto&rdquo;'),
    dict(slug='feuquieres', label='Feuqui&egrave;res', year='1691', y=1691, place='Pignerol &rarr; Suze', st='solved', stt='read',
         title='Feuqui&egrave;res to Catinat &mdash; the petit chiffre of the Pignerol governors',
         blurb='The 418-group despatch of 25 January 1691 that the 1819 editor of Catinat&rsquo;s papers could not read and Bazeries read but never printed. The same edition prints a second letter in the same 367-group code, Louvois to d&rsquo;Herleville of 6 September 1690, with its contemporary translation; the two letters share 72 groups, and hand alignment carried between them reads 586 of their 601 tokens. Feuqui&egrave;res&rsquo; plan for the surprise of Veillane: two roads into the town, eighty horse to Saint-Ambroise, an attack at two points, and the dragoons not to be let escape into the castle.',
         quote='&ldquo;j&rsquo;attaqueray [par] deux endrois, et surtout &hellip; prendray garde que les dragons ne puissent m&rsquo;eschaper&rdquo;',
         rights='Page images: Bayerische Staatsbibliothek, CC BY-NC-SA'),
    dict(slug='catinat1691', label='Catinat 1691', year='1691', y=1691.5, place='Versailles &rarr; Piedmont', st='solved', stt='read',
         title='Louis XIV and Louvois to Catinat &mdash; seven Grand Chiffre despatches, and the decision to abandon Piedmont',
         blurb='The 1819 editor of Catinat&rsquo;s papers printed seven court despatches of July&ndash;September 1691 in figures and could not read them; Bazeries rebuilt the code from them in 1893, printed two in clear for the Man in the Iron Mask, and stopped. His table reads all seven from the library&rsquo;s OCR of the volume, 12,362 groups, checked against the page images; the two he printed agree at 98 and 99 %. The other five are read here for the first time, among them the King&rsquo;s twenty-page letter of 14 September: bring the army back over the Alps, hold the passes, keep Carmagnole to cover the negotiation with the Pope, then burn it, and take Coni in the winter.',
         quote='&ldquo;je me suis d&eacute;termin&eacute; &agrave; pr&eacute;f&eacute;rer le parti solide &agrave; l&rsquo;honorable&rdquo; &middot; Louis XIV, 14 September 1691',
         rights='Page images: Bayerische Staatsbibliothek, CC BY-NC-SA'),
    dict(slug='urquhart', label='Urquhart', year='1652', y=1652, place='London', st='solved', stt='octastich read',
         title='Urquhart&rsquo;s Cyphral Octastich &mdash; a book cipher on his own Jewel, read without the plaintext',
         blurb='Eight lines and a &ldquo;Decagram&rdquo; of numbers on the last leaf of The Jewel (1652), Schmeh&rsquo;s Top 50 no. 28. Number k indexes a word on physical page k of the book, and Urquhart took the first word of the initial he needed: a habit checkable without any plaintext. The public transcription was thirteen numbers short; the 1983 edition&rsquo;s photographs on the HCPortal give 285, which decode straight with 238 of 284 first-occurrence hits against 0.43 for shuffled and random-page controls, into a royalist prayer for Charles II. Vals AI published the rule in August 2026 as a Claude Fable 5.1 result; the companion distich claim does not reproduce.',
         quote='&ldquo;Great Lord, mantaine that regal familie &hellip; Our Emperour, King, Monarch and Protector&rdquo;'),
    dict(slug='mondoucet', label='Mondoucet', year='1571&ndash;74', y=1572, place='Brussels &rarr; the Court', st='stuck', stt='corpus found, key open',
         title='Mondoucet&rsquo;s cipher &mdash; twenty despatches nobody listed',
         blurb='A Gallica sweep for volumes outside the standard lists found BnF fr. 16127, the Court&rsquo;s file of Claude de Mondoucet&rsquo;s correspondence from the Low Countries, 1571&ndash;74: about twenty ciphered despatches in one system, most with the Court&rsquo;s decipherment, one long letter of 13 July 1572 without. Two verbatim pairs, one glossed word by word by the decipherer, were transcribed three ways and aligned with four methods proved on controls; all sit at the shuffled baseline. The key is open; the route is hand-anchoring from the glosses.',
         quote='1.3 glyphs per letter on a glossed pair &middot; 29 Aug &ldquo;1571&rdquo; is 1572, Alva&rsquo;s Te Deum for St Bartholomew'),
    dict(slug='lanssac', label='Lanssac', year='1573', y=1573, place='Warsaw &rarr; Paris', st='solved', stt='read',
         title='Lanssac to Charles IX, Warsaw, 26 April 1573 &mdash; the Polish election embassy&rsquo;s cipher',
         blurb='BnF fr. 4735 f. 124, catalogued &ldquo;avec chiffre&rdquo; with no decipherment. The key is a homophonic letter cipher with word signs, recovered from a sibling letter whose Court decipherment survives as gutter-cut marginal notes (&ldquo;car je n&rsquo;ay pas cinquante escuz&rdquo;) and checked against the fragments on f. 124 itself. Both passages read: the dangers French travellers meet in Germany, and how, without his Saxon escort, Lanssac would have been detained or stopped on his way to Warsaw. Tomokiyo&rsquo;s published table for the cipher is corrected.',
         quote='&ldquo;j&rsquo;eusse sans doubte pour le moins est&eacute; retenu ou empesch&eacute; de passer oultre&rdquo;',
         rights='Manuscript rights: Biblioth&egrave;que nationale de France'),
    dict(slug='mendoza1589', label='Mendoza 1589', year='1589', y=1589, place='San Lorenzo &rarr; Paris', st='found', stt='resolved',
         title='Philip II to Mendoza, 7 September 1589 &mdash; the &ldquo;second undeciphered letter&rdquo; is the decipherer&rsquo;s copy',
         blurb='BnF fr. 3641 holds both of Philip II&rsquo;s letters of that day twice: the originals in the general cipher Cg.13 and the 1589 decipherer&rsquo;s fair copies, laid out like the originals with the unread code words in the margin, one of them miscatalogued as a second cipher letter. Aligning the pairs rebuilds some seventy syllables and fifty code groups of Cg.13, reads groups the decipherers left blank (respeto, vuestro, negocio) and corrects their &ldquo;Francia&rdquo; to England. Fourteen groups open.',
         quote='&ldquo;dos papeles que se han escapado de [Inglaterra] refieren que salieron de alli en compa&ntilde;ia de Manuel de Andrada, [portugu&eacute;s]&rdquo;',
         rights='Manuscript images: Biblioth&egrave;que nationale de France'),
    dict(slug='hyde', label='Hyde', year='1659&ndash;60', y=1659, place='Brussels', st='found', stt='explained',
         title='Hyde&rsquo;s ciphered superscriptions &mdash; not a cipher at all',
         blurb='The four &ldquo;undeciphered addresses&rdquo; on Hyde&rsquo;s letters to Barwick decode to nothing under the full Hyde&ndash;Barwick key printed in 1721, because, as the 1724 editor states, they were numbers &ldquo;signifying nothing &hellip; only to puzzle the Enemy&rdquo;.',
         quote='&ldquo;some Persons &hellip; have wondered what was the meaning of them&rdquo; &mdash; Life of Barwick, 1724'),
    dict(slug='armstrong', label='Armstrong', year='1808', y=1808, place='United States', st='solved', stt='solved',
         title='Armstrong to Madison &mdash; the coded postscript',
         blurb='Forty-nine groups of the 1,600-element &ldquo;THE = 972&rdquo; diplomatic code, read in full after reconstructing 580 groups from the State Department&rsquo;s own pencil decodes on NARA microfilm M34 roll 13.',
         quote='&ldquo;Russel ought to be the consul: he is an American by birth &hellip; Next to him in fitness is O&rsquo;Mealy, but he is, like Warden, an Irishman.&rdquo;'),
    dict(slug='debosnys', label='Debosnys', year='1883', y=1883, place='Elizabethtown, NY', st='stuck', stt='too short to break',
         title='The Debosnys cryptograms &mdash; a French syllabary, and why it stops there',
         blurb='A convicted wife-killer&rsquo;s invented script, about 1,200 glyphs, unread since he was hanged. Three passages transcribed. The cipher poem is twenty lines of rhyming couplets, and line length and rhyme both make it a syllabary too short for any crib-free attack.',
         quote='final glyph matches in 9 of 10 couplets &middot; 0 of 9 across &middot; planted 1,000-glyph syllabary: 0% recovered'),
    dict(slug='sunyatsen', label='Sun Yat-sen', year='1916', y=1916, place='Swatow &rarr; Tokyo', st='solved', stt='solved',
         title='The Swatow telegram to Sun Yat-sen &mdash; a systematic code condenser',
         blurb='Twenty consonants, five vowels, ten-letter words: a code condenser over the standard Chinese telegraph code. The family of systematic tables is small enough to brute-force, and one key reads 41 characters: Mo Qingyu&rsquo;s independence at Chaozhou and Sun&rsquo;s men ordered out of the Swatow garrison headquarters, 3 April 1916.',
         quote='潮城由莫擎宇獨立。我軍亦光復汕頭。後莫率大隊來，令我退出鎮守府&hellip;'),
    dict(slug='huangxing', label='Huang Xing', year='1916', y=1916.5, place='China / Japan', st='solved', stt='scheme found',
         title='Huang Xing to Lin Hu and Li Genyuan &mdash; a kana condenser',
         blurb='Listed as &ldquo;solved but specific scheme unknown&rdquo;: the Japanese Foreign Ministry filed a decode nobody could read, and an encipherment nobody could name. Both recovered, and then corrected from the frames: three kana carry one character deterministically from a private code, a superfluous kana had hidden the repeats, and the vowel is not free.',
         quote='護國軍能速入湘贛甚好。章行嚴何日東渡？速令出發，並望預電。興　徑'),
    dict(slug='adfgvx', label='ADFGVX', year='1918', y=1918, place='Eastern Front', st='partial', stt='9 of 22 read',
         title='The ADFGVX residue of 1918 &mdash; twenty-two mutilated messages against known keys',
         blurb='Schmeh&rsquo;s Top 50 lists twenty-two German radio messages of November 1918 as unsolved, but the keys were published in 2017 and the messages are garbled in transmission. The comment thread that read nine of them is tabulated for the first time, Lasry&rsquo;s unpublished CHI key is rebuilt, his readers&rsquo; method re-derives the solved pages blind, and the ten never read resist every key and a key-free attack that fails its own control.',
         quote='9 solved &middot; 3 partial &middot; 10 open &middot; best open score &minus;6.9 against &minus;4.4 to &minus;6.0 solved'),
    dict(slug='goldbar', label='Gold bars', year='1933', y=1933, place='Shanghai', st='found', stt='no message',
         title='The Chinese gold bar cryptograms &mdash; ten of everything',
         blurb='Sixteen strings on seven bars said to certify $300,000,000, unread for ninety years. They contain almost exactly ten of every letter of the alphabet: chi-squared 1.25 against uniform where chance predicts 25. No cipher can flatten a distribution past what randomness allows, so there is nothing to read.',
         quote='MQOLCSJTLGAJOKBSSBOMUPCE &middot; ZUQUPNZN &middot; FEWGDRHDDEEUMFFTEEMJXZR',
         rights='Bar photographs from the IACR'),
    dict(slug='roosevelt', label='Roosevelt', year='1935', y=1935, place='Washington', st='found', stt='no message',
         title='The Roosevelt cryptogram &mdash; the numbers 1 to 52, written once each',
         blurb='Three lines of digits above a threat to the President, reproduced by Friedman and unread since 1935. Read at glyph level they are a permutation of 1 to 52 with zero padding; the permutation drifts upward, runs 39 40 41 42 and falls into sixteen rising chains where a shuffle gives 26, the marks of a hand-written list. The ordered-key cipher readings that can be tested fail while matched controls are recovered.',
         quote='16 rising chains against 26 &middot; rank correlation +0.39 &middot; every value once',
         rights='Figure from The Friedman Legacy, NSA 1992, via the Internet Archive'),
    dict(slug='copenhagen', label='Copenhagen', year='c.1950s', y=1955, place='Copenhagen', st='stuck', stt='not a simple substitution',
         title='The Copenhagen cryptogram &mdash; not a simple substitution of any language tested',
         blurb='Three lines found behind an 1835 portrait of a Danish general, 107 characters, unsolved at the American Cryptogram Association since the 1950s. Transcribed twice, attacked in ten languages under six reading conventions; the same solver recovers matched controls at 96 to 100 percent and the note never comes close.',
         quote='best &minus;2.7 nats per letter in any language &middot; controls solve at &minus;1.4 to &minus;2.1'),
    dict(slug='scorpion', label='Scorpion', year='1991', y=1991, place='United States', st='stuck', stt='below unicity distance',
         title='The Scorpion letters &mdash; two ciphers below the unicity distance',
         blurb='Two Zodiac-style cryptograms sent to John Walsh in 1991, 70 and 180 symbols with 53 and 145 distinct. Both carry more key than the English text has redundancy, so fluent false solutions are guaranteed; matched controls produce them at 3 to 13 percent accuracy, and a claimed 2018 solution is tested against the same rule.',
         quote='S5: every repeat at a multiple of 16 &middot; key 682 bits against 576 of redundancy'),
    dict(slug='voynich', label='Voynich', year='c.1420', y=1420, place='Beinecke MS 408', st='partial', stt='adjudicated',
         title='The Voynich manuscript &mdash; hoax, cipher or language, adjudicated',
         blurb='Six computational tests on the transliteration against eleven languages and implemented hoax generators, each re-run adversarially, and five literature sweeps. A plain or simply enciphered European language is excluded on transliteration-robust entropy; a verbose encoding and a structured meaningless text are left roughly even, with the tests that would separate them.',
         quote='h2 2.2&ndash;2.9 bits against a 3.3 floor &middot; slot grammar 1.7&ndash;2.3&times; more rigid than any language'),
    dict(slug='famous', label='The famous ones', year='survey', y=9999, place='Survey', st='partial', stt='the famous ones',
         title='Why the famous ciphers resist',
         blurb='Kryptos, Voynich, Dorabella, Beale, Linear A, Phaistos, the pigeon message. Sorted by the actual reason each has held out: undeciphered writing systems, one that is information-theoretically secure, several too short for any answer to be provable, and at least two that were probably never enciphered.',
         quote='Fame is a poor guide to tractability.'),
]
IMAGES = {'richelieu': None, 'feuquieres': ('feuquieres_p283.jpg', 'Mémoires de Catinat 1819, vol. II p. 283, the ciphered despatch', 'Bayerische Staatsbibliothek'), 'urquhart': None, 'mondoucet': None, 'mendoza1589': ('mendoza1589_f14.jpg', 'BnF Français 3641 f. 14, the copy made by the 1589 decipherer of letter A, with the unread code groups underlined and listed in the margin', 'Bibliothèque nationale de France'), 'catinat1691': ('catinat1691_p320.jpg', 'Mémoires de Catinat 1819, vol. II p. 320, the start of the King\'s letter of 14 September 1691 in figures', 'Bayerische Staatsbibliothek'), 'ormonde': ('ormonde_p28.jpg', 'Page of the Maltravers to Ormonde cipher letter, 1634', 'Ormonde manuscripts'), 'vatican': ('vatican_meister176.jpg', 'Meister 1906, page 176: the Farnese chancery keys of 1539 to 1542, including the last cipher with Poggio', 'Meister, Die Geheimschrift, 1906, via the Internet Archive'), 'lucca': None, 'boswell': None, 'forster': None, 'warsaw': None, 'hyde': ('hyde_p396.jpg', 'Page 396 of the Life of Barwick, 1724, with the ciphered superscription', 'Life of Barwick, 1724'), 'armstrong': ('armstrong_ps.jpg', 'The coded postscript of Armstrong to Madison, 30 August 1808', 'Founders Online'), 'debosnys': ('debosnys_verse.png', 'Debosnys cipher poem in his invented script, 1883', ''), 'sunyatsen': ('sunyatsen_telegram.png', 'The Swatow telegram to Sun Yat-sen, 3 April 1916', 'JACAR'), 'huangxing': ('huangxing_telegram.png', 'Telegram from Huang Xing, 25 May 1916', 'JACAR'), 'adfgvx': None, 'goldbar': ('goldbar_bar.jpg', 'One of the seven Chinese gold bars with its Latin-letter strings', 'IACR'), 'roosevelt': ('roosevelt_fig2.jpg', 'The Roosevelt letter of 1935: three lines of digits, the letter lines, a skull and crossbones and a dagger through a boot', 'The Friedman Legacy, NSA 1992, Internet Archive scan'), 'copenhagen': ('copenhagen_note.jpg', 'The Copenhagen cryptogram: three lines of digits, letters and strokes', 'Scan published by Klaus Schmeh, Cipherbrain, 2015'), 'scorpion': ('scorpion_s1.jpg', 'Scorpion cipher S1, 70 symbols in a 10 by 7 grid, 1991', 'FBI release via Oranchak and Schmeh'), 'voynich': ('voynich_f34r.jpg', 'Voynich manuscript, folio 34r: a herbal page with four paragraphs of Voynichese', 'Beinecke MS 408, public domain, via Wikimedia Commons'), 'famous': None}

GROUPS = [('Solved', lambda p: p['st'] == 'solved'), ('Explained', lambda p: p['st'] == 'found'),
          ('Partly read', lambda p: p['st'] == 'partial' and p['slug'] != 'famous'),
          ('Attempted, not solved', lambda p: p['st'] == 'stuck'), ('Survey', lambda p: p['slug'] == 'famous')]

def nav_html(current):
    items = []
    for gname, pred in GROUPS:
        ps = sorted([p for p in PAGES if pred(p)], key=lambda p: p['y'])
        if not ps: continue
        lis = ''.join(f'<li><a href="{p["slug"]}.html"{" aria-current=\"page\"" if p["slug"] == current else ""}>'
                      f'<span class="st {p["st"]}">{p["stt"]}</span><b>{p["label"]}</b><span class="yr">{p["year"]}</span></a></li>' for p in ps)
        items.append(f'<div class="grp"><h4>{gname}</h4><ul>{lis}</ul></div>')
    return (
        f'<header class="nav"><div class="in">\n'
        f'  <a class="brand" href="index.html"><span class="glyph">972</span><span>{SITE}</span></a>\n'
        f'  <button class="navtoggle" type="button" aria-expanded="false" aria-controls="sitemenu"><span></span><span></span><span></span><i>Menu</i></button>\n'
        f'  <nav id="sitemenu" class="links" aria-label="Site">\n'
        f'    <details class="menu"><summary>Write-ups <svg width="10" height="7" viewBox="0 0 10 7" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></summary>\n'
        f'      <div class="panel">{"".join(items)}</div></details>\n'
        f'    <a href="index.html#recent">Latest</a>\n'
        f'    <a href="catalogue.html"{" aria-current=\"page\"" if current == "catalogue" else ""}>Catalogue</a>\n'
        f'    <a class="ext" href="{REPO}" rel="noopener">Code &#8599;</a>\n'
        f'    <button class="theme" type="button" aria-label="Switch between dark and light" title="Dark / light"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.8a6.2 6.2 0 0 1 0 12.4z" fill="currentColor"/></svg></button>\n'
        f'  </nav>\n</div></header>')

def footer_html(current):
    order = sorted([p for p in PAGES if p['slug'] != 'famous'], key=lambda p: p['y'])
    prev = nxt = None
    for i, p in enumerate(order):
        if p['slug'] == current:
            prev = order[i-1] if i > 0 else None; nxt = order[i+1] if i+1 < len(order) else None
    cur = next((p for p in PAGES if p['slug'] == current), None)
    rights = f' &middot; {cur["rights"]}' if cur and cur.get('rights') else ''
    links = ['<a href="index.html">Overview</a>']
    if prev: links.append(f'<a href="{prev["slug"]}.html" rel="prev">&larr; {prev["label"]} {prev["year"]}</a>')
    if nxt: links.append(f'<a href="{nxt["slug"]}.html" rel="next">{nxt["label"]} {nxt["year"]} &rarr;</a>')
    links.append(f'<a href="{REPO}" rel="noopener">Code &#8599;</a>')
    links.append('<a href="mailto:dnbourdeau@gmail.com" title="dnbourdeau@gmail.com">Contact &#9993;</a>')
    links.append('<a href="#top">Top &uarr;</a>')
    return (f'<footer><div class="in">\n  <span>Daniel Bourdeau, September 2026 &middot; Text released under CC BY 4.0{rights}</span>\n'
            f'  <nav aria-label="Footer">{"".join(links)}</nav>\n</div></footer>')

def toc_html(s):
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', s, re.S)
    if len(heads) < 3: return ''
    links = []
    for hid, inner in heads:
        text = re.sub(r'<span class="num">.*?</span>', '', inner); text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', html.unescape(text)).strip()
        text = text.split(' &mdash; ')[0]
        links.append(f'<a href="#{hid}">{html.escape(text[:48])}</a>')
    return '<nav class="toc" aria-label="On this page"><span>On this page</span>' + ''.join(links) + '</nav>\n'

def card_html(p):
    im = IMAGES.get(p['slug'])
    thumb = f'    <img class="thumb" src="{im[0]}" alt="" loading="lazy">\n' if im else ''
    return (f'  <a class="card{" hasthumb" if im else ""}" href="{p["slug"]}.html">\n' + thumb +
            f'    <div class="eyebrow"><span>{p["place"]} &middot; {p["year"]}</span><span class="st {p["st"]}">{p["stt"]}</span></div>\n'
            f'    <h3>{p["title"]}</h3>\n    <p>{p["blurb"]}</p>\n    <p class="quote">{p["quote"]}</p>\n    <span class="go">read &rarr;</span>\n  </a>\n')

RECENT_VISIBLE = 5      # "Recent findings" on index.html shows this many entries; the rest fold behind the button

def fold_findings(s, n=RECENT_VISIBLE):
    """Rebuild the Recent findings section so the first n <li> are visible and the rest sit in the hidden
    .more block. Entries may be added to either list by hand; this gathers them all in order and re-splits."""
    m = re.search(r'(<h2 id="recent">.*?</h2>\n(?:<p>.*?</p>\n)?)(<ul class="findings">.*?)(?=\n<h2|\n<!-- |\Z)', s, re.S)
    if not m: return s
    items = re.findall(r'<li>.*?</li>', m.group(2), re.S)
    if not items: return s
    head = '<ul class="findings">\n' + '\n'.join(items[:n]) + '\n</ul>'
    rest = items[n:]
    if rest:
        head += ('\n<div class="more" hidden><ul class="findings">\n' + '\n'.join(rest) + '\n</ul></div>\n'
                 f'<button class="showmore" type="button" data-target="findings">Show {len(rest)} earlier finding{"s" if len(rest) != 1 else ""}</button>')
    return s[:m.start(2)] + head + s[m.end(2):]

SHARED_INLINE = ('.why', '.w-yes', '.w-no', '.w-lang', '.w-otp', '.w-short', '.w-fake', '.w-open', '.item', '.item h3', '.item .meta2', '.ct', '.callout', '.callout h3', '.tw')

def process(path):
    slug = path.stem
    s = path.read_text(encoding='utf-8')
    if s.startswith('﻿'): s = s[1:]
    nav = nav_html(slug)
    if '<!-- site:nav -->' in s: s = s.replace('<!-- site:nav -->', nav, 1)
    else: s = re.sub(r'<header class="nav">.*?</header>|<nav class="nav">.*?</nav>', lambda m: nav, s, count=1, flags=re.S)
    s = re.sub(r'(</div></header>)(\s*</div></header>)+', r'\1', s)      # stray closers left by an earlier build
    foot = footer_html(slug)
    if '<!-- site:footer -->' in s: s = s.replace('<!-- site:footer -->', foot, 1)
    else:
        ms = list(re.finditer(r'<footer.*?</footer>', s, re.S))
        if ms: m = ms[-1]; s = s[:m.start()] + foot + s[m.end():]
        else: s = s.replace('</main>', '</main>\n' + foot, 1)
    # give every h2 an id so the contents strip and deep links work
    used = set(re.findall(r'<h2 id="([^"]+)"', s))
    def add_id(m):
        text = re.sub(r'<span class="num">.*?</span>', '', m.group(2)); text = html.unescape(re.sub(r'<[^>]+>', '', text))
        base = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:40] or 'section'
        hid = base; k = 2
        while hid in used: hid = f'{base}-{k}'; k += 1
        used.add(hid); return f'<h2 id="{hid}"{m.group(1)}>{m.group(2)}</h2>'
    s = re.sub(r'<h2((?![^>]*\bid=)[^>]*)>(.*?)</h2>', add_id, s, flags=re.S)
    # contents strip
    s = re.sub(r'<nav class="toc".*?</nav>\n*', '', s, flags=re.S)      # also eat blank lines an earlier build left
    if slug != 'index':
        toc = toc_html(s)
        if toc: s = re.sub(r'<main>\n*', lambda m: '<main>\n' + toc, s, count=1)
    # lead figure: pages that have an image in the manifest but no figure of their own get one after the contents strip
    im = IMAGES.get(slug)
    s = re.sub(r'<figure class="lead">.*?</figure>\n?', '', s, flags=re.S)
    if im and '<figure' not in s:
        cap = im[1] + (f'. {im[2]}.' if im[2] else '.')
        fig = f'<figure class="lead"><img src="{im[0]}" alt="{im[1]}"><figcaption>{cap}</figcaption></figure>\n'
        if '<nav class="toc"' in s:
            s = re.sub(r'(<nav class="toc".*?</nav>\n)', lambda m: m.group(1) + fig, s, count=1, flags=re.S)
        else:
            s = s.replace('<main>', '<main>\n' + fig, 1)
    # drop inline style blocks made of shared rules only
    def strip_style(m):
        rules = re.findall(r'([^{}]+)\{', m.group(1))
        if rules and all(r.strip() in SHARED_INLINE for r in rules): return ''
        return m.group(0)
    s = re.sub(r'<style>(.*?)</style>\s*', strip_style, s, flags=re.S)
    # versions, anchor for "Top", script
    s = re.sub(r'<link rel="stylesheet" href="style.css[^"]*">', f'<link rel="stylesheet" href="style.css?v={VERSION}">', s)
    if 'href="style.css' not in s: s = s.replace('</head>', f'<link rel="stylesheet" href="style.css?v={VERSION}">\n</head>', 1)
    s = re.sub(r'<script src="site.js[^"]*"></script>\s*', '', s)
    s = s.replace('</body>', f'<script src="site.js?v={VERSION}"></script>\n</body>', 1)
    s = re.sub(r'<body(?![^>]*id=)', '<body id="top"', s, count=1)
    if slug == 'index':
        s = fold_findings(s)
        FEATURED =['catinat1691', 'voynich', 'feuquieres', 'armstrong', 'lucca', 'warsaw', 'richelieu', 'sunyatsen']
        feat = [next(p for p in PAGES if p['slug'] == f) for f in FEATURED]
        rest = sorted([p for p in PAGES if p['slug'] not in FEATURED], key=lambda p: ({'solved': 0, 'found': 1, 'partial': 2, 'stuck': 3}[p['st']] if p['slug'] != 'famous' else 4, -p['y']))
        rows = ''.join(f'  <li><a href="{p["slug"]}.html"><span class="st {p["st"]}">{p["stt"]}</span><span class="t">{p["title"]}</span><span class="yr">{p["year"]}</span></a></li>\n' for p in rest)
        cards = ('<!-- cards:start -->\n<div class="cards">\n' + ''.join(card_html(p) for p in feat) + '</div>\n'
                 '<h3 class="listhead">And the rest</h3>\n<ul class="list">\n' + rows + '</ul>\n<!-- cards:end -->')
        if '<!-- cards:start -->' in s:
            s = re.sub(r'<!-- cards:start -->.*?<!-- cards:end -->', lambda m: cards, s, flags=re.S)
        else:
            s = re.sub(r'(<h2(?: id="writeups")?><span class="num">01</span> Write-ups</h2>\s*)<div class="cards">.*?</div>\n(?=\n<h2)', lambda m: m.group(1) + cards + '\n', s, count=1, flags=re.S)
    path.write_text(s, encoding='utf-8')
    return slug

if __name__ == '__main__':
    done = [process(p) for p in sorted(HERE.glob('*.html'))]
    print('built', ', '.join(done))
