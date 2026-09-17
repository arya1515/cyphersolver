# cyphersolver

An informal benchmark of a frontier AI (Claude Fable 5.1) on historically "unsolved" ciphers, as much a hobby as a
measurement. The targets
are drawn from three standard lists: S. Tomokiyo's
[Unsolved Historical Ciphers](https://cryptiana.web.fc2.com/code/unsolved.htm), Klaus Schmeh's
[Top 50 unsolved encrypted messages](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/),
and Elonka Dunin's [famous unsolved codes](https://elonka.com/UnsolvedCodes.html). Each one is a test of how far an AI
assistant, working with a human, can get on a problem that has resisted people for decades or centuries: how much is
archival research, how much is cryptanalysis, and where it stops. Method: archival research, historical cribs,
19th-century printed editions, and small purpose-built solvers, always run against matched controls so that a
negative result says something.

- **Website:** https://dbourdeau.github.io/cyphersolver/ — hub, priority queue, and formal write-ups (source in [`docs/`](docs/)).
- **Tracker:** [TARGETS.md](TARGETS.md) — every list entry ranked by feasibility, with status, evidence and next step.
- **Solved, ranked:** [SOLVED_RANKING.md](SOLVED_RANKING.md) — the finished targets scored by difficulty, historical weight, novelty, research effort, profile and verification.
- **Catalogue of new targets:** [CATALOGUE.md](CATALOGUE.md) — 25 undeciphered letters, 1497–1610, absent from the standard lists, harvested from the BnF catalogue on Gallica and from the fine print of the cryptiana articles; shelfmarks, arks, prior art, difficulty class. Unvalidated on the leaves except fr. 16127.
- **Per-target record:** each working directory has a `NOTES.md` with sources, dead ends, what is established and what is inferred.

## Results

### Solved

| Target | Date | Result | Where |
|---|---|---|---|
| Richelieu → M. de Rancé, BnF Français 3829 ff. 87 & 89 | 1629 | Homophonic alphabet and nomenclature recovered ciphertext-only; later matched word for word to Avenel (1858), which the catalogues missed | [`richelieu/`](richelieu/) · [write-up](https://dbourdeau.github.io/cyphersolver/richelieu.html) |
| Armstrong → Madison, coded postscript ("THE = 972" code) | 1808 | 49/49 groups read; 580-group code table reconstructed from NARA pencil decodes | [`armstrong/`](armstrong/) · [write-up](https://dbourdeau.github.io/cyphersolver/armstrong.html) |
| Swatow telegram to Sun Yat-sen (JACAR B03050738800) | 1916 | Systematic code condenser over the standard telegraph code recovered by brute force; 41 of ~44 characters read | [`sunyatsen/`](sunyatsen/) · [write-up](https://dbourdeau.github.io/cyphersolver/sunyatsen.html) |
| Huang Xing → Lin Hu and Li Genyuan (JACAR B03050731500) | 1916 | Scheme identified: three kana per character, consonant row carries the digit, vowel free; plaintext read from the JACAR frames | [`sunyatsen/HUANG_NOTES.md`](sunyatsen/HUANG_NOTES.md) · [write-up](https://dbourdeau.github.io/cyphersolver/huangxing.html) |
| Maltravers → Ormonde | 1634–35 | Regular block alphabet and nulls recovered from 59 figures; every spelled word reads; the nomenclator then confirmed clause for clause against Wentworth's dispatches in Knowler's *Strafforde's Letters* (1739). Two person-codes in one clause remain unidentified | [`ormonde/`](ormonde/) · [write-up](https://dbourdeau.github.io/cyphersolver/ormonde.html) |
| Fra Giovanni di Lucca → Ferdinand III, 30 May 1644 (DECODE R2159, ÖStA HHStA) | 1644 | Read in full from Tomokiyo's transcription: a 24-figure Italian alphabet with two polyphonic figures (17 = i/n, 19 = t/s), found by annealing from the eight consistent crib letters, all seeds agreeing and shuffled controls failing; Viterbi over the alternatives reads the 231 groups end to end. An offer to keep the Turk off Rákóczi, raise Moldavia against him and supply 2,000 Cossacks. Needs the images for three odd spellings and the speaker's name | [`lucca/`](lucca/) · [write-up](https://dbourdeau.github.io/cyphersolver/lucca.html) |
| Warsaw, 24 Dec 1627, to the Bishop of Olmütz? (DECODE R1408, ÖStA HHStA) | 1627 | Read in full from Tomokiyo's transcription: a homophonic substitution whose alphabet turns out to be in plain order (odd figures a–m, even figures n–z), with letter pairs for consonants, a dozen two-figure syllables, the letters *a m* as nulls and thirteen word codes. A 5-gram + dictionary annealer converged from random and seeded starts, shuffled controls failing. The writer, back in Warsaw from Nikolsburg, presses for a promised canonry of Olmütz for one of the Queen of Poland's sons. Word codes glossed from context only; needs the image and the key fascicle | [`warsaw/`](warsaw/) · [write-up](https://dbourdeau.github.io/cyphersolver/warsaw.html) |
| Henry of Navarre → Ségur, BnF 500 de Colbert 401 ff. 233, 239, 288v (listed as Henry III) | 1585–86 | Three figure-cipher letters to the envoy raising a German army, read from the Gallica images. The upper figures fall into blocks of five (mod 5 test), an alphabetical syllabary; a structured annealer with the letters' clear French as context recovered a key that is alphabetical on its own (a 4–6 … u 45–47, x y z, et, null; syllables ba–vu 54–123; doubles ée ll ss), 97 % on a matched control. Conclude with Duke Casimir, raise the largest levy and march it; Clervant's two thousand reiters; the Vivarais or Dauphiné road. Word-signs partly glossed; f. 143 (1583) is another key. The whole volume swept: one more cipher leaf, f. 366 (autograph, same key, mostly names), and f. 333 read with Tomokiyo's sibling key, which is this key shifted by eight | [`segur/`](segur/) · [write-up](https://dbourdeau.github.io/cyphersolver/segur.html) |
| Charles I and Nicholas → Boswell, TNA SP 84/157 ff. 217, 219 | 1643 | Alphabet solved by R. Pitt (Sept 2026): a 24-letter row repeated four times over 20–115, plus supplementary homophones and nulls; verified here against a 20,000-row permutation control (z = 9.6). Added here: the four graphic signs read as word-signs introduced inline (good, Cousin, Master, us), which closes the framed passages; the King's letter is to the Duke of Courland's envoy, sent via Boswell with the re-credentials Simpson printed in 1893; Nicholas's letter concerns the Dutch embassy of 1644. Both letters read in substance; a dozen single-occurrence word codes remain, and the transcription needs the folios | [`boswell/`](boswell/) · [write-up](https://dbourdeau.github.io/cyphersolver/boswell.html) |
| Sir Richard Forster, 13 May 1644 (Val-d'Oise 68.H.8) | 1644 | Found already read: George Lasry, Norbert Biermann and R. Pitt (Sept 2026) had the key; Tomokiyo's page still says unsolved. Here: permutation control z = 8.8, and a blind recovery of 31 of 34 symbols from the 207 tokens once the word boundaries are used and the French model writes *u* for *v*, *i* for *j*; six matched controls read. Not a regular Stuart key but a mixed homophonic alphabet. Four slips need the manuscript | [`forster/`](forster/) · [write-up](https://dbourdeau.github.io/cyphersolver/forster.html) |
| Louvois and Louis XIV → Catinat, seven despatches, 8 July – 14 Sept 1691 (Mémoires de Catinat 1819, t. II pp. 295–342) | 1691 | 12,362 groups of the Grand Chiffre de 1691 decoded in full with Bazeries' 1893 table from the MDZ hOCR of the volume, checked against the page images; the two letters Bazeries printed in clear agree at 98.1 % and 99.1 % of characters, and the other five (9 July, 24 and 29 Aug, 6 and 14 Sept; about 9,700 groups) are read for the first time in print. The 14 Sept letter is the King's decision to bring the army back over the Alps, fight defensively in the passes in 1692, hold Carmagnole to cover the negotiation with the Pope and then burn it, and take Coni in winter. Six groups misprinted above 587 in 1819 stay unread | [`catinat1691/`](catinat1691/) · [write-up](https://dbourdeau.github.io/cyphersolver/catinat1691.html) |
| Urquhart's Cyphral Octastich, The Jewel (1652), last leaf | 1652 | Book cipher on the book itself: number k → first word of the needed initial on physical page k; verified from EEBO-TCP A95749 and a new 285-number transcription from the 1983 edition's photographs (HCPortal), without the plaintext Vals AI published in Aug 2026: 238/284 first-occurrence hits vs 0.43 shuffled and random-page controls. A royalist prayer for Charles II in ottava rima, *Great Lord, mantaine that regal familie … Our Emperour, King, Monarch and Protector. Amen, so be it.* Ten letters of line 5 unread (TCP text defect at pp. 149–158). Distich (Works 1834 p. 417): Proquiritation rule 34/64, chance, no English; open | [`urquhart/`](urquhart/) · [write-up](https://dbourdeau.github.io/cyphersolver/urquhart.html) |
| Feuquières → Catinat, Pignerol (418-group two-part "petit chiffre") | 1691 | **Read** (16 Sept 2026): the code is the petit chiffre of the Pignerol governors, companion of Bazeries' Grand Chiffre de 1691 (table transcribed from Gallica and verified on four 1690-91 despatches). A second letter in the same code, Louvois to d'Herleville of 6 Sept 1690, sits in the 1819 Mémoires t. I with its contemporary translation; the two letters share 72 groups, and hand alignment carried between them reads 586 of 601 tokens. Feuquières fixes the Veillane surprise: ready on receipt of Catinat's letter of the 24th, the enemy will not defend seriously, two roads into Avigliana (the faubourg and the houses along the pond), 80 horse to Saint-Ambroise, attack at two points, keep the dragoons from escaping. First reading since Bazeries' unpublished one of 1893 | [`feuquieres/`](feuquieres/) |
| Lanssac → Charles IX, Warsaw, 26 Apr 1573, BnF fr. 4735 no. 51 f. 124, and the siblings ff. 160, 164, 174 (catalogue item 3, class A) | 1573 | **Read** (17 Sept 2026): both cipher passages of f. 124 (96/100 signs) from the Gallica images; homophonic letter cipher with word signs, key fixed from the glossed sibling f. 154v ("car je n'ay pas cinquante escuz"), the gutter-cut marginal fragments, and a pinned annealer with shuffled and blind controls. The key then reads the three election letters whose "déchiffrement" is only that cut gloss: 1 May to the King, *ceste nation est autant vénale et sujette à se laisser gaigner par argent comme sont les Allemans*; 1 May to Anjou, *l'Empereur en y a despendu plus de trois cens mil … faisant le pis qu'il peult contre vous*; 9 May from Płock, the election carried *contre la volunté et menées du Grand Seigneur, de l'Empereur, des princes de l'Empire, du Roy d'Espaigne, du Moscovite et du Roy de Suède, qui tous estoient bandez contre vostre Majesté*. Tomokiyo's table for the cipher corrected. Short runs unread, flagged | [`lanssac/`](lanssac/) · [write-up](https://dbourdeau.github.io/cyphersolver/lanssac.html) |
| Philip II → Mendoza, two letters of 7 Sept 1589, BnF fr. 3641 ff. 10/14 and 12/76 (catalogue item 32, "second undeciphered letter") | 1589 | **Resolved** (17 Sept 2026): the "second letter" (f. 14) is the 1589 decipherer's fair copy of the Cg.13 original on f. 10, laid out like the original with the unread nomenclator groups underlined and listed in the margin; f. 76 is the same for the other letter (f. 12), miscatalogued by Omont. Both pairs aligned group by group: a partial table of Philip II's general cipher Cg.13 (some 70 syllables in rows of five, three ending marks, c. 50 code groups), consistent with Tomokiyo's published fragment at every overlap. Cross-reading the letters reads groups the decipherers left blank (pur respeto, mes vuestro, san negocio; bur persona, dom dicho, dur porque, pen mucho from Phelippes's interlinear f. 5), shows tur to be a miscopy of tum, and corrects the copyist's "Francia" for dun (England: the fleet's return, "entre ellos y el de Bearne", "sus armaçones") and "si se hiziesse" for the King's "si yo hiziesse". Fourteen groups in the two letters still unread; the Simancas table (Devos 1950) would close them | [`mendoza1589/`](mendoza1589/) · [write-up](https://dbourdeau.github.io/cyphersolver/mendoza1589.html) |

### Explained: not a cipher, or nothing to read

| Target | Date | Finding | Where |
|---|---|---|---|
| Hyde's ciphered superscriptions | 1659–60 | Dummy numbers "only to puzzle the Enemy", per the 1724 editor and the full Hyde–Barwick key of 1721 | [`hyde/`](hyde/) · [write-up](https://dbourdeau.github.io/cyphersolver/hyde.html) |
| Chinese gold bar cryptograms, Shanghai | 1933 | Almost exactly ten of every letter; flatter than any cipher of a real text can be. No message | [`goldbar/`](goldbar/) · [write-up](https://dbourdeau.github.io/cyphersolver/goldbar.html) |
| Roosevelt cryptogram, number block | 1935 | A permutation of 1 to 52, each once, padded with zeros; its statistics are those of a list written by hand, and the testable ordered-key cipher readings fail while matched controls succeed. Ernst's 2017 doodle claim confirmed. No message | [`roosevelt/`](roosevelt/) · [write-up](https://dbourdeau.github.io/cyphersolver/roosevelt.html) |
| D'Agapeyeff challenge cipher | 1939 | The ciphertext is not enciphered English | [`dagapeyeff/`](dagapeyeff/) |
| Beale Paper no. 1 | 1885 | Fabrication; evidence in notes, book-cipher scan over Gutenberg negative | [`beale/`](beale/) |

### Partly read or adjudicated

| Target | Date | Result | Where |
|---|---|---|---|
| Jean du Bellay → Montmorency, London, the ciphered letters of 1529, BnF fr. 3078 nos. 3, 4, 5, 17, 19 and fr. 3077 nos. 18, 20, 23 (catalogue item 4) | 1529 | **Identified and partly read** (17 Sept 2026): the notice hides the years; all eight are 1529, and six were read at the Court and printed in clear by Le Grand (1688), so the catalogue's 'no decipherment' is inventory language. The 22 June letter carries the decipherer's interlinear reading over every sign, from which the key (Tomokiyo's 'Bayonne's Cipher 1529'; Friedmann's NAF 4206 no. 5) was re-derived on the leaf with additions (B = o; word signs *bien*, *fault*, *paix*). Two texts were never read: the whole cipher block of **16 June 1529** (fr. 3078 p. 21, DECODE 'non-decrypted'), read here in stretches — *semblant [que] madame ne fust … pour conclure … la [name] luy ayt par[lé] … [il] fault envoyé querir pouvoir, il ne fauldroyt oublyer a le faire* — about 60 % of the signs; and the opening of **22 Oct 1529** (fr. 3077 no. 23), 'non déchiffré' in Le Grand and Brewer, not yet fetched. The 1528 letters are all in clear in Bourrilly 1905. Scheurer 1969 unchecked | [`dubellay/`](dubellay/) |
| Henri IV → Béthune (Rome), 9, 10 and 22 Nov 1601, BnF fr. 3484 nos. 7, 8, 12 (catalogue item 22, class A) | 1601 | **10 Nov read, key largely recovered** (17 Sept 2026): the notice's "copie du n° précédent" (f. 36) is the minute of the 10 Nov letter in clear; EM alignment of cipher and minute, with the marginal decipherments of 8 Nov and 10 Dec, gives a Villeroy-office key of the design Bazeries printed for Béthune's brother in 1599 (letters with homophones, dotted/comma letters for words, two-digit figures for names: 48 Cardinal, 17 Aldobrandin, 7 le Roy d'Espagne). Ten thousand écus to Cardinal Aldobrandini for the Peace of Lyon and ten thousand more promised, "sans avoir esgard à l'arrest obtenu par lad. duchesse de Nemours". The 9 Nov letter (one page in cipher) reads about half with a lexicon decoder; 22 Nov open. Next: 4× retranscription and the later glosses for the names | [`bethune/`](bethune/) · [write-up](https://dbourdeau.github.io/cyphersolver/bethune.html) |
| Nevers → Pisany, 8 Sept and 14 Oct 1593, BnF fr. 3985 f. 209 and fr. 3986 f. 168 (catalogue item 21; the seven "lettres avec chiffre" to Revol and Pisany) | 1593 | **Two of seven read** (17 Sept 2026). Tomokiyo's Nevers cipher no. 46 (fr. 3995 f. 87, read from the full-resolution Gallica image; two-digit alphabet with homophones, barred/plain/dotted word lists, 1 as an intercalated null, checked against the office's decipherment of a Gondi letter in the same key) resolves every figure of both Pisany letters: 8 Sept reads whole ("l'on dissuadoit [le Roy] de rechercher [que le Pape] luy donnast l'absolution … qu'il n'estoyt besoin qu'il allast sans cela, parce qu'il ne feroit rien … l'on n'a volonté de contanter le Pape, que l'on n'y aille poynt"), 14 Oct in long stretches. The five letters to Revol are in the Court's symbol cipher no. 60, not no. 46: the 27 Aug copy is in clear, the 9 Oct copy has c. 90 symbols, three not reached on the image | [`nevers1593/`](nevers1593/) |
| Voynich manuscript (Beinecke MS 408) | c.1404–38 | Plain or simply enciphered European language excluded on transliteration-robust entropy; verbose encoding vs structured meaningless text left roughly even, with the separating tests named | [`voynich/`](voynich/) · [write-up](https://dbourdeau.github.io/cyphersolver/voynich.html) |

### Found already solved by others (the lists are stale)

| Target | Date | Solved by | Where |
|---|---|---|---|
| ADFGVX messages, Eastern Front | 1918 | Keys published by Lasry, Niebel, Kopal and Wacker; the 22 "unsolved" residue is garbled in transmission. The 2017 thread consolidated: 9 solved, 3 partial, 10 open; Lasry's sixteenth key rebuilt; Norbert's method reimplemented and re-derives 7 pages blind; the 10 open ones resist 15 keys and a key-free attack that fails its own control | [`adfgvx/`](adfgvx/) · [write-up](https://dbourdeau.github.io/cyphersolver/adfgvx.html) |

Six further list entries turned out to be solved by others with nothing to add here: Perwich 1670 (Brown; Lasry, Biermann and Tomokiyo, 2025), Ferdinand III and the Cardinal-Infante (Ernst, 2017), the Milroy telegrams (Bean, 2026), the Feynman ciphers 2 and 3 (2023), the Confederate Navy dictionary code (2026) and the Mazarin–Bordeaux letter of 1654 (Lasry, 2025). They are not counted in the results above; the directories `perwich/`, `ferdinand3/`, `milroy/`, `feynman/` and `barney/` hold only the pointer to the published solution.

### Attempted and closed from the evidence

Each of these was attacked with solvers validated on matched controls of the same length and design. The controls solve;
the target does not, and the notes say why.

| Target | Date | Why it stops | Where |
|---|---|---|---|
| SP 53/16 nos. 78-79 and SP 53/22 f. 52 (Mary Queen of Scots papers residue) | 1585 | Symbol ciphers of the Paris-Rheims exile network in Tomokiyo's glyph-label transcription, 507 and 644 groups. Second session: the two letters share one key (10 of the 20 commonest symbols in common, 2.9 expected), so they pool to 1151 tokens; third session: a numba pipeline now reads clean 507- and 1151-token controls (and a 507-token control with word-signs), yet no. 78 shows no language basin in English, French, Latin, Italian or Spanish, no. 79 sits at random level, and pooling scores worse than either letter, so the same-key claim is withdrawn; a nulls-plus-nomenclator control is not read at this length, so that design stays open. f. 52 (84 tokens) is below unicity. Needs the images and the SP 53/22 keys | [`sp53/`](sp53/) |
| Regent Moray → John Wood, Add MS 32091 f. 213 (134 groups, 32 symbols) | 1568 | Homophonic alphabet in Scots on the face of it, and a 5-gram Scots annealer reads 5 of 6 matched 134-letter controls, but the target gives no reading in Scots, English, French or Latin; no null, separator or crib is supported. The catalogue says the passage is Border news, i.e. names, and 13% of genuine Scots windows score below the solver's false optimum, so the result is undetermined rather than excluded. Needs the page (BL offline) or a second letter in the cipher | [`moray/`](moray/) |
| Louis XIV → duc de Chaulnes, Rome (300-group one-part code) | 1690 | Ciphertext verified from the page images and the code's ten-column Croissy design established, but 300 groups do not determine a 116-entry nomenclator: the annealer recovers 4-12% of a matched control and wrong keys score within noise of the true one. No printed plaintext found. Needs the minute in AE Rome Corr. 331-332 | [`chaulnes/`](chaulnes/) |
| Bordeaux → Brienne, London, 30 May 1653 (Thurloe intercept, BL Add MS 4200 f. 88; 810 tokens, 156 symbols) | 1653 | Identified as a Brienne-office cipher of the 1651-54 family, in which consecutive numbers run through the syllabary alphabetically across diacritic series (cf. Lasry's 1654 Mazarin-Bordeaux key). A solver using that order as a hard prior reads matched 810-token controls to 99 %, but the real text never leaves the failed-seed level over 21 seeds; the rival reading of the symbol classes is unsolvable even on its control. Plaintext not in print (Thurloe SP, Guizot). The English key of 1653 for "Mr. Bordeaux" sits in BL Add MS 32263 f. 1 (DECODE R7537, login) | [`bordeaux/`](bordeaux/) |
| Armstrong → Madison, 20 Feb 1808 (unique code, 369 groups to 1900, plus shorthand-like symbols) | 1808 | Adjudication of the AFIO contest solution (May 2025): the 56-entry key covers 36 % of the groups, leaves 93 of its own 133 mapped occurrences unread, rests on five numbers absent from the letter, and fits its sentence worse than a key built by the same procedure on a shuffled ciphertext. Madison himself wrote in May 1808 that no such cipher was in the office, and the roll-13 pencil decodes are all THE=972, so they cannot supply it. The claim does not hold; the letter stays unsolved | [`armstrong/`](armstrong/) |
| Doge Cicogna and Senate → Giovanni Mocenigo in France, subscribed Marco Ottobon, 27 Apr 1589 (BNE Mss/994 ff. 35-38; 1,528 tokens, 196 symbols) | 1589 | Folios obtained from BNE Digital (130 dpi) and transcribed at first pass, about 70 % reliable per token. The letter is partly in clear: the Lyon postmaster forwarded only a few lines of the dispatch of 28 March, the rest and three other letters were intercepted, hence the cipher. Design: base letters a c d f g h with figures 1-99, letters, syllables and words mixed, the 1577-78 *Zifra Prima* type (not Franceschi's N.11, whose alphabet is confined to 1-20). Letter-only and letter-plus-wildcard annealers fail matched synthetic controls (0-9 % recovery even without transcription noise), so nothing is read. Route: the key sheets DECODE R1789/R1790, the register copy in ASVe Senato Secreta 1589, or a 300-dpi scan | [`ottobon/`](ottobon/) |
| Vatican Challenge Part 5 (Farnese → Poggio) | 1542 | Identified as an Antonio Elio polyphonic-syllabic cipher; Meister key 176/2 verified from the scan and excluded; letter-, lattice- and unit-level attacks fail against controls. Needs the DECODE images or the key | [`vatican5/`](vatican5/) · [write-up](https://dbourdeau.github.io/cyphersolver/vatican.html) |
| Debosnys cryptograms | 1882–83 | Cipher poem is rhyming couplets in a French syllabary, too short for any crib-free attack | [`debosnys/`](debosnys/) · [write-up](https://dbourdeau.github.io/cyphersolver/debosnys.html) |
| Copenhagen cryptogram | c.1950s | Two transcriptions, ten languages, six reading conventions; not a simple substitution of any language tested | [`copenhagen/`](copenhagen/) · [write-up](https://dbourdeau.github.io/cyphersolver/copenhagen.html) |
| Scorpion letters S1 and S5 | 1991 | Below the unicity distance for a homophonic key; controls produce fluent false solutions. The 2018 claim tested | [`scorpion/`](scorpion/) · [write-up](https://dbourdeau.github.io/cyphersolver/scorpion.html) |
| Charles I, Isle of Wight letters | 1648 | Two letters still unread; two candidate keys newly excluded | [`charlesi/`](charlesi/) |
| Berthier → Napoleon; letter to Marmont | 1807–12 | Neither attackable from the single printed source (Vilcoq 1969) | [`napoleon/`](napoleon/) |
| Catokwacopa advertisements | 1875 | Readings audited: which the letters force, which are guesses | [`catokwacopa/`](catokwacopa/) |
| Kaliningrad bottle post | found 2015 | Blocker is transcription from two photographs, not cryptanalysis | [`kaliningrad/`](kaliningrad/) |
| Thomas Urquhart's encrypted poems | 17th c. | Provenance objection to the Aug 2026 claim checked independently | [`urquhart/`](urquhart/) |
| Zhongshan telegrams | c.1938 | No corpus exists online; the premise of the list entry was wrong | [`zhongshan/`](zhongshan/) |
| Koehler cryptograms (Abwehr) | 1944 | Five short letter-cipher messages; skipped as intractable | [`abwehr/`](abwehr/) |
| WW2 censorship-manual steganograms | 1940s | Blocked on image resolution; TNA's digital copy is the same scan | [`censorship/`](censorship/) |
| Lodovico Birago → Duke of Nevers, Saluzzo 13 Nov 1571 (BnF fr. 3251 f. 119) | 1571 | Glyph-level transcription from Gallica: 483 digits, 16 marked digits, 9 inline wavy signs, 6 null letters. Variable-length prefix and suffix codes excluded against controls; the only consistent design is two-digit letters with one- or two-digit marked code groups (75 pairings, 228 tokens over 62 symbols), and at that homophony the annealer fails matched controls, so the target's negative is the method's limit; polyphonic single figures (Lucca-type) excluded with a method that reads its control 3/3; no sibling letter in the volume. Needs a sibling letter or a crib | [`birago/`](birago/) |
| Colbert passages (Mélanges Colbert) | 1665–75 | Read from the Gallica images: the Charost letter (Calais, 3 July 1675, not 1673) and the Gravel–Maulevrier copy (Mainz, 1674) are one key, Maulevrier's, 106 plain figures 52–489 between them. The printed catalogue located all 22 other Charost letters online and both Maulevrier letters: every one in clear. A monotone annealer reads matched controls of both strict alphabetical designs this office used and fails the target under each; looser designs fail their own controls. Probably a word nomenclator; needs the key or a clear copy of the news | [`colbert/`](colbert/) |
| Thurloe State Papers intercepts | 1653–56 | Four short pieces, all period keys fail | [`thurloe/`](thurloe/) |
| D'Estaing → Gérard | 1779 | 217 tokens of a 600-code with no key material; needs the archive copy | [`destaing/`](destaing/) |
| Le Tellier → Castelnau | 1657 | Too short for an unconstrained syllabic solve | [`letellier/`](letellier/) |
| Henry III → Ségur | 1583–86 | Blocked on Gallica access; the sibling cipher's design is known | [`segur/`](segur/) |
| Mondoucet → Charles IX, Brussels 13 July 1572, and the c. 20-letter cipher corpus of BnF fr. 16127 (Gallica sweep find, on no list) | 1571–74 | The volume swept entire: Mondoucet's despatches from the Low Countries arrive in one cipher (letter-forms in variants, figures, ~20 signs) and carry the Court's decipherments, except 13 July 1572. Two verbatim pairs (29 Aug 1572 with f. 9; 16 July 1572 with f. 64, glossed word by word on the leaf) transcribed by hand and by glyph clustering; four aligners, each validated on synthetic controls, sit at the shuffled baseline; 1.3–1.4 glyphs per letter even on the glossed pair, and the 1573 marginal readings are abridged. Key open; route is hand-anchoring from the f. 62r glosses | [`gallica_sweep/`](gallica_sweep/) · [write-up](https://dbourdeau.github.io/cyphersolver/mondoucet.html) |
| Cardinal de Joyeuse → Villars, Rome, 15 Feb 1594 (500 Colbert 33 f. 539) | 1594 | Transcribed from Gallica: 358 tokens in three layers (81-sign homophonic alphabet, 48-sign marked syllabary, 29 code numbers); not Lasry's Senecey key from the same volume; the letter-layer anneal recovers 2-18 % of three matched controls and the target's seeds disagree | [`joyeuse/`](joyeuse/) |
| Cocquet → Mangot, Rome, Nov 1616 (Clairambault 369 f. 317) | 1616 | Gate check: ~160 letter-shaped glyphs in nine runs inside clear French; none of the five period keys from the same volumes matches; du Croc regime | [`cocquet/`](cocquet/) |
| Blancmesnil → Nevers (fr. 3633 f. 24) | 1589? | No ciphertext online: fr. 3633 is not digitised (the source page's catalogue link goes to fr. 4736); the Potier-Nevers key of 1589 is the candidate once a copy exists; sibling letters with decipherments sit in fr. 3616/3621 (DECODE R9434-9448, images restricted) | [`blancmesnil/`](blancmesnil/) |
| 1520s superscript-digit ciphers | 1526–29 | Blocked: DECODE and BL images need login | [`superscript/`](superscript/) |

### Offline only

Nothing more can be done online; the key or the text is located in an archive.

| Target | Date | What is needed | Where |
|---|---|---|---|
| Charles II → Duke of Hamilton | 1650 | Copy order for NRS GD406/1/2197 (open) | [`hamilton/`](hamilton/) |
| Maurice → Rupert; royalist intercepts, BL Add MS 72438 | 1645–46 | BL volumes digitised but offline since the 2023 cyber-attack | [`rupert/`](rupert/) |
| Stepney → Manchester, Vienna | 1702 | Stepney's office cipher in TNA SP 105/106 or BL Add MSS 7058–78 | [`stepney/`](stepney/) |
| Torcy → Geertruidenberg plenipotentiaries; Villars → Polignac (BL Add MS 61575) | 1710 | The ciphertext itself: Tomokiyo's transcription files are dead links, DECODE R8755/R8756 need a login, the BL volume is not digitised | [`geertruidenberg/`](geertruidenberg/) |
| Marco Ottobon → Giovanni Mocenigo, BNE Mss/994 ff. 34–38 | 1589 | One browser session: the manuscript is digitised (BNE Digital oid 0000174344; DECODE R2252, nine openings) but bne.es sits behind a Cloudflare Turnstile check that blocks scripts and automated browsers, and DECODE needs a login. About 6.5 pages of letter-plus-figure Venetian cipher, est. 2,500–4,000 tokens; the 1578–87 *zifra granda* syllabary is transcribed as a candidate key and the structural tests are written | [`ottobon/`](ottobon/) |

### In progress

| Target | Date | State | Where |
|---|---|---|---|
| "BLUME SALAMANCA" telegrams, Zurich → London | 1937 | Transposition of telegraphic Spanish. Every single transposition and every double columnar with a second key of ten or fewer letters excluded against planted controls (lag scan plus exhaustive second-key enumeration). Open: double columnar with two long keys; needs the second telegram. Attempted, not solved | [`blume/`](blume/) |

### Surveys

- [`top50/`](top50/) — Schmeh's Top 50 cross-referenced entry by entry and re-checked against what has been solved since each post.
- [Why the famous ciphers resist](https://dbourdeau.github.io/cyphersolver/famous.html) — Kryptos, Voynich, Dorabella, Beale, Linear A, Phaistos, the pigeon message, sorted by the actual reason each holds out.

## Repository layout

```
README.md          this file
TARGETS.md         ranked tracker of every list entry
SOLVED_RANKING.md  the solved targets ranked by difficulty and historical weight
unsolved.htm       snapshot of Tomokiyo's source page, for diffing against later revisions
docs/              the website (GitHub Pages), see below
<target>/          one directory per target: NOTES.md, ciphertext, scripts, small derived data
```

Every target directory except `barney/` has a `NOTES.md`. Large downloads (microfilm, corpora, OCR, run logs, images)
are excluded by [`.gitignore`](.gitignore) and regenerated by the scripts named in each directory's notes.

### The website

`docs/` is served by GitHub Pages. One manifest in [`docs/_build_site.py`](docs/_build_site.py) drives the navigation,
footers with previous/next links, "On this page" strips and the index cards. After editing any page:

```bash
cd docs && python _build_site.py
```

The builder is idempotent. The priority queue on the index page is generated separately from
[`docs/_queue.json`](docs/_queue.json) by `python _build_queue.py`.

## Reproducing the two flagship results

### Armstrong → Madison, 30 August 1808

John Armstrong (U.S. Minister to France) ended a private letter to Madison with 49 groups of the diplomatic code he used
1804–1810, in which 972 = *the*. The code was never published. It was reconstructed from the State Department's own
pencil interlinear decodes on NARA microfilm M34 roll 13 (frames 0192–0201, a despatch of October 1806), merged with
Tomokiyo's known-plaintext values from the letter of 4 May 1806, and completed by alphabetical-slot inference. Reading:

> Russel ought to be the consul: he is an American by birth, and is much better qualified than any other candidate. In a
> word, he is above men in general. Next to him in fitness is O'Mealy, but he is, like Warden, an Irishman.

| file | purpose |
|---|---|
| `armstrong/NOTES.md` | group-by-group evidence, corrections to the Founders transcription, residual doubts |
| `armstrong/pairs.txt` | ~500 number → syllable pairs read from the pencil decodes, with frame/line reference and H/M grade |
| `armstrong/code972_partial.json` | Tomokiyo's table from the 4 May 1806 known plaintext (base layer) |
| `armstrong/decode972.py` | merges the three layers and renders any coded passage: `python decode972.py ps\|feb\|all\|table` |
| `armstrong/export_key.py` → `key972.js` | exports the merged 580-group table for the website decoder |
| `armstrong/pencil_score.py` | ranks microfilm frames by amount of faint pencil (finds the annotated despatches) |
| `armstrong/crawl_wb.py` | follows Founders Online correspondent links via the Wayback Machine to list coded letters |

Not in the repo: the 393 roll-13 frames (2.5 GB, from [NARA catalog 188671172](https://catalog.archives.gov/id/188671172)),
roll 14, crops, and the downloaded Founders/LOC pages. The decode reproduces from tracked files alone:

```bash
cd armstrong && python decode972.py all
```

### Richelieu → M. de Rancé, July 1629

Homophonic substitution recovered by ciphertext-only analysis from a published transcription, then found to agree
word for word with the decipherment printed by Avenel in 1858 (*Lettres … du cardinal de Richelieu*, t. III,
pp. 368–369, 381–383). The letters are listed as undeciphered in current catalogues (cryptiana; DECODE R9461–R9462)
and should be marked solved. Full write-up: [richelieu/SOLUTION.md](richelieu/SOLUTION.md).

| file | purpose |
|---|---|
| `richelieu/richelieu1629.txt` | S. Tomokiyo's transcription (source) |
| `richelieu/parse.py` | tokenise transcription, frequency / n-gram stats |
| `richelieu/build_ngrams.py` | build French quadgram model from Gutenberg texts |
| `richelieu/solve.py` | simulated-annealing homophonic solver (`--fix`, `--core`, `--weight`) |
| `richelieu/render.py`, `final.py` | render letters with a hand-built / final key |
| `richelieu/avenel.py`, `avenel_ctx.py` | fetch and search Avenel vol. III OCR (Internet Archive) |

```bash
cd richelieu && pip install requests && python build_ngrams.py && python solve.py --restarts 8 && python final.py
```

## Conventions

- Every claimed reading is graded: **H** read from a primary key source, **C** from a known-plaintext letter, **M** uncertain,
  **I** inferred from context or alphabetical position. The website decoders show the grade per group.
- A negative result is only reported alongside a matched control: a synthetic text of the same length, alphabet and cipher
  design that the same solver does recover.
- Before treating a catalogue item as unsolved, check the 19th-century printed editions (Avenel, Camden Society,
  Nuntiaturberichte) and the comment threads of the list posts. Six items so far were already solved in the open.
- Dates in notes are absolute. Sessions are dated so that "since" claims can be checked against the source lists' last-modified dates.

## Publication drafts

[`papers/`](papers/) holds anonymised HistoCrypt-format drafts of the solved results (two regular papers, one short paper), the
official style files, a shared bibliography, and a README with the verified format rules and the pre-submission checklist.
Unvalidated drafts, not submitted.

## Contact

Daniel Bourdeau, [dnbourdeau@gmail.com](mailto:dnbourdeau@gmail.com). Corrections, prior solutions I have missed,
archive copies, or pointers to key material are all welcome. Issues and pull requests on this repository work too.

## Licence

Text and notes CC BY 4.0; code MIT. Manuscript images are from the Library of Congress, National Archives, BnF, JACAR and
the IACR and remain subject to those institutions' terms.
