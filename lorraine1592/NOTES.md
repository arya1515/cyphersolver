# Charles III of Lorraine to the comte de Vaudémont, Nancy, 18 June 1592 (BnF fr. 3621 no. 97)

**Status: not read (18 Sept 2026). The catalogue's verification question is answered, negatively; the
cipher is attacked and not broken, with the failure measured.** Catalogue item 15.

## 1. The verification step, answered

The catalogue set this task first: *"Look for the ciphered originals of the January intercepts in
fr. 3621."* They are not there. **No. 22 (fol. 31) is a plaintext decipherment only** — a fair copy of the
French of three intercepted Vaudémont letters, with no cipher anywhere on the sheet, headed "Dechiffrement
des lettres de Monsieur de Vaudemont à Monsieur de Lorraine [son] pere, interceptées et apportées à
Monsieur de Dinteville, le XX[e] Janvier 1592". Nothing else in the volume is described as intercepted;
"intercept" occurs once in the whole BnF notice, in that entry. So the hoped-for crib — decipherment
against its own ciphertext — does not exist in this volume, and the catalogue's own scoring note ("if
no. 22's decipherment corresponds to a cipher copy elsewhere in the volume the key falls; otherwise a
single copy") resolves to the second branch.

## 2. What the documents are

Gallica `btv1b52524472n`, 286 canvases, single pages about 4266 × 5883 — good images, not microfilm.
**Canvas = 2 × folio + 9**, fixed on fol. 30 (canvas 69, the Nevers letter of 14 January that the notice
assigns to no. 21). In this notice the folio printed *before* a piece number belongs to that piece.

| piece | leaf | canvas | content |
|---|---|---|---|
| 22 | fol. 31 | 71 | decipherment of three intercepted Vaudémont letters, plaintext only |
| **97** | **fol. 109** | **227** | **"Coppie d'une lettre … de Charles de Lorraine à monsieur de Vaudemont", Nancy, 18 June 1592, with cipher** |

The volume is Nevers's own intercept and correspondence file for 1591–92, and it holds several letters
"avec chiffre et déchiffrement" from his own correspondents — Lodovico Birago (nos. 31, 35), Nicolas
Potier de Blancmesnil (no. 79), Dinteville (no. 114). Those are the Nevers side's own keys, not this one.

## 3. The cipher of no. 97

About twenty lines, set inside the letter between clear openings and a clear close, with a wholly clear
postscript after the signature. It is a mixed system: an alphabet of **ordinary-looking cursive letters
plus a few special signs** (a lambda, a dotted circle, a cross), **figures for names and words** running
from the thirties to about 146 (57, 88, 98, 103, 121, 122, 123, 137, 139, 141, 145, 146 all occur), and
some **letters carrying an overbar**. The flanking clear text is about the same business as the cipher must
be: munitions promised and undelivered, the inhabitants of Chaumont, the sieur de Buzonville, and the
attempt on **Chasteauvillain**. Transcriptions in `ct/clear_texts.md`.

## 4. The key is not published

* Tomokiyo's survey of cipher material in the *Mémoires de la Ligue* covers **fr. 3974–3995 only**;
  fr. 3621 is outside it. Neither his League page nor his Nevers-collection page mentions fr. 3621, and
  neither mentions a Lorraine–Vaudémont cipher.
* fr. 3995, the Nevers key book ("Recueil de chiffres avec leurs clefs, de l'année 1580 à l'année 1595"),
  does contain keys **reconstructed from intercepted League letters** — no. 39 (fol. 72, 1591, "extracted
  from an intercepted letter", endorsement illegible to Tomokiyo), no. 48 (fol. 90, Mayenne with Aumale),
  nos. 50 and 51 (fol. 91v, Péricard with Saint-Laurin, Mayenne with Villars). Those were the obvious
  candidates, since Nevers's office demonstrably broke this family by January 1592. I read the sheets:
  no. 48 is a symbol-only alphabet with no figures; the tables at canvases 151 and 156 are figure-alphabet
  keys with "Motz", "Provinces" and "Noms propres" columns. **None matches a letter alphabet with a
  numeric nomenclator to ~146.** So the key for this correspondence is, as far as I can find, unpublished
  and not in the Nevers book.

## 5. The attack, and where it fails

Built on the pure-Python tooling from `../sormano1529`, with one genuine improvement worth keeping.

**Deskew works, and is the useful result.** The baselines of this page slope, which smears any horizontal
ink profile and had my first line-finder reporting 13 bands with absurd gaps. `deskew.py` searches for the
shear that minimises the entropy of the histogram of component y-centres; the optimum is **−0.032**, and
at that shear the histogram resolves into 22 clean peaks about 88 px apart. With a line gap of 12 px it
segments **20 lines and 1,114 glyphs in correct reading order**, with consistent line lengths of 45–73
glyphs. This is the right way to segment sloping manuscript lines and it is reusable.

**The solve fails.** `cluster2.py` clusters the glyphs by the blurred, shift-tolerant mask metric;
`solve.py` is a homophonic solver — each cipher cluster maps independently to a letter, so a letter may
have several forms and over-segmentation is absorbed — scored by a 4-gram model of sixteenth-century
French built from Montaigne's *Essais* (`src/fr4ns.json`; 6.4 M letters after stripping roman numerals,
which otherwise poison the model with runs of "iiii"), with a penalty holding the induced letter
frequencies near French. Simulated annealing, 8 restarts, 500,000 iterations.

| setting | result |
|---|---|
| real French text, same model | **−1.85 per character** |
| degenerate all-one-letter mapping | −3.09 |
| solve at 58 clusters | −2.96 |
| solve at 103 clusters | −2.78 |

Between −2.78 and −2.96 against −1.85 is not a solution; the output has French-looking fragments and is
not text. Two causes, both identified rather than guessed:

1. **The shape clustering does not cleanly separate the letters.** Sampled pair distances give p1 = 0.056,
   p5 = 0.113, median 0.263 — no gap between same-glyph and different-glyph, the same weakness measured at
   length in `../sormano1529/NOTES.md`. Thresholds either over-segment (103 clusters) or merge different
   letters (32 clusters, the largest holding 26 % of all glyphs).
2. **The model is wrong for this cipher.** The nomenclator figures segment into individual digits (roughly
   4 % of glyphs) and cannot map to letters at all; and these League ciphers routinely carry nulls and
   signs for double letters and small words, which a pure letter-substitution model cannot absorb. Fixing
   this needs the figures detected and excluded, and nulls modelled — not just a better clusterer.

## 6. What would finish it

* **A published key.** The Sormano case in this repository is the cautionary precedent: I reported there
  that no published key existed, and was wrong — it was on a page I had not searched. For this
  correspondence the places to look are Lasry's work on League ciphers and any treatment of fr. 3621,
  which Tomokiyo's League survey does not reach.
* **Detect the figures before solving.** The digits are visually distinct from the letter forms; excluding
  them, and treating each multi-digit group as one unknown token, would remove about 4 % of pure noise and
  let the letter model fit what it can.
* **A crib from the correspondence.** No. 22 gives the vocabulary and the proper names of this exchange in
  plaintext — Parme, Mayenne, Rouen, Villeroy, Pontoise, Bellievre, Dinteville, the Pope, the légat — which
  is what the figures to 146 will encode. Matched against a figure-frequency profile it is a way in to the
  nomenclator even without the alphabet.

## 7. What the letters say, from the clear text

In `ct/clear_texts.md`. The June letter's clear portions have the Duke urging his son to press the attempt
on **Chasteauvillain**, complaining of munitions promised and undelivered, and naming Chaumont and
Buzonville. No. 22's decipherment carries the January business: the Spanish army's march on Rouen, the duc
de Mayenne finding the Spaniards resolved on a battle, Parma's judgement, the cavalry; and then the
political matter — the papal legate, the Spanish pretensions, Villeroy at Pontoise, the house of Bourbon,
Bellievre, and the peace which nobody could support the war's length without. That is the double game the
catalogue points at: the Duke of Lorraine's son inside the League army reporting home on Parma and on
feelers toward Henri IV, and the King's side reading his letters.

## 8. Files

`fetch.sh`, `zoom.sh`, `zoom71.sh` (page and region fetches), `fetch3995.sh` (the Nevers key book),
`deskew.py` (shear deskew and line segmentation — the reusable piece), `lines.py`, `stitch.py`, `pipe.py`
(earlier, superseded line finders kept for the record), `cluster.py`, `cluster2.py` (shape clustering),
`solve.py` (homophonic solver), `ct/clear_texts.md`, `ct/no97_*.txt` (clustered ciphertexts),
`src/` (manifests, notices, Tomokiyo's pages, the French corpus and 4-gram model).

Checked: the folio-to-canvas mapping on a foliated leaf; that no. 22 carries no cipher; the piece list
against the notice; the absence of fr. 3621 from Tomokiyo's League survey; three candidate key sheets in
fr. 3995; the deskew and line segmentation; the solver's score against real French. Not checked: the
remaining ~60 key sheets in fr. 3995 one by one; whether Lasry has published this cipher; any printed
edition of these letters. User must verify: the clear-text transcriptions are my readings of a secretary
hand and the uncertain words are marked.
