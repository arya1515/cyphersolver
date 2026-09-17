# Henri IV to Philippe de Béthune (Rome), 9, 10 and 22 November 1601 — BnF fr. 3484 nos. 7, 8, 12 (catalogue item 22)

**Status, 17 Sept 2026: partly read.** The 10 November letter (f. 34) is read in full, because its minute survives in
clear four leaves on (f. 36, the notice's "copie du n° précédent"); that pair, six glossed passages of the 8 November
letter and a glossed passage of 10 December give the cipher's design and most of its letter values; the 9 November
letter (f. 33, one page entirely in cipher) decodes to about half of its words with that key and a French language
model; the 22 November letter (ff. 46–47, some forty lines) is transcribed in part and not decoded. The key is a
Villeroy-office cipher of the same design as the one Bazeries printed for Béthune's brother in 1599 (letters =
figures and letter-shaped symbols with homophones; letters with a comma, one dot or two dots = words in alphabetical
series; two-digit figures = names), with different values.

Working files: `corpus.txt` (known-plaintext pairs), `ct_f33.txt` (the 9 Nov cipher, 1.5× transcription),
`em_align.py` / `em_model.json` (EM alignment and the learned P(unit | symbol)), `decode.py` (character 5-gram
Viterbi) and `worddecode.py` (lexicon decoder, trie over the Xivrey volumes), `decode_f33.txt` (their output),
`key.tsv` (the key as recovered), `reading_10nov.md` (the 10 Nov letter). Images (`img/`, `full/`, crops, the
Xivrey and Bazeries downloads) are gitignored; `fetch.py` / `fetch_full.py` refetch them (Gallica IIIF, canvas =
2 × folio + 7 for a recto).

## Leaf map (from the images; the notice's folio guesses in the catalogue were wrong)

| item | date | folios | canvases | cipher | decipherment |
|---|---|---|---|---|---|
| 6 | Paris, 8 Nov 1601 | 30r–31v | 67–70 | six passages, 1–5 lines each | numbered marginal glosses in a smaller hand (paraphrase, near-verbatim) |
| 7 | Paris, 9 Nov 1601 | **33r** | 73 | 22 full lines, one passage after "il me mande qu'il est certain que" | **none** |
| 8 | Paris, 10 Nov 1601 | **34r–v** | 75–76 | 4 + 8 + 2 + 3 lines in four passages | **none on the leaf; the minute f. 36r–v (item 9) is in clear** |
| 9 | "Du Xe 9bre 1601" | 36r–v | 79–80 | none | the minute of no. 8, with corrections |
| 10 | Saint-Germain, 18 Nov | 43–44 | 93–95 | none | – |
| 12 | Saint-Germain, 22 Nov 1601 | **46r–47v** | 99–102 | c. 40 lines in several blocks | **none** (no clear copy found; f. 45 and f. 48 are address leaves) |
| 13 | Paris, 10 Dec 1601 | 49r–50v | 105–108 | 5 lines on 49v, c. 9 on 50r | footnote gloss on 49v (verbatim), marginal glosses on 50r |
| 14 | 24 Dec 1601 | 53 | 113 | 9 + 2 lines | marginal glosses |
| 16–17 | Jan 1602 | 56–57 | 119–121 | several blocks | marginal glosses |

Bazeries 1901, pp. 28–29 ("Chiffre baillé à M. de Béthune, 1599", Gallica bpt6k325768q, canvases 40–41) is the
elder brother's key of the same office: A = 3 + three symbols, B = 10 …; names = figures with two dots (Le Roy 4̈,
Le Pappe 3̈, Le Roy d'Espagne 2̈, Aldobrandin not present); words = a, ayant … z, nous; ä nostre … ÿ selon; 2, tout …
11, vivs; Δ doubles, y and $ cancel. The 1601 key uses the same conventions with other values.

## What is read

**10 November 1601 (f. 34).** The minute f. 36 gives the text of every enciphered passage; the sent original follows
it word for word except for small variants ("la somme de dix mil escus" written with the figures 6 7 1 for *a t i*
in "gratification"; "faites doncques valoir … et faites semblant que vous n'aiez receu la presente"). Reading in
`reading_10nov.md`. The passages: the King had "ce pretexte de gratifier led. Cardinal" [Aldobrandini] after the
Parlement's judgment in the Este–Aldobrandini debt, paid him 10,000 écus through Sillery at once, will pay 10,000
more in the first four months of 1602 through Sillery's brother "sans avoir esgard à l'arrest obtenu par lad.
duchesse de Nemours", wants Béthune to tell Cardinal Aldobrandini through Cardinal d'Ossat, "de facon qu'il recoive
et estime ceste grace comme elle merite", to pretend not to have received the letter, and to be "le premier qui en
avertira led. Cardinal Aldobrandin".

**Key.** `key.tsv`. Letters (confidence from the EM posterior and hand checks at 4× and 7×): e = Z ff EP 0;
a = 4 6 u; i = Cm(hooked m) v a 1; o = f + t; t = q 7 (p uncertain); s = g R2(2-shaped r) n; r = r d(∂-shaped);
l = h B S PH; m = x; f = m; u = y c; v = c; c = b e; p = o T; g = Cu(hooked u); x = f (in *veux*); y = a.
Word signs: f, = le; g, g' = la; x, = que; r, = par; s, = pro; q, q_ = pour; d, DL, = je; x: x^ = et; s: = dit;
t. t: = de; p: p. = ce; f: = au; J = bon; J, = mais; m, = men(t); y: = ent; r: = du; a, = faict; 61 = qui;
63 = re; 65 = si. Names: 48 = Cardinal, 17 = Aldobrandin, 7 = le Roy d'Espagne (P7, f. 56r). Open code groups
in the 9 and 22 Nov letters: 44, 45, 62, 66–72, 26–28, 5, 3, 8.

**9 November 1601 (f. 33).** `decode_f33.txt`. With the key and a lexicon decoder about half the words read; the
letter is about the Spanish news from La Rochepot's secretary and the cardinalate: "…et le [44] de la … cardinal …
de leurs places … le premier …", "…seront d'interest que [69] … partant vous en conférerez [avec] Aldobrandin…",
"…de vous dire … qu'il a de telles pratiques…", "…jamais il m'avoit … proposé de rechercher le cardinal…", "…comme
sera la promo[tion] [71] au cardinalat de … Alexandre communiqu…", "…les cardinaux de Joyeuse et d'Ossat … ensemble
ce que vous aurez…", "…Alexandre quelque instance que je ne face…", "…de partir de ce premier de [62] … des raisons
des dits car[dinaux]". Not a reading yet; a substance.

## Method, and where it stopped

1. Volume fetched (canvases 55–130 at 2000 px; 3996 px originals for the pages worked). Leaves mapped; the minute of
   the 10 Nov letter found by reading the sheets, not from the notice.
2. Known-plaintext corpus (`corpus.txt`): the 10 Nov cipher against the minute (four blocks, c. 480 symbols); the
   six glossed passages of 8 Nov; the footnote passage of 10 Dec. EM alignment (`em_align.py`: monotone, each symbol
   0–12 letters, proper string prior, seeded with hand-verified values, nulls allowed on PH HB $ Y LS) gives
   P(unit | symbol). Two decoders on the 9 Nov transcription: character 5-gram Viterbi over Xivrey's *Lettres
   missives* vols III–V, and a trie/lexicon decoder.
3. Hand checks at 4× and 7× on f. 34 fixed the glyph classes the 1.5× transcription had merged: hooked m (= i) vs
   plain m (= f), 2-shaped r (= s) vs r, u (= a) vs n, 6 (= a) vs b (= c), 671 = *a t i*. They also showed the
   transcription of the 9 Nov leaf carries the same merges, which is why the decoders plateau around half the words.
4. The 22 Nov letter (ff. 46–47) was cut into third-line crops; lines 1–7 read, the rest not. Gallica began
   refusing connections (HTTP 429, then closed connections) after the volume fetch, so the full-resolution copies of
   the glossed leaves ff. 53 and 56 (which would fix the remaining code groups) were not obtained in this session.

**Next step (a day's work, mechanical):** re-transcribe f. 33 and ff. 46–47 at 4× with the refined glyph classes
(`q33_*.jpg` crops exist for f. 33), add the glosses of ff. 49v–50r, 53r, 56r–57r to the corpus from the
full-resolution pages, rerun `em_align.py` and `worddecode.py`. The design is known, the letter values are mostly
known, and the remaining unknowns are the two-digit names, which the later glosses name (Duc de Modène, Roy
d'Espaigne, Archiduc, Fuentes).

Not in Tomokiyo (his Béthune ciphers are fr. 15975 for 1602–05 and fr. 15972 for 1606–08), not in DECODE
(search "Bethune" returns only Charost 1673), not in Xivrey (t. V has no Béthune letter for Nov 1601).
